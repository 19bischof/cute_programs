# Import the necessary packages
from consolemenu import *
from consolemenu.items import *
import subnetter
import time

s = subnetter.subnetter()

# Create the menu
main_menu = ConsoleMenu("Main Menu","Gain Information about your Subnet")
set_ipadress_menu = ConsoleMenu("Input-Options","in which manner do you want to input the IP-Adress?")
set_subnetmask_menu = ConsoleMenu("Input-Options","in which manner do you want to input the Subnetmask?")
show_subnetmask_menu = ConsoleMenu("Output-Options","How do you want the Subnetmask displayed?")
show_ipadress_menu = ConsoleMenu("Output-Options","How do you want the IP-Adress displayed?")



def pre_set_ipadress_in_decimal():
    s.set_ipadress_in_decimal(input().strip())
    time.sleep(0.5)
def pre_set_ipadress_in_binary():
    s.set_ipadress_in_binary(input().strip())
    time.sleep(0.5)

set_ipadress_menu_item = SubmenuItem("Set IP-Adress", set_ipadress_menu, main_menu)
set_ip_in_decimal = FunctionItem("Decimal", pre_set_ipadress_in_decimal)
set_ip_in_binary = FunctionItem("Binary", pre_set_ipadress_in_binary)
set_ipadress_menu.append_item(set_ip_in_decimal)
set_ipadress_menu.append_item(set_ip_in_binary)

def pre_set_mask_in_decimal():
    s.set_subnetmask_in_decimal(input().strip())
    time.sleep(0.5)
def pre_set_mask_in_binary():
    s.set_subnetmask_in_binary(input().strip())
    time.sleep(0.5)
def pre_set_mask_in_slash():
    s.set_subnetmask_in_slash(input().strip())
    time.sleep(0.5)
set_subnetmask_menu_item = SubmenuItem("Set Subnetmask", set_subnetmask_menu, main_menu)
set_mask_in_decimal_item = FunctionItem("Decimal", pre_set_mask_in_decimal)
set_mask_in_binary_item = FunctionItem("Binary", pre_set_mask_in_binary)
set_mask_in_slash_item = FunctionItem("Slash", pre_set_mask_in_slash)
set_subnetmask_menu.append_item(set_mask_in_decimal_item)
set_subnetmask_menu.append_item(set_mask_in_binary_item)
set_subnetmask_menu.append_item(set_mask_in_slash_item)

def pre_show_dec_subnetmask():  
    s.show_dec_subnetmask()
    input()
def pre_show_bin_subnetmask():
    s.show_bin_subnetmask()
    input()
def pre_show_slash_subnetmask():
    s.show_slash_subnetmask()
    input()
show_subnetmask_menu_item = SubmenuItem("Show Subnetmask", show_subnetmask_menu,main_menu)
show_dec_mask_item = FunctionItem("Decimal", pre_show_dec_subnetmask)
show_bin_mask_item = FunctionItem("Binary", pre_show_bin_subnetmask)
show_slash_mask_item = FunctionItem("Slash", pre_show_slash_subnetmask)
show_subnetmask_menu.append_item(show_dec_mask_item)
show_subnetmask_menu.append_item(show_bin_mask_item)
show_subnetmask_menu.append_item(show_slash_mask_item)


def pre_show_ipadress_in_decimal():
    s.show_ipadress()
    input()
def pre_show_ipadress_in_binary():
    s.show_bin_ipadress()
    input()

show_ipadress_menu_item = SubmenuItem("Show IP-Adress", show_ipadress_menu, main_menu)
show_ip_in_decimal = FunctionItem("Decimal", pre_show_ipadress_in_decimal)
show_ip_in_binary = FunctionItem("Binary", pre_show_ipadress_in_binary)
show_ipadress_menu.append_item(show_ip_in_decimal)
show_ipadress_menu.append_item(show_ip_in_binary)

def pre_show_number_of_hosts():
    s.show_number_of_hosts()
    input()
show_number_of_hosts_item = FunctionItem("Show Number of possible Hosts",pre_show_number_of_hosts)

def pre_show_host_ip_range():
    s.show_host_ip_range()
    input()
show_host_ip_range_item = FunctionItem("Show IP-Range of Hosts",pre_show_host_ip_range)

def pre_show_network_adress():
    s.show_network_adress()
    input()
show_network_adress_item = FunctionItem("Show Network Adress",pre_show_network_adress)
def pre_show_broadcast_adress():
    s.show_broadcast_adress()
    input()
show_broadcast_adress_item = FunctionItem("Show Broadcast Adress",pre_show_broadcast_adress)


# Once we're done creating them, we just add the items to the menu
main_menu.append_item(set_subnetmask_menu_item)
main_menu.append_item(set_ipadress_menu_item)
main_menu.append_item(show_subnetmask_menu_item)
main_menu.append_item(show_ipadress_menu_item)
main_menu.append_item(show_number_of_hosts_item)
main_menu.append_item(show_host_ip_range_item)
main_menu.append_item(show_network_adress_item)
main_menu.append_item(show_broadcast_adress_item)

# Finally, we call show to show the menu and allow the user to interact
main_menu.show()

