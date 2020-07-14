#!/usr/bin/env python

import subprocess
import optparse  # using --interface wlan0 in command line
import re  # this library functions allows to run regex command


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change its Mac addres")
    parser.add_option("-m", "--mac", dest="new_mac",
                      help="Enter new mac adress")
    # this commands allows to run parser.add_option on terminal and save to variable
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Please specify an interface , use --help for more info.")
    elif not options.new_mac:
        parser.error("Please specify an new mac , use --help for more info.")
    return options


def change_mac(interface, new_mac):
    print("Changing MAC address for " + interface + " to " + new_mac)
    # subprocess.call("ifconfig "+interface+" down", shell=True)  # to start comment on terminator but this is not security
    # because person can run more than one command on terminator like wlan0;ls
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(
        ifconfig_result))  # using str because python3 need this to run
    if mac_address_search_result:
        # there can be more than one result  we need first element so we use group(0)
        return mac_address_search_result.group(0)
    else:
        print("Could not read MAC address.")


options = get_arguments()

current_mac = get_current_mac(options.interface)
# using str because  upper code has a string in else block so there cannot be return a type
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("MAC address was successfully changed to " + current_mac)
else:
    print("MAC address did not change")
