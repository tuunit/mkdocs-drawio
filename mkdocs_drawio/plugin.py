import re
import json
import mkdocs
import string
import logging
from lxml import etree
from typing import Dict
from html import escape
from pathlib import Path
from bs4 import BeautifulSoup
from mkdocs.plugins import BasePlugin

# ------------------------
# Constants and utilities
# ------------------------
SUB_TEMPLATE = string.Template(
    '<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="$config"></div>'
)

LOGGER = logging.getLogger("mkdocs.plugins.diagrams")

# ------------------------
# Plugin
# ------------------------
class DrawioPlugin(BasePlugin):
    """
    Plugin for embedding Drawio Diagrams into your MkDocs
    """

    config_scheme = (
        ("viewer_js",mkdocs.config.config_options.Type(str, default="https://viewer.diagrams.net/js/viewer-static.min.js")),
        ("toolbar",mkdocs.config.config_options.Type(bool, default=True)),
        ("tooltips",mkdocs.config.config_options.Type(bool, default=True)),
        ("border",mkdocs.config.config_options.Type(int, default=0)),
    )

    def on_post_page(self, output_content, config, page, **kwargs):
        return self.render_drawio_diagrams(output_content, page)

    def render_drawio_diagrams(self, output_content, page):
        if ".drawio" not in output_content.lower():
            return output_content

        plugin_config = self.config.copy()

        soup = BeautifulSoup(output_content, "html.parser")

        diagram_config = {
            "toolbar": "zoom" if plugin_config["toolbar"] else None,
            "tooltips": "1" if plugin_config["tooltips"] else "0",
            "border": plugin_config["border"] + 5,
            "resize": "1",
            "edit": "_blank",
        }

        # search for images using drawio extension
        diagrams = soup.findAll("img", src=re.compile(r".*\.drawio$", re.IGNORECASE))
        if len(diagrams) == 0:
            return output_content

        # add drawio library to body
        lib = soup.new_tag("script", src=plugin_config["viewer_js"])
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
                mxgraph = BeautifulSoup(
                    DrawioPlugin.substitute_with_file(diagram_config, path, diagram["src"], diagram["alt"]),
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
            LOGGER.error(f"Error: Provided diagram file '{src}' on path '{path}' is not a valid diagram")
            diagram_xml = etree.fromstring('<invalid/>')

        diagram = DrawioPlugin.parse_diagram(diagram_xml, alt)
        config["xml"]=diagram

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
                LOGGER.warning(f"Warning: Found {len(page)} results for page name '{alt}' for diagram '{src}' on path '{path}'")

            return etree.tostring(mxfile, encoding=str)
        except Exception:
            LOGGER.error(f"Error: Could not properly parse page name '{alt}' for diagram '{src}' on path '{path}'")
        return ""
