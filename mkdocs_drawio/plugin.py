import re
import json
import string
import logging
from lxml import etree
from typing import Dict
from html import escape
from pathlib import Path
from bs4 import BeautifulSoup
from mkdocs.utils import copy_file
from mkdocs.plugins import BasePlugin
from mkdocs.config import base, config_options as c

SUB_TEMPLATE = string.Template(
    '<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="$config"></div>'
)

LOGGER = logging.getLogger("mkdocs.plugins.diagrams")


class DrawioConfig(base.Config):
    """Configuration options for the Drawio Plugin"""

    viewer_js = c.Type(
        str, default="https://viewer.diagrams.net/js/viewer-static.min.js"
    )
    toolbar = c.Type(bool, default=True)
    tooltips = c.Type(bool, default=True)
    border = c.Type(int, default=0)
    edit = c.Type(bool, default=True)
    darkmode = c.Type(bool, default=False)


class DrawioPlugin(BasePlugin[DrawioConfig]):
    """
    Plugin for embedding Drawio Diagrams into your MkDocs
    """

    def on_post_page(self, output_content, config, page, **kwargs):
        return self.render_drawio_diagrams(output_content, page)

    def render_drawio_diagrams(self, output_content, page):
        if ".drawio" not in output_content.lower():
            return output_content

        soup = BeautifulSoup(output_content, "html.parser")

        diagram_config = {
            "toolbar": "zoom" if self.config.toolbar else None,
            "tooltips": "1" if self.config.tooltips else "0",
            "border": self.config.border + 5,
            "resize": "1",
            "edit": "_blank" if self.config.edit else None,
        }

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

        for diagram in diagrams:
            if re.search("^https?://", diagram["src"]):
                mxgraph = BeautifulSoup(
                    DrawioPlugin.substitute_with_url(diagram_config, diagram["src"]),
                    "html.parser",
                )
            else:
                diagram_page = diagram["alt"]
                # Use page attribute instead of alt if it is set
                if "page" in diagram:
                    diagram_page = diagram["page"]
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
    def substitute_with_file(config: Dict, path: Path, src: str, alt: str) -> str:
        try:
            diagram_xml = etree.parse(path.joinpath(src).resolve())
        except Exception:
            LOGGER.error(
                f"Error: Provided diagram file '{src}' on path '{path}' is not a valid diagram"
            )
            diagram_xml = etree.fromstring("<invalid/>")

        diagram = DrawioPlugin.parse_diagram(diagram_xml, alt)
        config["xml"] = diagram

        return SUB_TEMPLATE.substitute(config=escape(json.dumps(config)))

    @staticmethod
    def parse_diagram(data, alt, src="", path=None) -> str:
        if alt is None or len(alt) == 0:
            return etree.tostring(data, encoding=str)

        try:
            mxfile = data.xpath("//mxfile")[0]

            # try to parse for a specific page by using the alt attribute
            page = mxfile.xpath(f"//diagram[@name='{alt}']")

            if len(page) == 1:
                parser = etree.XMLParser()
                result = parser.makeelement(mxfile.tag, mxfile.attrib)

                result.append(page[0])
                return etree.tostring(result, encoding=str)
            else:
                LOGGER.warning(
                    f"Warning: Found {len(page)} results for page name '{alt}' for diagram '{src}' on path '{path}'"
                )

            return etree.tostring(mxfile, encoding=str)
        except Exception:
            LOGGER.error(
                f"Error: Could not properly parse page name '{alt}' for diagram '{src}' on path '{path}'"
            )
        return ""

    def on_config(self, config: base.Config):
        """Load embedded files"""
        self.base = Path(__file__).parent
        self.css = []
        self.js = []

        if self.config.darkmode:
            self.css.append("css/drawio-darkmode.css")
            self.js.append("js/drawio-darkmode.js")

        for path in self.css:
            config.extra_css.append(str(path))
        for path in self.js:
            config.extra_javascript.append(str(path))

    def on_post_build(self, config: base.Config):
        """Copy embedded files to the site directory"""
        site = Path(config["site_dir"])
        for path in self.css + self.js:
            copy_file(self.base / path, site / path)
