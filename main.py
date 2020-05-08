__description__ = 'nmap scanner'
__author__ = 'Froststein'

import argparse
import os
import time
import logging
import xml.dom.minidom as xmlParser

timestamp = None #global var for time of scan

def check_deviation(combined_dic):
    check = False
    deviations = []
    keys = []
    for key,value in combined_dic.items():
        keys.append(key)
    print(keys)
    oldData = combined_dic[keys[1]] #get previous scan result
    newData = combined_dic[keys[0]] #get newest scan result
    for key in newData:
        if(newData[key] != oldData[key]):
            deviations.append(key)
            check = True
    return check, deviations


def process_XML(log_files):
    combined_datadic = {}
    for xmlFile in log_files:
        doc = xmlParser.parse(xmlFile)
        dataDic = {}
        for host in doc.getElementsByTagName('host'):
            ip = host.getElementsByTagName('address')[0].getAttribute('addr')
            port_state = []
            open_count, close_count = 0,0
            for port in host.getElementsByTagName('port'):
                state = port.getElementsByTagName('state')[0].getAttribute('state')
                if state == 'open' :
                    open_count  +=  1
                elif state == 'close':
                    close_count +=1
            port_state.append(open_count)
            port_state.append(close_count)
            dataDic.update({ip:port_state})
        time = doc.getElementsByTagName('nmaprun')[0].getAttribute('start')
        combined_datadic.update({time:dataDic})
    return combined_datadic


# directory = ./logs/
def getLogs(directory):
    log_files = []
    for f in os.listdir(directory):
        if os.path.isfile(os.path.join(directory,f)) and f.endswith('.xml'):
            log_files.append(os.path.join(directory,f))
    return sorted(log_files, reverse=True)


def scan(inputfile):
    filename = str(int(time.time())) +'.xml'
    global timestamp
    timestamp=filename.strip('.xml')
    command='nmap -iL '+ inputfile +' -oX logs/' +filename
    try:
        os.system(command)
    except RuntimeError:
        print('Error occured')

def initialize_scan(inputfile):
    try:
        f=open(inputfile)
        scan(inputfile)
        f.close()
    except FileNotFoundError:
        print('File specified not found')
        input_file = input('Enter the file name again: ')
        return initialize_scan(input_file)


def print_deviation(ip_arr):
    print('Deviation detected.')
    print('IP(s) with deviation :')
    for ip in ip_arr:
        print(ip)


def revert():
    print('Reverting changes....')
    try: 
        os.remove('./logs/'+timestamp+'.xml')
    except FileNotFoundError as e:
        logging.error(e)

def setUp():
    try:
        if not os.path.exists('./logs'):
            print('Setting up environment........')
            os.mkdir('logs')
    except SystemError as e:
        logging.error(e)
        print('Opps.. something went wrong. Please try again')


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


if __name__ == '__main__':
    banner()
    setUp()

    aParser = argparse.ArgumentParser(description='usage: ' + __description__ ) 
    aParser.add_argument('-i',dest='inputfile', action='store',default=False,help='Input file')
    aParser.add_argument('-d',dest='deviation', action='store_true',default=False,help='Check for deviations')
    aParser.add_argument('-s',dest='scan', action='store_true',default=False,help='Include an input file to use nmap to scan')
    result = aParser.parse_args()

    try:
        if (result.inputfile != None and result.scan is True):
            initialize_scan(result.inputfile)   #scan list of ip and produce xml file
        if (result.deviation is True):    
            log_list = getLogs('./logs/')   #get list of past logs
            if len(log_list) != 1:
                combined_dic = process_XML(log_list)    #process all xml log files to dictionary
                result = check_deviation(combined_dic) #check for deviation
                if bool(result[0]):
                    print_deviation(result[1])
                else:
                    print('No deviations detected.')
            else:
                print('Insufficiant data. Please perform scan again.')

    except KeyboardInterrupt as e:
        print('\nScan cancelled.....')
        revert()
    except RuntimeError as e:
        print('Opps... something went wrong. Please try again.')

