#!/usr/bin/env python


__description__ = 'nmap scanner'
__author__ = 'Froststein'
__version__ = '0.2'

import os

def makeStorageDirectory():
    if not os.path.exists('./logs'):
        os.mkdir('logs')
        print('Directory /logs created..........')
    if not os.path.exists('./scan'):
        os.mkdir('scan')
        print('Directory /scan created..........')

def installNmapPythonLib():
    try:
        import nmap
        print('Nmap Python lib has already been installed.')
    except ImportError:
        print('Installing python nmap library..........')
        os.system('pip install python-nmap ')
        
def checkEnvVar():
    print('correct')
    
def makeScanningScript():
    
    
if __name__ == "__main__":
    makeStorageDirectory()
    installNmapPythonLib()
    checkEnvVar()
    makeScanningScript()
    