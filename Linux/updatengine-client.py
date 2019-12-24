#!/usr/bin/env python

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

import sys
import os
import argparse
import time
import logging
from ueinventory import ueinventory
from uecommunication import uecommunication
from uedownload import uedownload
from xml.dom.minidom import parseString as parseXML
import ueconst


class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        sys.stderr.write('Try with \'--help\' for more information\n')  # or self.print_help()
        sys.exit(1)


def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


def wait(minutes, passphrase):
    import socket
    from datetime import datetime, timedelta
    socket.setdefaulttimeout(minutes*60)
    Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    Host = ''
    Port = 2010
    Sock.bind((Host, Port))
    Sock.listen(3)
    limit = datetime.now() + timedelta(minutes=minutes)
    print 'wait for connexion with passphrase %s or %s' % (passphrase, limit)
    try:
        client, adresse = Sock.accept()
        while datetime.now() < limit:
            RequeteDuClient = client.recv(255)
            print RequeteDuClient
            if RequeteDuClient == passphrase:
                client.close()
                Sock.close()
                return

    except socket.timeout:
        Sock.close()
    return


def main():
    # Check if running as administrator
    if not isAdmin():
        sys.exit('error: Administrator permission required')

    # Define options
    parser = ArgParser(
        description='UpdatEngine client allow computer and server to be '
        'inventoried automatically on an UpdatEngine server and to deploy applications')
    parser.add_argument(
        '-s', '--server', dest='server',
        type=str, help='UpdatEngine server URL')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-i', '--inventory', dest='inventory',
        action='store_true', help='to inventory the host')
    parser.add_argument(
        '-n', '--noproxy', dest='noproxy',
        action='store_true', help='do not use any proxy')
    parser.add_argument(
        '-m', '--minutes', dest='minute',
        type=int, help='minute between each inventory')
    parser.add_argument(
        '-c', '--cert', dest='cert',
        type=str, help='absolute path to cacert.pem file')
    group.add_argument(
        '-l', '--list', dest='list',
        action='store_true', help='to get public soft list')
    group.add_argument(
        '-g', '--get', type=int, dest='get',
        help='package number to install  manually')
    parser.add_argument(
        '-o', '--out', type=str, dest='out',
        help='full path to logfile')
    parser.add_argument(
        '-v', '--verbose', dest='verbose',
        action='store_true', help='verbose mode')
    parser.add_argument(
        '--version', action='version',
        version=ueconst.UE_CLIENT_VERSION, help='display version number')
    options = parser.parse_args()

    if len(sys.argv) == 1:
        parser.error('at least one argument is required')

    if (options.get is not None or options.list is True or options.inventory is True) and options.server is None:
        parser.error('a server URL is required')

    # Check options
    try:
        if options.out is not None:
            try:
                logging.basicConfig(level=logging.DEBUG, filename=options.out)
            except:
                logging.basicConfig(level=logging.DEBUG, filename='updatengine-client.log')
                logging.exception('can\'t write on '+options.out+' file use default file instead')
        else:
            logging.basicConfig(level=logging.DEBUG, filename='updatengine-client.log')

        last = False

        if options.list is True and options.server is not None:
            logging.info('*********************************\n')
            localtime = time.localtime()
            logging.info('Start: ' + time.strftime('%Y-%m-%d-%H:%M:%S', localtime))

            print('Public packages software available on server')
            url = options.server+'/post/'
            softxml = uecommunication.get_public_software_list(url, options)
            uecommunication.printable_public_software(softxml)

            logging.info('List public packages available on server')
            localtime = time.localtime()
            logging.info('End: ' + time.strftime('%Y-%m-%d-%H:%M:%S', localtime))

        if options.get is not None and options.server is not None:
            logging.info('*********************************\n')
            localtime = time.localtime()
            logging.info('Start: ' + time.strftime('%Y-%m-%d-%H:%M:%S', localtime))

            url = options.server+'/post/'
            print('Trying to install package %d' % options.get)
            logging.info('Trying to install package %d' % options.get)
            ue = uedownload()
            ue.download_pack(url, options.get, options)

            localtime = time.localtime()
            logging.info('End: ' + time.strftime('%Y-%m-%d-%H:%M:%S', localtime))

        if options.inventory is False and options.list is False and options.get is None:
            print('Just to test, inventory will not be send')
            last = True

        if options.minute is None:
            last = True

        download = uedownload()

        while True:
            if options.get is not None or options.list is True:
                break
            logging.info('*********************************\n')
            localtime = time.localtime()
            logging.info('Start: ' + time.strftime('%Y-%m-%d-%H:%M:%S', localtime))

            try:
                inventory = ueinventory.build_inventory()
            except Exception:
                print('Error when building inventory')
                logging.exception('Error when building inventory')
                sys.exit(1)
            else:
                if inventory is not None:
                    localtime = time.localtime()
                    print time.strftime('%Y-%m-%d-%H:%M:%S', localtime)
                    print('Inventory built')
                    logging.info('Inventory built')

                if options.verbose is True:
                    try:
                        inventory_pretty = inventory[0].replace('&', '&amp;')
                        inventory_pretty = parseXML(inventory_pretty).toprettyxml(encoding='UTF-8', indent='  ')
                        logging.info(inventory_pretty + inventory[1])
                        if len(sys.argv) == 2:
                            print(inventory_pretty)
                    except:
                        logging.info(inventory)

                if options.inventory is True and options.server is not None:
                    url = options.server+'/post/'
                    try:
                        response_inventory = uecommunication.send_inventory(url, inventory[0], options)
                    except Exception:
                        print('Error on send_inventory process')
                        logging.exception('Error on send_inventory process')
                        sys.exit(1)
                    else:
                        print('Inventory sent to ' + url)
                        logging.info('Inventory sent to ' + url)
                        if options.verbose is True:
                            print(parseXML(response_inventory).toprettyxml(encoding='UTF-8', indent='  '))
                        uecommunication.print_warninfo(response_inventory)
                        try:
                            extended_inventory = ueinventory.build_extended_inventory(response_inventory)
                            if extended_inventory:
                                if options.verbose is True:
                                    extended_pretty = extended_inventory.replace('&', '&amp;')
                                    logging.info(parseXML(extended_pretty).toprettyxml(encoding='UTF-8', indent='  '))
                                response_inventory = uecommunication.send_extended_inventory(url, extended_inventory, options)
                        except Exception:
                            print('Error on extended inventory function')
                            logging.exception('Error on extended inventory function')
                            sys.exit(1)
                        else:
                            if extended_inventory:
                                print('Extended inventory sent to ' + url)
                                logging.info('Extended inventory sent to ' + url)
                                if options.verbose is True:
                                    print(parseXML(response_inventory).toprettyxml(encoding='UTF-8', indent='  '))
                            try:
                                download.download_action(url, str(response_inventory), options)
                            except Exception:
                                print 'Error on download_action function'
                                logging.exception('Error on download_action function')
                                sys.exit(1)

            localtime = time.localtime()
            logging.info('End: ' + time.strftime('%Y-%m-%d-%H:%M:%S', localtime))

            if last:
                break
            else:
                logging.info('Waiting '+str(options.minute)+' minute(s) until next inventory\n')
                wait(options.minute, inventory[1])
    except:
        logging.exception('Error in main() function')
        sys.exit(1)

if __name__ == '__main__':
    main()
