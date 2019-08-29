#!/usr/bin/env python3

#realtimetranslation.net

import scapy.all as scapy
#from scapy import all as scapy
import optparse
import json
import urllib.request as urllib
import codecs


def get_arguments():

	parser = optparse.OptionParser()
	parser.add_option("-t", "--target", dest="target", help="IP ADRESS OF TARGET NETWORK.") #using optparse to pass target ip address
	#parser.add_option("-h", "--help", help="")
	(options, arguments) =  parser.parse_args()

	return options

def get_mac(ip):
	arp_req = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_req_broadcast = broadcast/arp_req
	answerd_list = scapy.srp(arp_req_broadcast, timeout=1, verbose=False)[0]

	return answerd_list[0][1].hwsrc

def scan(ip):
	arp_req = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_req_broadcast = broadcast/arp_req #combining two packets together with "/"
	answerd_list = scapy.srp(arp_req_broadcast, timeout=1, verbose=False)[0]
	client_list = []
	for element in answerd_list:
		client_dict = {"ip":element[1].psrc, "mac":element[1].hwsrc}
		client_list.append(client_dict)

	return client_list

def get_mac_vendor(mac_v):
	mac_url = "http://macvendors.co/api/"
	req = urllib.Request(mac_url+mac_v, headers={'User-agent' : "API Browser"})
	response = urllib.urlopen(req)
	reader = codecs.getreader("utf-8")
	obj = json.load(reader(response))
	reqprint = (obj['result']['company'])

	return reqprint


def print_result(result_list):
	print("----------------------------------------------------------------------------------------------")
	print("IP ADDRESS\t\t\tMAC ADDRESS\t\t\tMAC VENDOR")
	print("----------------------------------------------------------------------------------------------")

	for client in result_list:
		print (client["ip"] + "\t\t\t" + client["mac"] + "\t\t" + get_mac_vendor(client["mac"])) 

	#print(unanswerd.summary()) #printing the summary of a packet
	#scapy.ls(scapy.Ether) #checking for fields

options = get_arguments()
scan_res = scan(options.target)
print_result(scan_res)
