import os
import xml.etree.ElementTree as ET


def clean_drawio_files(directory="."):
    """
    Look for all .drawio files in the given directory and its subdirectories and
    remove the host and agent attributes from the mxfile element if they exist.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".drawio"):
                file_path = os.path.join(root, file)
                try:
                    tree = ET.parse(file_path)
                    root_element = tree.getroot()

                    if root_element.tag == "mxfile":
                        changed = False
                        for attr in ["host", "agent"]:
                            if attr in root_element.attrib:
                                del root_element.attrib[attr]
                                changed = True

                        if changed:
                            tree.write(
                                file_path, encoding="utf-8", xml_declaration=True
                            )
                            print(f"Nettoyé : {file_path}")
                        else:
                            print(f"Aucun changement : {file_path}")
                except Exception as e:
                    print(f"Erreur lors du traitement de {file_path} : {e}")


if __name__ == "__main__":
    clean_drawio_files()
