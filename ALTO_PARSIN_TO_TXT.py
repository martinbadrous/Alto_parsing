#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 11:47:40 2023

@author: martin
"""
import argparse
import codecs
import io
import os
import re
import sys
import xml.etree.ElementTree as ET
import numpy as np
__version__ = "0.0.2"


def alto_parse(alto, **kargs):
    """Convert ALTO xml file to element tree"""
    try:
        xml = ET.parse(alto, **kargs)
    except ET.ParseError as e:
        print(f"Parser Error in file '{alto}': {e}")
    # Register ALTO namespaces
    # https://www.loc.gov/standards/alto/ | https://github.com/altoxml
    # alto-bnf (unofficial) BnF ALTO dialect - for further info see
    # http://bibnum.bnf.fr/alto_prod/documentation/alto_prod.html
    namespace = {
        "alto-1": "http://schema.ccs-gmbh.com/ALTO",
        "alto-2": "http://www.loc.gov/standards/alto/ns-v2#",
        "alto-3": "http://www.loc.gov/standards/alto/ns-v3#",
        "alto-4": "http://www.loc.gov/standards/alto/ns-v4#",
        "alto-bnf": "http://bibnum.bnf.fr/ns/alto_prod",
    }
    # Extract namespace from document root
    if "http://" in str(xml.getroot().tag.split("}")[0].strip("{")):
        xmlns = xml.getroot().tag.split("}")[0].strip("{")
    else:
        try:
            ns = xml.getroot().attrib
            xmlns = str(ns).split(" ")[1].strip("}").strip("'")
        except IndexError:
            sys.stderr.write(
                f'\nERROR: File "{alto.name}": no namespace declaration found.'
            )
            xmlns = "no_namespace_found"
    if xmlns in namespace.values():
        return alto, xml, xmlns
    else:
        sys.stdout.write(
            f'\nERROR: File "{alto.name}": namespace {xmlns} is not registered.\n'
        )
from xml.dom import minidom

# parse an xml file by name
file = minidom.parse('00023.xml')

x, y, z = alto_parse('00023.xml')

def alto_text_HPOS(xml, xmlns):
    """Extract text content from ALTO xml file"""
    # Ensure use of UTF-8
    if isinstance(sys.stdout, io.TextIOWrapper) and sys.stdout.encoding != "UTF-8":
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    text = []
    # Find all <TextLine> elements
    for lines in xml.iterfind(".//{%s}TextLine" % xmlns):
        # New line after every <TextLine> element
        # Find all <String> elements
        for line in lines.findall("{%s}String" % xmlns):
            # Check if there are no hyphenated words
            if "SUBS_CONTENT" not in line.attrib and "SUBS_TYPE" not in line.attrib:
                # Get value of attribute @CONTENT from all <String> elements
                text.append(line.attrib.get("HPOS") + " ")
            else:
                if "HypPart1" in line.attrib.get("SUBS_TYPE"):
                    text.append(line.attrib.get("SUBS_CONTENT") + " ")
                    if "HypPart2" in line.attrib.get("SUBS_TYPE"):
                        pass
    return text
def alto_text_VPOS(xml, xmlns):
    """Extract text content from ALTO xml file"""
    # Ensure use of UTF-8
    if isinstance(sys.stdout, io.TextIOWrapper) and sys.stdout.encoding != "UTF-8":
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    text = []
    # Find all <TextLine> elements
    for lines in xml.iterfind(".//{%s}TextLine" % xmlns):
        # New line after every <TextLine> element
        # Find all <String> elements
        for line in lines.findall("{%s}String" % xmlns):
            # Check if there are no hyphenated words
            if "SUBS_CONTENT" not in line.attrib and "SUBS_TYPE" not in line.attrib:
                # Get value of attribute @CONTENT from all <String> elements
                text.append(line.attrib.get("VPOS") + " ")
            else:
                if "HypPart1" in line.attrib.get("SUBS_TYPE"):
                    text.append(line.attrib.get("SUBS_CONTENT") + " ")
                    if "HypPart2" in line.attrib.get("SUBS_TYPE"):
                        pass
    return text
def alto_text_HEIGHT(xml, xmlns):
    """Extract text content from ALTO xml file"""
    # Ensure use of UTF-8
    if isinstance(sys.stdout, io.TextIOWrapper) and sys.stdout.encoding != "UTF-8":
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    text = []
    # Find all <TextLine> elements
    for lines in xml.iterfind(".//{%s}TextLine" % xmlns):
        # New line after every <TextLine> element
        # Find all <String> elements
        for line in lines.findall("{%s}String" % xmlns):
            # Check if there are no hyphenated words
            if "SUBS_CONTENT" not in line.attrib and "SUBS_TYPE" not in line.attrib:
                # Get value of attribute @CONTENT from all <String> elements
                text.append(line.attrib.get("HEIGHT") + " ")
            else:
                if "HypPart1" in line.attrib.get("SUBS_TYPE"):
                    text.append(line.attrib.get("SUBS_CONTENT") + " ")
                    if "HypPart2" in line.attrib.get("SUBS_TYPE"):
                        pass
    return text
def alto_text_WIDTH(xml, xmlns):
    """Extract text content from ALTO xml file"""
    # Ensure use of UTF-8
    if isinstance(sys.stdout, io.TextIOWrapper) and sys.stdout.encoding != "UTF-8":
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    text = []
    # Find all <TextLine> elements
    for lines in xml.iterfind(".//{%s}TextLine" % xmlns):
        # New line after every <TextLine> element
        # Find all <String> elements
        for line in lines.findall("{%s}String" % xmlns):
            # Check if there are no hyphenated words
            if "SUBS_CONTENT" not in line.attrib and "SUBS_TYPE" not in line.attrib:
                # Get value of attribute @CONTENT from all <String> elements
                text.append(line.attrib.get("WIDTH") + " ")
            else:
                if "HypPart1" in line.attrib.get("SUBS_TYPE"):
                    text.append(line.attrib.get("SUBS_CONTENT") + " ")
                    if "HypPart2" in line.attrib.get("SUBS_TYPE"):
                        pass
    return text

vertical = alto_text_VPOS(y, z)
horizontal= alto_text_HPOS(y, z)
width= alto_text_WIDTH(y, z)
hight= alto_text_HEIGHT(y, z)

top_left_point_position = np.row_stack((vertical,horizontal))
bounding_box=np.row_stack((hight,width))
np.savetxt('top_left_point_position.txt', top_left_point_position, fmt='%s')
np.savetxt('bounding_box.txt', bounding_box, fmt='%s')
