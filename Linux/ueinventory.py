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
import dmidecode
import hashlib
import psutil
from lxml import etree
import time
import ueconst


class ueinventory(object):
    xml = None

    @staticmethod
    def build_inventory():
        self = ueinventory()
        dmixml = dmidecode.dmidecodeXML()
        dmixml.SetResultType(dmidecode.DMIXML_DOC)
        xmldoc = dmixml.QuerySection('all')
        dmixp = xmldoc.xpathNewContext()
        manufacturer = self.get_manufacturer(dmixp).strip()
        product = self.get_product(dmixp).strip()
        serial = self.get_serial(dmixp).strip()
        uuid = self.get_uuid(dmixp).strip()
        domain = self.get_domain().strip()
        language = self.get_language().strip()
        chassistype = self.get_chassistype(dmixp).strip()
        hostname = self.get_hostname().strip()
        osdata = self.format_oslist(self.get_oslist())
        ossum = str(hashlib.md5(osdata).hexdigest())
        softwaredata = self.format_softlist(self.get_softwarelist())
        softsum = str(hashlib.md5(softwaredata).hexdigest())
        netdata = self.format_netlist(self.get_netlist())
        netsum = str(hashlib.md5(netdata).hexdigest())
        username = self.get_username().strip()

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

        dmixml = dmidecode.dmidecodeXML()
        dmixml.SetResultType(dmidecode.DMIXML_DOC)
        xmldoc = dmixml.QuerySection('all')
        dmixp = xmldoc.xpathNewContext()
        serial = self.get_serial(dmixp).strip()
        hostname = self.get_hostname().strip()
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

    def checkdmi(self, dmixp, tag):
        try:
            return dmixp.xpathEval(tag)[0].get_content()
        except:
            return 'Unknown'

    def get_hostname(self):
        try:
            return platform.node()
        except:
            return 'Unknown'

    def get_serial(self, dmixp):
        try:
            return self.checkdmi(dmixp, '/dmidecode/SystemInfo/SerialNumber')
        except:
            return 'Unknown'

    def get_manufacturer(self, dmixp):
        try:
            return self.checkdmi(dmixp, '/dmidecode/SystemInfo/Manufacturer')
        except:
            return'Unknown'

    def get_uuid(self, dmixp):
        try:
            return self.checkdmi(dmixp, '/dmidecode/SystemInfo/SystemUUID')
        except:
            return 'Unknown'

    def get_username(self):
        try:
            return psutil.users()[0].name
        except:
            return 'undefined'

    def get_domain(self):
        try:
            import socket
            fqdn = socket.getfqdn
            hostname = socket.gethostname()
            domain = fqdn.replace(hostname, '')
            if domain != '':
                return domain
            else:
                return 'undefined'
        except:
            return 'Unknown'

    def get_language(self):
        import locale
        try:
            return locale.getdefaultlocale()[0]
        except:
            return 'Unknown'

    def get_product(self, dmixp):
        try:
            return self.checkdmi(dmixp, '/dmidecode/SystemInfo/ProductName')
        except:
            return 'Unknown'

    def get_chassistype(self, dmixp):
        try:
            return self.checkdmi(dmixp, '/dmidecode/ChassisInfo/ChassisType')
        except:
            return 'Unknown'

    def get_softwarelist(self):
        try:
            cmd = 'rpm -qa --queryformat "%{NAME},%{VERSION}\n"'
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            streamdata = p.communicate()[0]
            # Check returncode and streamdata (because rpm can be installed on
            # a debian based dstrib and dpkg on a redhat!)
            if p.returncode or not streamdata:
                cmd = 'dpkg -l |awk \'/^ii/ {print $2", "$3}\''
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                streamdata = p.communicate()[0]
            l = list()
            for s in streamdata.splitlines():
                l.append(s.encode('utf-8'))
            return l
        except:
            return []

    def format_softlist(self, slist):
        sdata = ''
        for s in slist:
            line = s.split(', ')
            if len(line) == 2:
                sdata += \
                    '<Software>' \
                    '<Name>'+line[0].strip()+'</Name>' \
                    '<Version>'+line[1].strip()+'</Version>' \
                    '<Uninstall>Defined only for Windows hosts</Uninstall>' \
                    '</Software>'
        return sdata

    def get_netlist(self):
        import netifaces
        netnamelist = netifaces.interfaces()
        netlist = list()
        for net in netnamelist:
            try:
                ip = netifaces.ifaddresses(net)[netifaces.AF_INET][0]['addr']
                mask = netifaces.ifaddresses(net)[netifaces.AF_INET][0]['netmask']
                try:
                    mac = netifaces.ifaddresses(net)[netifaces.AF_LINK][0]['addr']
                except:
                    mac = '00:00:00:00:00:00'
                netlist.append(ip + ', ' + mask + ', ' + mac)
            except:
                pass
        return netlist

    def format_netlist(self, netlist):
        ndata = ''
        for n in netlist:
            line = n.split(', ')
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
        ostuple = platform.linux_distribution()
        name = ostuple[0]
        version = ostuple[1] + ' - ' + ostuple[2]
        arch = os.uname()[4]
        systemdrive = '-'
        oslist.append(name + ', ' + version + ', ' + arch + ', ' + systemdrive)
        return oslist

    def format_oslist(self, oslist):
        osdata = ''
        for o in oslist:
            line = o.split(', ')
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

    def process_timeout(self, proc, timeout):
        while True:
            status = proc.poll()
            if status is not None:
                return status
            if timeout <= 0:
                if status is None:
                    proc.kill()
                return None
                break
            time.sleep(0.5)
            timeout -= 0.5

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
                p = subprocess.Popen(path.text, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                if self.process_timeout(p, 30) is None:
                    extdata += '<Status>undefined</Status>'
                else:
                    extdata += '<Status>' + str(p.returncode) + '</Status>'
                extdata += '</ExitCode>'
                handling.append(extdata)
        return ''.join(handling)
