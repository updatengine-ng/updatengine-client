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

import ssl
import urllib.request
import urllib.parse
import urllib.error
import socket
from lxml import etree
from ueerrors import *
import ueconst


class uecommunication(object):
    socket.setdefaulttimeout(30)
    ssl_version = ssl.PROTOCOL_SSLv23
    ssl_context = ssl.SSLContext(ssl_version)

    def check_ssl(self, hostname, port, cafile_local):
        try:
            open(cafile_local, 'r')
        except:
            print('Error in check_ssl (open function)')
            raise
        try:
            ssl.get_server_certificate((hostname, port), ssl_version=self.ssl_version, ca_certs=cafile_local)
        except ssl.SSLError:
            print('Error in check_ssl (ssl.get_server_certificate function)')
            raise ssl.SSLError('SSL cert of Host:' + str(hostname) + ' Port:' + str(port) + ' is invalid')

    def printable(self, s):
        import string
        s = s.replace('&', '&amp;')
        return ''.join([ch for ch in s if ord(ch) > 31 or ord(ch) == 9])

    @staticmethod
    def send_xml(url, xml, action, options=None):
        self = uecommunication()
        xml = self.printable(xml)
        cookieHandler = urllib.request.HTTPCookieProcessor()
        try:
            urlbits = urllib.parse.urlparse(url)
        except Exception:
            print('Error in send_xml (urlparse.urlparse function)')
            raise
        if options.cert is not None:
            try:
                if urlbits.scheme == 'https':
                    if ':' in urlbits.netloc:
                        hostname, port = urlbits.netloc.split(':')
                    else:
                        hostname = urlbits.netloc
                    if urlbits.port is None:
                        port = 443
                    else:
                        port = urlbits.port
                    self.check_ssl(hostname, int(port), options.cert)
                    self.ssl_context.load_verify_locations(cafile=options.cert)
                    self.ssl_context.check_hostname = not options.nosslcn
            except:
                raise
        if options.noproxy is True:
            proxy_handler = urllib.request.ProxyHandler({})
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=self.ssl_context), cookieHandler, proxy_handler)
        else:
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=self.ssl_context), cookieHandler)
        urllib.request.install_opener(opener)

        try:
            opener.addheaders = [('User-Agent', 'UpdatEngine-client/'+ueconst.UE_CLIENT_VERSION)]
            opener.open(url)
        except IOError as e:
            if hasattr(e, 'reason'):
                print('error: Unable to connect to server. ' + str(e.reason))
            elif hasattr(e, 'code'):
                print('error: The request could not be satisfied. ' + str(e.code))
            raise
        except Exception:
            raise

        cookie = None
        for cookie in cookieHandler.cookiejar:
            if cookie.name == 'csrftoken':
                csrf_cookie = cookie
                break
        if cookie is None:
            raise IOError('No csrf cookie found')
        try:
            parameter = urllib.parse.urlencode(dict(action=action, xml=xml, csrfmiddlewaretoken=csrf_cookie.value)).encode("utf-8")
            req = urllib.request.Request(url, parameter)
            req.add_header('Referer', url)
            response = urllib.request.urlopen(req).read()
        except Exception:
            raise
        return response

    @staticmethod
    def printable_public_software(xml):
        try:
            root = etree.fromstring(xml)
        except:
            print(xml)
            print('Error in printable_public_software, bad xml format')
            raise

        for pack in root.findall('Package'):
            try:
                command = pack.find('Command').text
                command = command.replace('\n', ' && ')
                command = command.replace('&& download_no_restart', '')
                command = command.replace('&& section_end', '')  # for retro compatibility

                print('---- Package number: %s ----' % pack.find('Pid').text)
                print('Package: %s' % pack.find('Name').text)
                print('Command associated to package: %s' % command)
                print('Url used to download package files (if needed): %s' % pack.find('Url').text)
                print('----------------------------\n')
            except:
                pass

    @staticmethod
    def get_public_software_list(url, options=None, pack=None):
        self = uecommunication()
        cookieHandler = urllib.request.HTTPCookieProcessor()
        try:
            urlbits = urllib.parse.urlparse(url)
        except Exception:
            print('Error in get_softlist (urlparse.urlparse function)')
            raise
        if options.cert is not None:
            try:
                if urlbits.scheme == 'https':
                    if ':' in urlbits.netloc:
                        hostname, port = urlbits.netloc.split(':')
                    else:
                        hostname = urlbits.netloc
                    if urlbits.port is None:
                        port = 443
                    else:
                        port = urlbits.port
                    self.check_ssl(hostname, int(port), options.cert)
                    self.ssl_context.load_verify_locations(cafile=options.cert)
                    self.ssl_context.check_hostname = not options.nosslcn
            except:
                raise
        if options.noproxy is True:
            proxy_handler = urllib.request.ProxyHandler({})
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=self.ssl_context), cookieHandler, proxy_handler)
        else:
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=self.ssl_context), cookieHandler)
        urllib.request.install_opener(opener)

        try:
            opener.addheaders = [('User-Agent', 'UpdatEngine-client/'+ueconst.UE_CLIENT_VERSION)]
            opener.open(url)
        except IOError as e:
            if hasattr(e, 'reason'):
                print('error: Unable to connect to server. ' + str(e.reason))
            elif hasattr(e, 'code'):
                print('error: The request could not be satisfied. ' + str(e.code))
            raise
        except Exception:
            raise

        cookie = None
        for cookie in cookieHandler.cookiejar:
            if cookie.name == 'csrftoken':
                csrf_cookie = cookie
                break
        if cookie is None:
            raise IOError('No csrf cookie found')
        try:
            if pack is not None:
                parameter = urllib.parse.urlencode(dict(action='softlist', pack=pack, csrfmiddlewaretoken=csrf_cookie.value)).encode("utf-8")
            else:
                parameter = urllib.parse.urlencode(dict(action='softlist', csrfmiddlewaretoken=csrf_cookie.value)).encode("utf-8")
            req = urllib.request.Request(url, parameter)
            req.add_header('Referer', url)
            response = urllib.request.urlopen(req).read()
        except Exception:
            raise
        return response

    def valid_response(self, response):
        '''Valid xml response after an inventory'''
        try:
            root = etree.fromstring(response)
        except Exception:
            raise UeReadResponse(response)

        if root.find('Import') is not None:
            if root.find('Import').text == 'Import ok':
                return response
            else:
                raise UeImportError(response)
        else:
            raise UeResponseError(response)

    @staticmethod
    def print_warninfo(response):
        '''Print server informations and warnings'''
        try:
            root = etree.fromstring(response)
        except Exception:
            raise UeReadResponse(response)

        for child in root.findall('Info'):
            print('information: ' + child.text)
        for child in root.findall('Warning'):
            print('information: ' + child.text)

    @staticmethod
    def send_inventory(url, xml, options=None):
        '''Send an inventory to an updatengine server'''
        self = uecommunication()
        try:
            response = self.send_xml(url, xml, 'inventory', options)
        except Exception:
            raise
        else:
            return self.valid_response(response)

    @staticmethod
    def send_extended_inventory(url, xml, options=None):
        '''Send an inventory to an updatengine server'''
        self = uecommunication()
        try:
            response = self.send_xml(url, xml, 'extended', options)
        except Exception:
            raise
        else:
            return self.valid_response(response)
