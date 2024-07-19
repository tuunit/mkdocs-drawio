import re
import mkdocs
import string
import logging
from lxml import etree
from pathlib import Path
from bs4 import BeautifulSoup
from mkdocs.plugins import BasePlugin

# ------------------------
# Constants and utilities
# ------------------------
SUB_TEMPLATE = string.Template(
    '<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;$xml_drawio&quot;}"></div>'
)


# ------------------------
# Plugin
# ------------------------
class DrawioPlugin(BasePlugin):
    """
    Plugin for embedding Drawio Diagrams into your MkDocs
    """

    config_scheme = (
        (
            "viewer_js",
            mkdocs.config.config_options.Type(
                str, default="https://viewer.diagrams.net/js/viewer-static.min.js"
            ),
        ),
    )

    def __init__(self):
        self.log = logging.getLogger("mkdocs.plugins.diagrams")
        self.pool = None

    def on_post_page(self, output_content, config, page, **kwargs):
        return self.render_drawio_diagrams(output_content, page)

    def render_drawio_diagrams(self, output_content, page):
        if ".drawio" not in output_content.lower():
            # Skip unecessary HTML parsing
            return output_content

        plugin_config = self.config.copy()

        soup = BeautifulSoup(output_content, "html.parser")

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
            diagram.replace_with(
                BeautifulSoup(
                    DrawioPlugin.substitute_image(path, diagram["src"], diagram["alt"]),
                    "html.parser",
                )
            )

        return str(soup)

    @staticmethod
    def substitute_image(path: Path, src: str, alt: str):
        diagram_xml = etree.parse(path.joinpath(src).resolve())
        diagram = DrawioPlugin.parse_diagram(diagram_xml, alt)
        escaped_xml = DrawioPlugin.escape_diagram(diagram)

        return SUB_TEMPLATE.substitute(xml_drawio=escaped_xml)

    @staticmethod
    def parse_diagram(data, alt):
        if alt is None:
            return etree.tostring(data, encoding=str)

        mxfile = data.xpath("//mxfile")[0]

        try:
            # try to parse for a specific page by using the alt attribute
            page = mxfile.xpath(f"//diagram[@name='{alt}']")

            if len(page) == 1:
                parser = etree.XMLParser()
                result = parser.makeelement(mxfile.tag, mxfile.attrib)

                result.append(page[0])
                return etree.tostring(result, encoding=str)
            else:
                print(f"Warning: Found {len(page)} results for page name '{alt}'")
        except Exception:
            print(f"Error: Could not properly parse page name: '{alt}'")

        return etree.tostring(mxfile, encoding=str)

    @staticmethod
    def escape_diagram(str_xml: str):
        str_xml = str_xml.replace("&", r"&amp;")
        str_xml = str_xml.replace("<", r"&lt;")
        str_xml = str_xml.replace(">", r"&gt;")
        str_xml = str_xml.replace('"', r"\&quot;")
        str_xml = str_xml.replace("'", r"&apos;")
        str_xml = str_xml.replace("\n", r"")
        return str_xml
