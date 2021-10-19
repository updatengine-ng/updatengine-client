###############################################################################
# UpdatEngine - Software Packages Deployment and Administration tool          #
#                                                                             #
# Copyright (C) Yves Guimard - yves.guimard@gmail.com                         #
#                                                                             #
# This program is free software; you can redistribute it and/or               #
# modify it under the terms of the GNU General Public License                 #
# as published by the Free Software Foundation; either version 2              #
# of the License, or (at your option) any later version.                      #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program; if not, write to the Free Software                 #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,                  #
# MA  02110-1301, USA.                                                        #
###############################################################################

import platform
import subprocess
import os
import re
from winreg import *
import hashlib
import sys
from lxml import etree
import time
import ueconst
import wmi


class ueinventory(object):
    xml = None
    wmi_conn = wmi.WMI()

    @staticmethod
    def build_inventory():
        self = ueinventory()
        hostname = self.get_hostname()
        serial = self.get_serial()
        manufacturer = self.get_manufacturer()
        product = self.get_product()
        uuid = self.get_uuid()
        domain = self.get_domain()
        language = self.get_language()
        chassistype = self.get_chassistype()
        osdata = self.format_oslist(self.get_oslist())
        ossum =  str(hashlib.md5(osdata.encode('utf-8')).hexdigest())
        softwaredata = self.format_softlist(self.get_softwarelist())
        softsum = str(hashlib.md5(softwaredata.encode('utf-8')).hexdigest())
        netdata = self.format_netlist(self.get_netlist())
        netsum =  str(hashlib.md5(netdata.encode('utf-8')).hexdigest())
        username = self.get_username()

        # Abort build_inventory if inventory presents too many errors
        if serial == manufacturer == product == domain == uuid == username == 'Unknown':
            raise Exception('Too many detection error: build_inventory aborted')

        data = \
            '<Inventory>' \
            '<ClientVersion>' + ueconst.UE_CLIENT_VERSION + '</ClientVersion>' \
            '<Hostname>' + hostname + '</Hostname>' \
            '<SerialNumber>' + serial + '</SerialNumber>' \
            '<Manufacturer>' + manufacturer + '</Manufacturer>' \
            '<Uuid>' + uuid + '</Uuid>' \
            '<UserName>' + username + '</UserName>' \
            '<Domain>' + domain + '</Domain>' \
            '<Language>' + language + '</Language>' \
            '<Product>' + product + '</Product>' \
            '<Chassistype>' + chassistype + '</Chassistype>' \
            '<Ossum>' + ossum + '</Ossum>' \
            '<Softsum>' + softsum + '</Softsum>' \
            '<Netsum>' + netsum + '</Netsum>' \
            + osdata \
            + softwaredata \
            + netdata + \
            '</Inventory>'
        return (data, softsum)

    @staticmethod
    def build_extended_inventory(xml):
        self = ueinventory()
        self.xml = xml

        serial = self.get_serial()
        hostname = self.get_hostname()
        extendeddata = self.get_extendeddata()
        if not extendeddata:
            return ''

        data = \
            '<Extended>' \
            '<ClientVersion>' + ueconst.UE_CLIENT_VERSION + '</ClientVersion>' \
            '<Hostname>' + hostname + '</Hostname>' \
            '<SerialNumber>' + serial + '</SerialNumber>' \
            + extendeddata + \
            '</Extended>'
        return (data)

    def get_hostname(self):
        try:
            return self.wmi_conn.Win32_ComputerSystem()[0].Caption.strip()
        except:
            return 'Unkown'

    def get_serial(self):
        try:
            return self.wmi_conn.Win32_BIOS()[0].SerialNumber.strip()
        except:
            return 'Unknown'

    def get_manufacturer(self):
        try:
            return self.wmi_conn.Win32_ComputerSystem()[0].Manufacturer.strip()
        except:
            return 'Unknown'

    def get_uuid(self):
        try:
            return self.wmi_conn.Win32_ComputerSystemProduct()[0].UUID.strip()
        except:
            return 'Unknown'

    def get_username(self):
        try:
            return self.wmi_conn.Win32_ComputerSystem()[0].UserName.split('\\')[1].strip()
        except:
            return 'Unknown'

    def get_domain(self):
        try:
            return self.wmi_conn.Win32_ComputerSystem()[0].Domain.strip()
        except:
            return 'Unknown'

    def get_language(self):
        import locale
        try:
            return locale.getdefaultlocale()[0].strip()
        except:
            return 'Unknown'

    def get_product(self):
        try:
            return self.wmi_conn.Win32_ComputerSystem()[0].Model.strip()
        except:
            return 'Unknown'

    def get_chassistype(self):
        chassis = ('Other','Unknown','Desktop','Low Profile Desktop','Pizza Box','Mini Tower',\
            'Tower','Portable','Laptop','Notebook','Hand Held','Docking Station','All in One',\
            'Sub Notebook','Space-Saving','Lunch Box','Main System Chassis','Expansion Chassis',\
            'Sub Chassis',' Bus Expansion Chassis','Peripheral Chassis','Storage Chassis',\
            'Rack Mount Chassis','Sealed-Case PC',\
            'Multi-system chassis', 'Compact PCI', 'Advanced TCA','Blade','Blade Enclosure',\
            'Tablet','Convertible','Detachable','IoT Gateway','Embedded PC','Mini PC','Stick PC')
        try:
            chassisnumber = int(self.wmi_conn.Win32_SystemEnclosure()[0].ChassisTypes[0])
            return chassis[chassisnumber-1]
        except:
            return 'Detection error'

    def get_softwarelist(self):
        def get_softwarelist_from_registry(hive, flag):
            try:
                aReg = ConnectRegistry(None, hive)
                aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",0, KEY_READ | flag)
                count_subkey = QueryInfoKey(aKey)[0]
                software_list = set()
                for i in range(count_subkey):
                    software = {}
                    try:
                        asubkey_name = EnumKey(aKey, i)
                        asubkey = OpenKey(aKey, asubkey_name)
                        software['name'] = QueryValueEx(asubkey, "DisplayName")[0]
                        try:
                            software['version'] = QueryValueEx(asubkey, "DisplayVersion")[0]
                        except:
                            software['version'] = 'undefined'
                        try:
                            software['uninstallstring'] = QueryValueEx(asubkey, "UninstallString")[0]
                        except:
                            software['uninstallstring'] = 'undefined'
                        software_list.add(software['name'] + ',;,' + software['version'] + ',;,' + software['uninstallstring'])
                    except:
                        continue
                return software_list
            except:
                return set()

        software_list = list(set().union(\
            get_softwarelist_from_registry(HKEY_LOCAL_MACHINE, KEY_WOW64_32KEY),\
            get_softwarelist_from_registry(HKEY_LOCAL_MACHINE, KEY_WOW64_64KEY),\
            get_softwarelist_from_registry(HKEY_CURRENT_USER, 0)
            ))
        return software_list

    def format_softlist(self, slist):
        sdata = ''
        for s in slist:
            s = self.encodeXMLText(s)
            line = s.split(',;,')
            if len(line) == 3:
                sdata += \
                    '<Software>' \
                    '<Name>' + line[0].strip() + '</Name>' \
                    '<Version>' + line[1].strip() + '</Version>' \
                    '<Uninstall>' + line[2].strip() + '</Uninstall>' \
                    '</Software>'
        return sdata

    def encodeXMLText(self,text):
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text

    def get_netlist(self):
        netlist = list()
        try:
            for q in self.wmi_conn.Win32_NetworkAdapterConfiguration(['IPAddress', 'IPSubnet', 'MACAddress', 'IPEnabled'], IPEnabled=1):
                ip = q.IPAddress[0]
                mask = q.IPSubnet[0]
                mac = q.MACAddress
                netlist.append(ip + ',' + mask + ',' + mac)
        except:
            print('Error when building netlist')
        return netlist

    def format_netlist(self, netlist):
        ndata = ''
        for n in netlist:
            line = n.split(',')
            if len(line) == 3:
                ndata += \
                    '<Network>' \
                    '<Ip>' + line[0].strip() + '</Ip>' \
                    '<Mask>' + line[1].strip() + '</Mask>' \
                    '<Mac>' + line[2].strip() + '</Mac>' \
                    '</Network>'
        return ndata

    def get_oslist(self):
        oslist = list()
        try:
            for q in self.wmi_conn.Win32_OperatingSystem():
                name = q.Caption
                csdversion = q.CSDVersion
                arch = q.OSArchitecture
                versionbuild = q.Version
                systemdrive = q.SystemDrive
            if csdversion:
                version = versionbuild + ' - ' + csdversion
            else:
                version = versionbuild
            oslist.append(name + ',' + version + ',' + arch + ',' + systemdrive)
        except:
               oslist = ('Unknown, Unknown, Unknown, Unknown')
        return oslist

    def format_oslist(self, oslist):
        osdata = ''
        for o in oslist:
            line = o.split(',')
            if len(line) == 4:
                osdata += \
                    '<Osdistribution>' \
                    '<Name>' + line[0].strip() + '</Name>' \
                    '<Version>' + line[1].strip() + '</Version>' \
                    '<Arch>' + line[2].strip() + '</Arch>' \
                    '<Systemdrive>' + line[3].strip() + '</Systemdrive>' \
                    '</Osdistribution>'
        return osdata

    def sha256_checksum(self, filename, block_size=65536):
        sha256 = hashlib.sha256()
        with open(filename, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()

    def get_extendeddata(self):
        root = etree.fromstring(self.xml)  # xml is a valid_response() then no Exception
        handling = list()
        for pack in root.findall('Extended'):
            for path in pack.findall('File'):
                extdata = '<File>'
                extdata += '<Name>' + path.text + '</Name>'
                if os.path.isfile(path.text):
                    extdata += '<Status>True</Status>'
                else:
                    extdata += '<Status>False</Status>'
                extdata += '</File>'
                handling.append(extdata)
            for path in pack.findall('Dir'):
                extdata = '<Dir>'
                extdata += '<Name>' + path.text + '</Name>'
                if os.path.isdir(path.text):
                    extdata += '<Status>True</Status>'
                else:
                    extdata += '<Status>False</Status>'
                extdata += '</Dir>'
                handling.append(extdata)
            for path in pack.findall('FileDir'):
                extdata = '<FileDir>'
                extdata += '<Name>' + path.text + '</Name>'
                if os.path.exists(path.text):
                    extdata += '<Status>True</Status>'
                else:
                    extdata += '<Status>False</Status>'
                extdata += '</FileDir>'
                handling.append(extdata)
            for path in pack.findall('Hash'):
                extdata = '<Hash>'
                extdata += '<Name>' + path.text + '</Name>'
                if os.path.isfile(path.text):
                    extdata += '<Status>' + self.sha256_checksum(path.text) + '</Status>'
                else:
                    extdata += '<Status>undefined</Status>'
                extdata += '</Hash>'
                handling.append(extdata)
            for path in pack.findall('ExitCode'):
                extdata = '<ExitCode>'
                extdata += '<Name>' + path.text + '</Name>'
                try:
                    p = subprocess.Popen(path.text, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    retcode = p.wait(timeout=30)
                    extdata += '<Status>' + str(retcode) + '</Status>'
                except:
                    extdata += '<Status>undefined</Status>'
                extdata += '</ExitCode>'
                handling.append(extdata)
        return ''.join(handling)


