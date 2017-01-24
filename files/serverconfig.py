#!/usr/bin/env python
import random
import string
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
    ss = ServerSettings()
    ss.load_from_xml()
    if ss.get_prop("TelnetPassword") in ["","CHANGEME"]:
        ss.set_prop(name="TelnetPassword", value=random_string(16))
    if ss.get_prop("ControlPanelPassword") in ["","CHANGEME"]:
        ss.set_prop(name="ControlPanelPassword", value=random_string(16))
    ss.save_to_file()
	
def random_string(length=8, chars=None):
    if chars is None:
        chars = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

class ServerSettings(object):
    def __init__(self, serverconfig_path = "/steamcmd/7dtd/server_data/serverconfig.xml"):
        self.serverconfig_path = serverconfig_path

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

    def set_prop(self, name, value):
        self.tree.find('./property[@name="%s"]' % name).attrib['value'] = value

    def get_prop(self, name, default=""):
        value = self.tree.find('./property[@name="%s"]' % name).attrib['value']
        if value is None or value == "":
            value = default
        return value

if __name__ == "__main__":
    main()

