###################################################################################
# UpdatEngine - Software Packages Deployment and Administration tool              #  
#                                                                                 #
# Copyright (C) Yves Guimard - yves.guimard@gmail.com                             #
#                                                                                 #
# This program is free software; you can redistribute it and/or                   #
# modify it under the terms of the GNU General Public License                     #
# as published by the Free Software Foundation; either version 2                  #
# of the License, or (at your option) any later version.                          #
#                                                                                 #
# This program is distributed in the hope that it will be useful,                 #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                  #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   #
# GNU General Public License for more details.                                    #
#                                                                                 #
# You should have received a copy of the GNU General Public License               #
# along with this program; if not, write to the Free Software                     #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA. #
###################################################################################

import os
import sys
import ssl
import urllib, urllib2
import urlparse
from lxml import etree

class uecommunication:

	def check_ssl(self, hostname, port, cafile_local):
    		if not os.path.isfile(cafile_local):
       		 print >> sys.stderr, "No cacert.pem found !"
   	 	try:
        		ssl.get_server_certificate((hostname, port), ca_certs=cafile_local)
    		except ssl.SSLError:
        		print >> sys.stderr, "SSL cert at %s:%d is invalid!" % (hostname, port)
        		raise 

	def printable(self, s):
		import string
		s = s.replace('&','&amp;')
		return filter(lambda x: x in string.printable, s)

	@staticmethod
	def send_xml(url,xml,action,options = None):
		self = uecommunication()
                try:
			xml = self.printable(xml)
			cookieHandler = urllib2.HTTPCookieProcessor()
			urlbits = urlparse.urlparse(url)
			if options.cert is not None:
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

			opener = urllib2.build_opener( urllib2.HTTPSHandler(), cookieHandler )
			urllib2.install_opener( opener )
			opener.open(url)
			cookie = None
			for cookie in cookieHandler.cookiejar:
				if cookie.name == 'csrftoken':
					csrf_cookie = cookie
					break
				if not cookie:
					raise IOError( "No csrf cookie found" )
			parameter = urllib.urlencode(dict(action=action,xml=xml,csrfmiddlewaretoken=csrf_cookie.value))
			req = urllib2.Request(url, parameter)
			req.add_header('Referer', url)
			response = urllib2.urlopen(req).read()
		except Exception as e:
			return str(e)
                return response

	@staticmethod
	def send_inventory(url, xml, options = None):
		self = uecommunication()
		response = self.send_xml(url,xml,'inventory', options)
		try:
			root  = etree.fromstring(response)	
		except:
			return (0,'Error while reading response after inventory\n\
			Response:\n'+response+'\n')
		if root.find('Import') is not None:
			if root.find('Import').text == 'Import ok':
				return (1,response)	
			else:
				return (0,response)
		else:
				return (0,response)

