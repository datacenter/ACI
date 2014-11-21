#!/usr/bin/env python
'''
APIC XML <-> JSON Converter

palesiak@cisco.com

Copyright (C) 2014 Cisco Systems Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Convert APIC encoded JSON to XML or XML to APIC encoded JSON
'''
import sys
from os.path import basename
import xml.etree.ElementTree as ET
import json
import StringIO
from argparse import ArgumentParser


class converter(object):

    def __init__(self):
        pass

    def buildJSON(self, elem):
        jsondict = {elem.tag: {'attributes': elem.attrib}}
        for e in elem:
            if 'children' not in jsondict[elem.tag]:
                jsondict[elem.tag]['children'] = []
            jsondict[elem.tag]['children'].append(self.buildJSON(e))
        return jsondict

    def recurseXMLTree(self, elem):
        return json.dumps(self.buildJSON(elem))

    def buildXML(self, jsondict):
        elem = ET.Element(jsondict.keys()[0])
        elem.attrib = jsondict[jsondict.keys()[0]]['attributes']

        if 'children' in jsondict[jsondict.keys()[0]]:
            for j in jsondict[jsondict.keys()[0]]['children']:
                elem.append(self.buildXML(j))

        return elem

    def recurseJSONDict(self, jsondict):
        return ET.tostring(self.buildXML(jsondict))


def isXMLorJSON(docStr):

    isXML = False
    isJSON = False

    try:
        json.loads(docStr)
        isJSON = True
    except:
        isJSON = False

    try:
        ET.ElementTree(ET.fromstring(docStr))
        isXML = True
    except:
        isXML = False

    if isJSON and isXML:
        raise ValueError(
            'This file appears to be both XML and JSON. I am confused. ' +
            'Goodbye')

    if isJSON:
        return 'json'
    elif isXML:
        return 'xml'
    else:
        return None


def main():
    parser = ArgumentParser('Convert APIC encoded JSON to XML to JSON')
    parser.add_argument('-s', '--stdin', help='Parse input from stdin, for ' +
                        'use as a filter, e.g., cat doc.xml | %s -s' %
                        str(basename(sys.argv[0])), action='store_true',
                        default=False, required=False)
    parser.add_argument(
        '-f', '--file', help='File containing XML or JSON', required=False)
    args = parser.parse_args()

    if not args.file and not args.stdin:
        print('ERROR: You must specify at least -s or -f')
        print('')
        parser.print_help()
        sys.exit(1)

    if args.stdin:
        inputStr = sys.stdin.read()
        inputFileH = StringIO.StringIO(inputStr)

    if args.file:
        with file(args.file, 'r') as inputFileH:
            inputStr = inputFileH.read()
            inputFileH = StringIO.StringIO(inputStr)

    format = isXMLorJSON(inputStr)

    if format == 'xml':
        tree = ET.ElementTree(ET.fromstring(inputStr))
        print converter().recurseXMLTree(tree.getroot())
    elif format == 'json':
        jsondict = json.loads(inputStr)
        print converter().recurseJSONDict(jsondict)
    else:
        raise IOError(
            'Unsupported format passed as input. Please check that input is' +
            ' formatted correctly in JSON or XML syntax')
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
