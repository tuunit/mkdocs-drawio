""" MkDocs Drawio Plugin """

import re
import json
import string
import logging
from lxml import etree
from typing import Dict
from html import escape
from pathlib import Path
from bs4 import BeautifulSoup, Tag
from mkdocs.plugins import BasePlugin
from mkdocs.config import base, config_options as c
from mkdocs.utils import copy_file
from collections import namedtuple

SUB_TEMPLATE = string.Template(
    '<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="$config"></div>'
)

LOGGER = logging.getLogger("mkdocs.plugins.diagrams")


class Toolbar(base.Config):
    """Configuration options for the toolbar, mostly taken from
    https://www.drawio.com/doc/faq/embed-html-options
    """

    pages = c.Type(bool, default=True)
    """ Display the page selector in the toolbar """

    zoom = c.Type(bool, default=True)
    """ Display the zoom control in the toolbar """

    layers = c.Type(bool, default=True)
    """ Display the layers control in the toolbar """

    lightbox = c.Type(bool, default=True)
    """ Display the open in lightbox control in the toolbar """

    position = c.Choice(["top", "bottom"], default="top")
    """ Position of the toolbar """

    no_hide = c.Type(bool, default=False)
    """ Whether to hide the toolbar when the mouse is not over it """


class DrawioConfig(base.Config):
    """Configuration options for the Drawio Plugin"""

    toolbar = c.SubConfig(Toolbar)
    """ Whether to show the toolbar with controls """

    tooltips = c.Type(bool, default=True)
    """ Whether to show tooltips """

    border = c.Optional(c.Type(int))
    padding = c.Type(int, default=10)
    """ Padding around the diagram, border will be deprecated
    but kept for backwards compatibility """

    edit = c.Type(bool, default=True)
    """ Whether to allow editing the diagram """

    alt_as_page = c.Type(bool, default=True)
    """ Whether to use the alt attribute as page name """

    def _post_validate(self):
        if self.border is not None:
            self.padding = self.border

        return super()._post_validate()


class DrawioPlugin(BasePlugin[DrawioConfig]):
    """
    Plugin for embedding Drawio Diagrams into your MkDocs
    """

    RE_DRAWIO_FILE = re.compile(r".*\.drawio$", re.IGNORECASE)

    def on_config(self, config: base.Config):
        """Add the drawio viewer library to the site"""
        self.base = Path(__file__).parent
        self.css = ["css/drawio.css"]
        self.js = ["js/drawio.js", "js/viewer-static.min.js"]

        for path in self.css:
            config.extra_css.append(str(Path("/") / path))
        for path in self.js:
            config.extra_javascript.append(str(Path("/") / path))

    def on_post_build(self, config: base.Config):
        """Copy assets to the site directory"""
        site = Path(config["site_dir"])
        for path in self.css + self.js:
            copy_file(self.base / path, site / path)

    def get_diagram_config(self, diagram: Tag) -> Dict:
        """Get the configuration for the diagram. Apply either default values in the plugin
        or values passed in the diagram tag from `attr_list` markdown extension."""

        # Coercion functions
        def no_action(x):
            return x

        def to_bool(x):
            if isinstance(x, bool):
                return x
            if x.lower() in ["true", "1", "yes"]:
                return True
            if x.lower() in ["false", "0", "no"]:
                return False
            LOGGER.warning(f'Could not parse boolean value "{x}"')
            return False

        def to_int_or_str(x):
            try:
                return int(x)
            except ValueError:
                return x

        class to_str:
            def __init__(self, text):
                self.text = text

            def __call__(self, enabled):
                return self.text if enabled else ""

        # To add more options described in https://www.drawio.com/doc/faq/embed-html-options
        # Add a new tuple to the list with the following format:
        T = namedtuple("EmbedOption", ["attr", "name", "default", "coerce"])
        embed_options = [
            T("data-page", "page", None, to_int_or_str),
            T("data-zoom", "zoom", None, no_action),
            T("data-edit", "edit", self.config.edit, lambda x: "_blank" if x else None),
            T("data-padding", "border", self.config.padding, lambda x: int(x) + 5),
            T("data-tooltips", "tooltips", self.config.tooltips, to_bool),
            T(
                "data-toolbar-position",
                "toolbar-position",
                self.config.toolbar.position,
                no_action,
            ),
            T("data-title", "title", None, no_action),
            T("data-nohide", "toolbar-nohide", self.config.toolbar.no_hide, to_bool),
            T(
                "data-toolbar-pages",
                "toolbar",
                self.config.toolbar.pages,
                to_str("pages"),
            ),
            T("data-toolbar-zoom", "toolbar", self.config.toolbar.zoom, to_str("zoom")),
            T(
                "data-toolbar-layers",
                "toolbar",
                self.config.toolbar.layers,
                to_str("layers"),
            ),
            T(
                "data-toolbar-lightbox",
                "toolbar",
                self.config.toolbar.lightbox,
                to_str("lightbox"),
            ),
        ]

        # Get the data-attributes from the diagram tag
        conf = {}
        for option in embed_options:
            value = None
            if option.default is not None:
                value = option.coerce(option.default)
            if option.attr in diagram.attrs:
                value = option.coerce(diagram.attrs[option.attr])
            if value is None:
                continue
            if option.name in conf and isinstance(conf[option.name], str):
                conf[option.name] += f" {value}"
            else:
                conf[option.name] = value

        conf["toolbar"] = conf["toolbar"].strip()
        if conf["toolbar"] == "":
            del conf["toolbar"]
        return conf

    def render_drawio_diagrams(self, output_content, page):
        """Backwards compatibility with mkdocs-print-site."""
        return self.on_post_page(output_content, self.config, page)

    def on_post_page(self, output_content, config, page):
        """Search for drawio diagrams and replace them with the viewer."""

        # Save time if there are no diagrams
        if ".drawio" not in output_content.lower():
            return output_content

        # Substitute images with embedded drawio diagram
        path = Path(page.file.abs_dest_path).parent

        # Search for images using drawio extension
        soup = BeautifulSoup(output_content, "html.parser")
        for diagram in soup.findAll("img", src=self.RE_DRAWIO_FILE):
            diagram_config = self.get_diagram_config(diagram)
            if re.search("^https?://", diagram["src"]):
                mxgraph = BeautifulSoup(
                    self.substitute_with_url(diagram_config, diagram["src"]),
                    "html.parser",
                )
            else:
                diagram_page = (
                    diagram["alt"] if self.config.alt_as_page else diagram.get("page")
                )
                mxgraph = BeautifulSoup(
                    self.substitute_with_file(
                        diagram_config, path, diagram["src"], diagram_page
                    ),
                    "html.parser",
                )
            diagram.replace_with(mxgraph)

        return str(soup)

    def substitute_with_url(self, config: Dict, url: str) -> str:
        config["url"] = url
        return SUB_TEMPLATE.substitute(config=escape(json.dumps(config)))

    def substitute_with_file(self, config: Dict, path: Path, src: str, alt: str) -> str:
        try:
            diagram_xml = etree.parse(path.joinpath(src).resolve())
        except Exception:
            LOGGER.error(
                f"Provided diagram file '{src}' on path '{path}' is not a valid diagram"
            )
            diagram_xml = etree.fromstring("<invalid/>")

        config["xml"] = self.parse_diagram(diagram_xml, alt)

        return SUB_TEMPLATE.substitute(config=escape(json.dumps(config)))

    def parse_diagram(self, data, page_name, src="", path=None) -> str:
        if page_name is None or len(page_name) == 0:
            return etree.tostring(data, encoding=str)

        try:
            mxfile = data.xpath("//mxfile")[0]

            # try to parse for a specific page
            pages = mxfile.xpath(f"//diagram[@name='{page_name}']")

            if len(pages) == 1:
                parser = etree.XMLParser()
                result = parser.makeelement(mxfile.tag, mxfile.attrib)

                result.append(pages[0])
                return etree.tostring(result, encoding=str)
            else:
                LOGGER.warning(
                    f"Found {len(pages)} results for page name '{page_name}' for diagram '{src}' on path '{path}'"
                )

            return etree.tostring(mxfile, encoding=str)
        except Exception:
            LOGGER.error(
                f"Could not properly parse page name '{page_name}' for diagram '{src}' on path '{path}'"
            )
        return ""
