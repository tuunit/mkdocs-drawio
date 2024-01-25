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
            "file_extension",
            mkdocs.config.config_options.Type(str, default=".drawio"),
        ),
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
        if ".drawio" not in output_content.lower():
            # Skip unecessary HTML parsing
            return output_content

        soup = BeautifulSoup(output_content, "html.parser")

        # search for images using drawio extension
        diagrams = soup.findAll("img", src=re.compile(r".*\.drawio$", re.IGNORECASE))
        if len(diagrams) == 0:
            return output_content

        # add drawio library to body
        lib = soup.new_tag("script", src=self.config["viewer_js"])
        soup.body.append(lib)

        # substitute images with embedded drawio diagram
        path = Path(page.file.abs_src_path).parent

        for diagram in diagrams:
            diagram.replace_with(
                BeautifulSoup(
                    self.substitute_image(path, diagram["src"], diagram["alt"]),
                    "html.parser",
                )
            )

        return str(soup)

    def substitute_image(self, path: Path, src: str, alt: str):
        diagram_xml = etree.parse(path.joinpath(src))
        diagram = self.parse_diagram(diagram_xml, alt)
        escaped_xml = self.escape_diagram(diagram)

        return SUB_TEMPLATE.substitute(xml_drawio=escaped_xml)

    def parse_diagram(self, data, alt):
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

    def escape_diagram(self, str_xml: str):
        str_xml = str_xml.replace("&", "&amp;")
        str_xml = str_xml.replace("<", "&lt;")
        str_xml = str_xml.replace(">", "&gt;")
        str_xml = str_xml.replace('"', "\&quot;")
        str_xml = str_xml.replace("'", "&apos;")
        str_xml = str_xml.replace("\n", "")
        return str_xml
