#!/usr/bin/env python


__description__ = 'nmap scanner'
__author__ = 'Froststein'
__version__ = '0.2'

import pathlib
import nmap
import csv
import optparse
import time
import os

# Read stored values for scanNmapCSV()
def readInput(inputfile):
    ip_list=[]
    with open(inputfile, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row:
                ip_list+=[f'{"".join(row)}']
    return ip_list
    
def scanNmapXML(inputfile,outputfile):
    checkDir()
    command="nmap -iL "+ inputfile +" -oX logs/"+outputfile+".xml"
    os.system(command)
    
def checkDir():
    if not os.path.exists('./logs'):
        os.mkdir('logs')
        

def initializeScan(inputfile,outputfile):
    try:
        f=open(inputfile)
        scanNmapXML(inputfile,outputfile)
        f.close()
    except FileNotFoundError:
        print('File specified not found')
        inputfile = input('Enter the file name again: ')
        initializeScan(inputfile,outputfile)

        
def banner():
	banner = '''                                                                 ____    ___  
  _  _   __  __    ___      ___             ___                                                   
 | \| | |  \/  |  /   \    | _ \    o O O  / __|    __     __ _    _ _     _ _      ___      _ _  
 | .` | | |\/| |  | - |    |  _/   o       \__ \   / _|   / _` |  | ' \   | ' \    / -_)    | '_| 
 |_|\_| |_|__|_|  |_|_|   _|_|_   TS__[O]  |___/   \__|_  \__,_|  |_||_|  |_||_|   \___|   _|_|_  
_|"""""|_|"""""|_|"""""|_| """ | {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'                                                 
	'''
	print (banner)


def main():
    banner()
    oParser = optparse.OptionParser(usage='usage: %prog \n' + __description__, version='%prog ' + __version__)
    oParser.add_option('-i', '--input',dest='inputfile', type='str', help='Input file')
    
    (options, args) = oParser.parse_args()
    if ((options.inputfile != None)):
        #declare file name for scan/.csv and logs/.xml
        OUTPUTFILE=time.strftime("%Y%m%d-%H%M%S")
        initializeScan(options.inputfile,OUTPUTFILE)
    else:
        oParser.print_help()
    
    
if __name__ == "__main__":
    main()
    