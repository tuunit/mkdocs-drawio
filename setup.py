from setuptools import setup, find_packages
import os.path


def read(name):
    mydir = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(mydir, name)).read()


setup(
    name="mkdocs-drawio",
    version="1.5.4",
    packages=find_packages(),
    url="https://github.com/tuunit/mkdocs-drawio",
    license="MIT",
    author="Sergey Lukin, Jan Larwig",
    author_email="onixpro@gmail.com, jan@larwig.com",
    description="MkDocs plugin for embedding Drawio files",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    install_requires=["mkdocs", "beautifulsoup4", "lxml"],
    entry_points={"mkdocs.plugins": [
        "drawio = mkdocs_drawio:DrawioPlugin",]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
