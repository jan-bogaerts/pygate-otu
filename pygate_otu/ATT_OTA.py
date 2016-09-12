__author__ = 'Sander Hendrickx'

import httplib
import zipfile
import os
import logging

'''
liatogateway-<version number>.zip

    example liatogateway-0_1.zip
'''


def upgradeFirmware(version):
    '''
    delete current root folder
    download new firmware
    unpack new firmware in root folder
    reboot device
    :param version:
    '''
    file = 'liatogateway-' + version + '.zip'
    conn = httplib.HTTPConnection("liato.blob.core.windows.net")
    conn.request("GET", "/firmware/" + version + '.zip')
    response = conn.getresponse()
    logging.info(response.status)

    if response.status == 200:
        #deleteFolder()
        target_path = os.getcwd()
        targetFile = os.path.join(target_path, file)
        f = open(targetFile, 'wb')                          # download file from ATT cloud
        f.write(response.read())
        f.close()
        logging.info('unzipping ' + targetFile)
        with zipfile.ZipFile(targetFile, 'r') as z:         # unzip file in current folder
            z.extractall(target_path)
    restart()

def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
    output = process.communicate()[0]
    logging.info(output)

def getVersionNumber():
    if os.path.isfile('version.txt'):
        with open('version.txt') as f:
            content = [x.strip('\n') for x in f.readlines()]
            return content[0]
    else:
        return 'unknown version'
