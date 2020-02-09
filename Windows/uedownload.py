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

from lxml import etree
from uecommunication import uecommunication
import os
import tempfile
import subprocess
from ueinventory import ueinventory
import hashlib
import time
import logging
import shutil
import sys
import re


class uedownload(object):
    urlinv = None
    xml = None
    options = None
    mid = None
    pid = None
    max_download_action = 5  # Parameter to avoid infinite loops
    default_timeout = 1800
    timeout = default_timeout

    def download_pack(self, url, pack, options):
        packxml = uecommunication.get_public_software_list(url, options, pack)
        try:
            root = etree.fromstring(packxml)
        except:
            print(self.xml)
            print('Error reading xml response in download_action')
            logging.exception('Error reading xml response in download_action')
            raise
        try:
            if not root.findall('Package'):
                print('Package ' + str(pack) + ' not found')
                logging.info('Package ' + str(pack) + ' not found')

            for pack in root.findall('Package'):
                try:
                    self.download_print_time()
                    print('Package: ' + pack.find('Name').text)
                    logging.info('Package: ' + pack.find('Name').text)
                    self.pid = pack.find('Pid').text
                    command = pack.find('Command').text
                    option_timeout = 'install_timeout_'
                    self.timeout = self.default_timeout
                    if command.find(option_timeout) != -1:
                        match = re.search(option_timeout+'(.+?)(\r?\n|$)', command)
                        try:
                            option_timeout += match.group(1)
                            command_value = int(match.group(1))
                            if command_value > 0:
                                self.timeout = command_value
                        except:
                            logmsg = 'Ignoring invalid option \'' + option_timeout + '\''
                            print(logmsg)
                            logging.warning(logmsg)
                    command = re.sub("\n\s*\n*", " && ", command)  # Remove blank lines and convert \n to &&
                    command = command.replace(' && download_no_restart', '')
                    command = command.replace(' && no_break_on_error', '')
                    command = command.replace(' && section_end', '')  # for retro compatibility
                    command = command.replace(' && ' + option_timeout, '')
                    url = pack.find('Url').text
                    packagesum = pack.find('Packagesum').text
                except:
                    print('Error in package xml format')
                    logging.exception('Error in package xml format')
                    raise

                logging.info('Ready to download and execute (manually)')

                if packagesum != 'nofile':
                    try:
                        tmpdir = tempfile.gettempdir()+'/updatengine/'
                        if not os.path.exists(tmpdir):
                            os.makedirs(tmpdir)
                        file_name = tmpdir+url.split('/')[-1]
                        self.download_tmp(url, file_name, packagesum)
                    except:
                        self.download_print_time()
                        print('Error when downloading: ' + file_name)
                        logging.exception('Error when downloading: ' + file_name)
                        raise
                    else:
                        print('Install in progress')
                        logging.info('Install in progress')

                        try:
                            os.chdir(tmpdir)
                            p = subprocess.Popen(command, stderr=subprocess.PIPE, shell=True)
                            retcode = p.wait(timeout=self.timeout)
                            if retcode != 0:
                                raise Exception(retcode)
                        except subprocess.TimeoutExpired:
                            p.kill()
                            err = "Timeout expired"
                            print('Error launching action: ' + err)
                            if sys.platform == 'win32':
                                logging.exception('Error launching action: ' + err.decode(sys.stdout.encoding).encode('iso-8859-1'))
                            else:
                                logging.exception('Error launching action: ' + err)
                            if no_break_on_error is True:
                                status_msg = None
                            else:
                                raise
                        except Exception as e:
                            err = [s.strip().decode('utf-8') for s in p.stderr.readlines()]
                            err = ' '.join(err)
                            if len(err):
                                err = err[:450] + ('...' if len(err) > 450 else '') + " | Exit code " + str(e)
                            else:
                                err = "Exit code " + str(e)
                            print('Error launching action: ' + str(err))
                            if sys.platform == 'win32':
                                logging.exception('Error launching action: ' + err.decode(sys.stdout.encoding).encode('iso-8859-1'))
                            else:
                                logging.exception('Error launching action: ' + err)
                            if no_break_on_error is True:
                                status_msg = None
                            else:
                                raise
                        finally:
                            # come back to gettemdir to remove updatengine directory
                            try:
                                os.chdir(tempfile.gettempdir())
                                shutil.rmtree(tmpdir)
                            except:
                                print('Can\'t delete temp file')
                                logging.info('Can\'t delete temp file')
                else:
                    print('Install in progress')
                    logging.info('Install in progress')

                    try:
                        p = subprocess.Popen(command, stderr=subprocess.PIPE, shell=True)
                        retcode = p.wait(timeout=self.timeout)
                        if retcode != 0:
                            raise Exception(retcode)
                    except subprocess.TimeoutExpired:
                        p.kill()
                        err = "Timeout expired"
                        print('Error launching action: ' + err)
                        if sys.platform == 'win32':
                            logging.exception('Error launching action: ' + err.decode(sys.stdout.encoding).encode('iso-8859-1'))
                        else:
                            logging.exception('Error launching action: ' + err)
                        if no_break_on_error is True:
                            status_msg = None
                        else:
                            raise
                    except Exception as e:
                        err = [s.strip().decode('utf-8') for s in p.stderr.readlines()]
                        err = ' '.join(err)
                        if len(err):
                            err = err[:450] + ('...' if len(err) > 450 else '') + " | Exit code " + str(e)
                        else:
                            err = "Exit code " + str(e)
                        print('Error launching action: ' + str(err))
                        if sys.platform == 'win32':
                            logging.exception('Error launching action: ' + err.decode(sys.stdout.encoding).encode('iso-8859-1'))
                        else:
                            logging.exception('Error launching action: ' + err)
                        if no_break_on_error is True:
                            status_msg = None
                        else:
                            raise

                self.download_print_time()
                print('Operation completed')
                logging.info('Operation completed')
        except:
            print('Error detected when launching download_action')
            logging.info('Error detected when launching download_action')
            raise

    def download_action(self, url, xml, options=None):
        self.urlinv = url
        self.xml = xml
        self.options = options
        try:
            root = etree.fromstring(self.xml)
        except:
            print(self.xml)
            print('Error reading xml response in download_action')
            logging.info('Error reading xml response in download_action')
            raise
        # download_launch is used to know if a download action append
        download_launch = None
        self.max_download_action -= 1
        try:
            # Install packages
            for pack in root.findall('Package'):
                try:
                    command = pack.find('Command').text
                    if command.find('download_no_restart') != -1 and self.max_download_action < 4:
                        continue
                    self.download_print_time()
                    print('Package: ' + pack.find('Name').text)
                    logging.info('Package: ' + pack.find('Name').text)
                    self.mid = pack.find('Id').text
                    self.pid = pack.find('Pid').text
                    no_break_on_error = None
                    if command.find('no_break_on_error') != -1:
                        no_break_on_error = True
                    option_timeout = 'install_timeout_'
                    self.timeout = self.default_timeout
                    if command.find(option_timeout) != -1:
                        match = re.search(option_timeout+'(.+?)(\r?\n|$)', command)
                        try:
                            option_timeout += match.group(1)
                            command_value = int(match.group(1))
                            if command_value > 0:
                                self.timeout = command_value
                        except:
                            logmsg = 'Ignoring invalid option \'' + option_timeout + '\''
                            print(logmsg)
                            self.download_send_status(logmsg)
                            logging.warning(logmsg)
                    command = re.sub("\n\s*\n*", " && ", command)  # Remove blank lines and convert \n to &&
                    command = command.replace(' && download_no_restart', '')
                    command = command.replace(' && no_break_on_error', '')
                    command = command.replace(' && section_end', '')  # for retro compatibility
                    command = command.replace(' && ' + option_timeout, '')
                    url = pack.find('Url').text
                    packagesum = pack.find('Packagesum').text
                    download_launch = True
                    status_msg = True
                except:
                    print('Error in package xml format')
                    logging.exception('Error in package xml format')
                    raise

                self.download_send_status('Ready to download and execute')
                logging.info('Ready to download and execute')

                if packagesum != 'nofile':
                    try:
                        tmpdir = tempfile.gettempdir()+'/updatengine/'
                        if not os.path.exists(tmpdir):
                            os.makedirs(tmpdir)
                        file_name = tmpdir+url.split('/')[-1]
                        self.download_tmp(url, file_name, packagesum)
                    except:
                        self.download_print_time()
                        print('Error when downloading: ' + file_name)
                        self.download_send_status('Error downloading file ' + file_name)
                        logging.exception('Error when downloading: ' + file_name)
                        raise
                    else:
                        print('Install in progress')
                        logging.info('Install in progress')
                        self.download_send_status('Install in progress')

                        try:
                            os.chdir(tmpdir)
                            p = subprocess.Popen(command, stderr=subprocess.PIPE, shell=True)
                            retcode = p.wait(timeout=self.timeout)
                            if retcode != 0:
                                raise Exception(retcode)
                        except subprocess.TimeoutExpired:
                            p.kill()
                            err = "Timeout expired"
                            print('Error launching action: ' + err)
                            if sys.platform == 'win32':
                                self.download_send_status('Error launching action: ' + err.decode(sys.stdout.encoding).encode('utf-8'))
                                logging.exception('Error launching action: ' + err.decode(sys.stdout.encoding).encode('iso-8859-1'))
                            else:
                                self.download_send_status('Error launching action: ' + err)
                                logging.exception('Error launching action: ' + err)
                            if no_break_on_error is True:
                                status_msg = None
                            else:
                                raise
                        except Exception as e:
                            err = [s.strip().decode('utf-8') for s in p.stderr.readlines()]
                            err = ' '.join(err)
                            if len(err):
                                err = err[:450] + ('...' if len(err) > 450 else '') + " | Exit code " + str(e)
                            else:
                                err = "Exit code " + str(e)
                            print('Error launching action: ' + str(err))
                            if sys.platform == 'win32':
                                self.download_send_status('Error launching action: ' + err.decode(sys.stdout.encoding).encode('utf-8'))
                                logging.exception('Error launching action: ' + err.decode(sys.stdout.encoding).encode('iso-8859-1'))
                            else:
                                self.download_send_status('Error launching action: ' + err)
                                logging.exception('Error launching action: ' + err)
                            if no_break_on_error is True:
                                status_msg = None
                            else:
                                raise
                        finally:
                            # come back to gettempdir to remove updatengine directory
                            try:
                                os.chdir(tempfile.gettempdir())
                                shutil.rmtree(tmpdir)
                            except:
                                print('Can\'t delete temp file')
                                logging.info('Can\'t delete temp file')
                else:
                    print('Install in progress')
                    logging.info('Install in progress')
                    self.download_send_status('Install in progress')

                    try:
                        p = subprocess.Popen(command, stderr=subprocess.PIPE, shell=True)
                        retcode = p.wait(timeout=self.timeout)
                        if retcode != 0:
                            raise Exception(retcode)
                    except subprocess.TimeoutExpired:
                        p.kill()
                        err = "Timeout expired"
                        print('Error launching action: ' + err)
                        if sys.platform == 'win32':
                            self.download_send_status('Error launching action: ' + err.decode(sys.stdout.encoding).encode('utf-8'))
                            logging.exception('Error launching action: ' + err.decode(sys.stdout.encoding).encode('iso-8859-1'))
                        else:
                            self.download_send_status('Error launching action: ' + err)
                            logging.exception('Error launching action: ' + err)
                        if no_break_on_error is True:
                            status_msg = None
                        else:
                            raise
                    except Exception as e:
                        err = [s.strip().decode('utf-8') for s in p.stderr.readlines()]
                        err = ' '.join(err)
                        if len(err):
                            err = err[:450] + ('...' if len(err) > 450 else '') + " | Exit code " + str(e)
                        else:
                            err = "Exit code " + str(e)
                        print('Error launching action: ' + str(err))
                        if sys.platform == 'win32':
                            self.download_send_status('Error launching action: ' + err.decode(sys.stdout.encoding).encode('utf-8'))
                            logging.exception('Error launching action: ' + err.decode(sys.stdout.encoding).encode('iso-8859-1'))
                        else:
                            self.download_send_status('Error launching action: ' + err)
                            logging.exception('Error launching action: ' + err)
                        if no_break_on_error is True:
                            status_msg = None
                        else:
                            raise

                if status_msg is True:
                    self.download_print_time()
                    print('Operation completed')
                    self.download_send_status('Operation completed')
                    logging.info('Operation completed')

            if not root.findall('Package'):
                print('No package to install')
                logging.info('No package to install')
        except:
            print('Error detected when launching download_action')
            logging.exception('Error detected when lauching download_action')
            raise
        else:
            # Loop download action
            if download_launch:
                try:
                    self.download_print_time()
                    print('End of download and install')
                    time.sleep(5)
                    inventory = ueinventory.build_inventory()
                    response_inventory = uecommunication.send_inventory(self.urlinv, inventory[0], options)
                    extended_inventory = ueinventory.build_extended_inventory(response_inventory)
                    if extended_inventory:
                        response_inventory = uecommunication.send_extended_inventory(self.urlinv, extended_inventory, options)
                    if self.max_download_action > 0:
                        self.download_action(self.urlinv, response_inventory, options)
                except:
                    print('Error in loop download action')
                    logging.exception('Error in loop download action')

    def download_send_status(self, message):
        try:
            if not self.mid:
                self.mid = '0'
            header = '<Packstatus><Mid>' + self.mid + '</Mid><Pid>' + self.pid + '</Pid><Status>'
            tail = '</Status></Packstatus>'
            full_message = header + message + tail
            uecommunication.send_xml(self.urlinv, full_message, 'status', self.options)
        except:
            print('Error uecommunication.send_xml / status')
            logging.exception('Error uecommunication.send_xml / status')
            raise

    def download_print_time(self):
        localtime = time.localtime()
        print(time.strftime('%Y-%m-%d-%H:%M:%S', localtime))

    def download_tmp(self, url, file_name, packagesum):
        from zipfile import ZipFile
        try:
            import urllib.request, urllib.error, urllib.parse
            if packagesum is None:
                return 1
            u = urllib.request.urlopen(url)
            f = open(file_name, 'wb')
            meta = u.info()
            file_size = int(meta.get('Content-Length'))
            print('Downloading: %s Bytes: %s' % (file_name, file_size))

            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                f.write(buffer)
                status = r'%10d  [%3.2f%%]' % (file_size_dl, file_size_dl * 100. / file_size)
                status = '\r' + status
                sys.stdout.write(status)

            f.close()
            if self.md5_for_file(file_name) == packagesum:
                print('')
                if str(file_name).lower().endswith('.zip'):
                    ZipFile(file_name).extractall(tempfile.gettempdir() + '/updatengine/')
                return 1
            else:
                print('md5 don\'t match: ' + self.md5_for_file(file_name) + ' --- ' + packagesum)
                logging.debug('md5 don\'t match: ' + self.md5_for_file(file_name) + ' --- ' + packagesum)
                raise
        except:
            logging.exception('Error download_tmp')
            raise

    def md5_for_file(self, file_name, block_size=2**20):
        try:
            f = open(file_name, 'rb')
            md5 = hashlib.md5()
            while True:
                data = f.read(block_size)
                if not data:
                    break
                md5.update(data)
            f.close()
        except:
            raise
        return md5.hexdigest()
