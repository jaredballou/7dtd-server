#!/usr/bin/env python
import argparse
import random
import string
import sys
from xml.etree.ElementTree import parse, XML, SubElement, Element, tostring
import xml.etree.cElementTree as ET

"""
7 Days to Die Serverconfig.xml Tool
(c) 2017, Jared Ballou <7dtd@jballou.com>

Allows my Docker scripts to view and modify server configuration file.

TODO:
[ ] Arguments for getting/setting values
[ ] Argument for random strings
[ ] Have a normal check that fails if passwords are weak or empty

"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--passwords', action='store_true', help='Set TelnetPassword and ControlPanelPassword to random values if blank or CHANGEME is detected. Display passwords regardless.')
    parser.add_argument('-g','--get', action='store_true', help='get value [default]', default=True)
    parser.add_argument('-s','--set', action='store_true', help='set value', default=False)
    parser.add_argument('-n','--name', help='name')
    parser.add_argument('-v','--value', help='value to set [default empty]')
    parser.add_argument('-r','--random', default=argparse.SUPPRESS, type=int, help='instead of value, set [name] to a random string this long')
    parser.add_argument('-i', '--infile', nargs='?', default="/steamcmd/7dtd/server_data/serverconfig.xml")
    parser.add_argument('-o', '--outfile', nargs='?', default="/steamcmd/7dtd/server_data/serverconfig.xml")
    parsed = parser.parse_args()
    args = vars(parsed)

    ss = ServerSettings(serverconfig_path=args['infile'])
    if args['passwords']:
        ss.do_passwords()
    if args['name']:
        if 'set' in args and args['set']:
            ss.set_value(name=args['name'], value=args['value'])
        else:
            print ss.get_value(name=args['name'])

def random_string(length=8, chars=None):
    if chars is None:
        chars = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

class ServerSettings(object):
    def __init__(self, serverconfig_path=None):
        self.serverconfig_path = serverconfig_path
        self.load_from_xml()

    def load_from_xml(self, xml_file=None):
        """
        Parse XML with ElementTree
        """
        if xml_file is None:
            xml_file = self.serverconfig_path
        self.tree = ET.ElementTree(file=xml_file)

    def save_to_file(self, xml_file=None):
        if xml_file is None:
            xml_file = self.serverconfig_path
        self.tree.write(xml_file)

    def set_value(self, name, value):
        self.tree.find('./property[@name="%s"]' % name).attrib['value'] = value
        ss.save_to_file()

    def get_value(self, name, default="", caption=False):
        value = self.tree.find('./property[@name="%s"]' % name).attrib['value']
        if value is None or value == "":
            value = default
        if caption:
            return "%s %s" % (name, value)
        else:
            return value

    def do_passwords(self):
        if self.get_value("TelnetPassword") in ["","CHANGEME"]:
            self.set_value(name="TelnetPassword", value=random_string(16))
        if self.get_value("ControlPanelPassword") in ["","CHANGEME"]:
            self.set_value(name="ControlPanelPassword", value=random_string(16))
        print self.get_value(name="TelnetPassword",caption=True)
        print self.get_value(name="ControlPanelPassword",caption=True)

if __name__ == "__main__":
    main()

