import nmap
import csv

# Read stored values to scan with nmap
def readCSV():
    # declare list to store IP Address / Web Addresses
    ip_list=[]
    #further improvements could be made for line 8
    with open('test.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row:
                ip_list+=[f'{"".join(row)}']
    return ip_list

def scan():
    
    scanresult_list=[]
    
    ip_list = readCSV()
    print("List to scan: ", ip_list)
    print("Scanner Starting.......")
    ns = nmap.PortScanner()
    ns.scan(ip_list[0],'1-1024','-v -sS')
    print(ns.scaninfo())
    print("IP Status: ",ns[ip_list[0]].state())
    print(ns[ip_list[0]].all_protocols())
    print("Open Ports: ", ns[ip_list[0]]['tcp'].keys())
    scanresult_list+=[ns[ip_list[0]]['tcp'].keys()]
    print(scanresult_list)
    
    
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
    scan()
    
    
if __name__ == "__main__":
    main()
    