"""Setup script for rarfile.
"""

from setuptools import setup, Extension

def description_short():
    with open("README.rst") as readme:
        ldesc = readme.read().strip()
        sdesc = ldesc.split('\n')[0].split(' - ')[1].strip()
        return sdesc

def description_long():
    with open("README.rst") as readme:
        return readme.read().strip()

setup(
    description=description_short(),
    long_description=description_long(),
    ext_modules=[
        Extension(
            name="rarfile._rarfile",
            sources=["src/rarfile/rarfile.c"],
        ),
    ],
)

