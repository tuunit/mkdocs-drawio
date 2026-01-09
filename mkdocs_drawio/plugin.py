import re
import json
import string
import logging
from lxml import etree
from html import escape
from pathlib import Path
from typing import Dict
from bs4 import BeautifulSoup
from mkdocs.utils import copy_file
from mkdocs.plugins import BasePlugin
from mkdocs.config import base, config_options as c

SUB_TEMPLATE = string.Template(
    '<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="$config"></div>'
)

LOGGER = logging.getLogger("mkdocs.plugins.diagrams")


class Toolbar(base.Config):
    """Configuration options for the toolbar, mostly taken from
    https://www.drawio.com/doc/faq/embed-html-options
    """

    pages = c.Type(bool, default=True)
    """ Display the page selector """

    tags = c.Type(bool, default=True)
    """ Display the tags selector """

    zoom = c.Type(bool, default=True)
    """ Display the zoom controls """

    layers = c.Type(bool, default=True)
    """ Display the layer controls """

    lightbox = c.Type(bool, default=True)
    """ Display the lightbox / fullscreen button """

    position = c.Choice(["top", "bottom"], default="bottom")
    """ Position of the toolbar """

    no_hide = c.Type(bool, default=False)
    """ Do not hide the toolbar when not hovering over diagrams """


class DrawioConfig(base.Config):
    """Configuration options for the Drawio Plugin"""

    viewer_js = c.Type(
        str, default="https://viewer.diagrams.net/js/viewer-static.min.js"
    )
    """ URL to the Drawio viewer JavaScript file """

    toolbar = c.Type((bool, dict), default=True)
    """ Configuration for the toolbar.

    Can be a bool or a dict. If bool, enables or disables the toolbar
    completely. If dict, allows to configure individual toolbar items.
    """

    tooltips = c.Type(bool, default=True)
    """ Enable tooltips on diagram elements """

    border = c.Type(int, default=0)
    """ Border size / padding around diagrams """

    edit = c.Type(bool, default=True)
    """ Enable opening the editor for diagrams """

    darkmode = c.Type(bool, default=False)
    """ Enable dark mode support """

    highlight = c.Type(str, default="")
    """ Highlight color for hyperlinks """

    lightbox = c.Type(bool, default=True)
    """ Enable to open the lightbox on click """


class DrawioPlugin(BasePlugin[DrawioConfig]):
    """
    Plugin for embedding Drawio Diagrams into your MkDocs
    """

    def get_diagram_config(self) -> Dict:
        """Build diagram config using only global plugin settings."""

        toolbar_items = []

        if self.toolbar_config.pages:
            toolbar_items.append("pages")
        if self.toolbar_config.tags:
            toolbar_items.append("tags")
        if self.toolbar_config.zoom:
            toolbar_items.append("zoom")
        if self.toolbar_config.layers:
            toolbar_items.append("layers")
        if self.toolbar_config.lightbox:
            toolbar_items.append("lightbox")

        toolbar_value = " ".join(toolbar_items) if toolbar_items else None

        config = {
            "toolbar-position": self.toolbar_config.position,
            "toolbar-nohide": "1" if self.toolbar_config.no_hide else "0",
            "tooltips": "1" if self.config.tooltips else "0",
            "border": self.config.border + 5,
            "resize": "1",
            "edit": "_blank" if self.config.edit else None,
            "highlight": self.config.highlight or None,
            "lightbox": "1" if self.config.lightbox else "0",
        }

        if toolbar_value is not None:
            config["toolbar"] = toolbar_value

        return {key: value for key, value in config.items() if value is not None}

    def get_toolbar_config(self, toolbar_config) -> Toolbar:
        config = Toolbar()

        # Bool means enable defaults or disable completely.
        if isinstance(toolbar_config, bool):
            if toolbar_config is False:
                # Flip all toolbar items off but keep other defaults intact.
                for key in ("pages", "tags", "zoom", "layers", "lightbox"):
                    setattr(config, key, False)

        if isinstance(toolbar_config, dict):
            # Load values through mkdocs config validation to respect defaults.
            config.load_dict(toolbar_config)

        config.validate()
        return config

    def on_post_page(self, output_content, config, page, **kwargs):
        return self.render_drawio_diagrams(output_content, page)

    def render_drawio_diagrams(self, output_content, page):
        if ".drawio" not in output_content.lower():
            return output_content

        soup = BeautifulSoup(output_content, "html.parser")

        # search for images using drawio extension
        diagrams = soup.find_all(
            "img", src=re.compile(r".*\.drawio(.svg)?$", re.IGNORECASE)
        )
        if len(diagrams) == 0:
            return output_content

        # add drawio library to body
        lib = soup.new_tag("script", src=self.config.viewer_js)
        soup.body.append(lib)

        # substitute images with embedded drawio diagram
        path = Path(page.file.abs_dest_path).parent

        diagram_config = self.get_diagram_config()

        for diagram in diagrams:
            if re.search("^https?://", diagram["src"]):
                mxgraph = BeautifulSoup(
                    DrawioPlugin.substitute_with_url(diagram_config, diagram["src"]),
                    "html.parser",
                )
            else:
                diagram_page = ""

                # Use page attribute instead of alt if it is set
                if diagram.has_attr("page"):
                    diagram_page = diagram.get("page")
                else:
                    diagram_page = diagram.get("alt")

                mxgraph = BeautifulSoup(
                    DrawioPlugin.substitute_with_file(
                        diagram_config, path, diagram["src"], diagram_page
                    ),
                    "html.parser",
                )

            diagram.replace_with(mxgraph)

        return str(soup)

    @staticmethod
    def substitute_with_url(config: Dict, url: str) -> str:
        config["url"] = url

        return SUB_TEMPLATE.substitute(config=escape(json.dumps(config)))

    @staticmethod
    def substitute_with_file(config: Dict, path: Path, src: str, page: str) -> str:
        try:
            diagram_xml = etree.parse(path.joinpath(src).resolve())
        except Exception as e:
            LOGGER.error(
                f"Error: Could not parse diagram file '{src}' on path '{path}': {e}"
            )
            config["xml"] = ""
            return SUB_TEMPLATE.substitute(config=escape(json.dumps(config)))

        diagram = DrawioPlugin.parse_diagram(diagram_xml, page)
        config["xml"] = diagram
        return SUB_TEMPLATE.substitute(config=escape(json.dumps(config)))

    @staticmethod
    def parse_diagram(data, page_name, src="", path=None) -> str:
        mxfile_nodes = data.xpath("//mxfile")

        if not mxfile_nodes:
            if data.xpath("//*[local-name()='svg']") is not None:
                return etree.tostring(data, encoding=str)
            return ""

        mxfile = mxfile_nodes[0]

        if not page_name:
            return etree.tostring(mxfile, encoding=str)

        page = mxfile.xpath(f"//diagram[@name='{page_name}']")
        if len(page) == 1:
            parser = etree.XMLParser()
            result = parser.makeelement(mxfile.tag, mxfile.attrib)
            result.append(page[0])
            return etree.tostring(result, encoding=str)

        LOGGER.warning(
            f"Warning: Found {len(page)} results for page name '{page_name}' "
            f"falling back to first page."
        )
        return etree.tostring(mxfile, encoding=str)

    def on_config(self, config: base.Config):
        # Prepare toolbar configuration
        self.toolbar_config = self.get_toolbar_config(self.config.toolbar)

        # Prepare list of embedded files
        self.base = Path(__file__).parent
        self.css = []
        self.js = []

        if self.config.darkmode:
            self.css.append("css/drawio-darkmode.css")

        for path in self.css:
            config.extra_css.append(str(path))
        for path in self.js:
            config.extra_javascript.append(str(path))

    def on_post_build(self, config: base.Config):
        """Copy embedded files to the site directory"""
        site = Path(config["site_dir"])
        for path in self.css + self.js:
            copy_file(self.base / path, site / path)
