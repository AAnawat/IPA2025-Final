# --------------------------------------------------------------
# Import libraries and connect to device
# --------------------------------------------------------------

from ncclient import manager
from dotenv import load_dotenv
import xmltodict
import os

load_dotenv()

m = manager.connect(
        host=os.environ.get("ROUTER_HOST"),
        port=830,
        username=os.environ.get("ROUTER_USER"),
        password=os.environ.get("ROUTER_PASS"),
        hostkey_verify=False
    )


# --------------------------------------------------------------
# Core functions
# --------------------------------------------------------------

# Create Loopback66070217 interface
def create():
    # Define Netconf configuration for creating Loopback66070217 interface
    netconf_config = """
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>Loopback66070217</name>
                    <description>Anawat Wongprachanukul 66070217 Loopback interface</description>
                    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                    <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                        <address>
                            <ip>172.2.17.1</ip>
                            <netmask>255.255.255.0</netmask>
                        </address>
                    </ipv4>
                </interface>
            </interfaces>
        </config>
    """

    try:
        # Check if interface Loopback66070217 already exists
        checkExist = check_interface_exist()
        if (checkExist):
            raise Exception("Interface already exist.")
        
        # Apply Netconf edit-config operation to create the interface
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if ('<ok/>' in xml_data):
            return "Interface loopback 66070217 is created successfully using Netconf"
    except:
        print("Error!")
        return "Cannot create: Interface loopback 66070217"


# Delete Loopback66070217 interface
def delete():
    # Define Netconf configuration for deleting Loopback66070217 interface
    netconf_config = """
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface operation="delete">
                    <name>Loopback66070217</name>
                </interface>
            </interfaces>
        </config>
    """

    try:
        # Check if interface Loopback66070217 exists
        checkExist = check_interface_exist()
        if not (checkExist):
            raise Exception("Interface Loopback66070217 doesn't exist")
        
        # Apply Netconf edit-config operation to delete the interface
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070217 is deleted successfully using Netconf"
    except:
        print("Error!")
        return "Cannot delete: Interface loopback 66070217"

# Enable Loopback66070217 interface
def enable():
    # Define Netconf configuration for enabling Loopback66070217 interface
    netconf_config = """
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>Loopback66070217</name>
                    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                    <enabled>true</enabled>
                </interface>
            </interfaces>
        </config>
    """

    try:
        # Check if interface Loopback66070217 exists
        checkExist = check_interface_exist()
        if not (checkExist):
            raise Exception("Interface Loopback66070217 doesn't exist")
        
        # Apply Netconf edit-config operation to enable the interface
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070217 is enabled successfully using Netconf"
    except:
        print("Error!")
        return "Cannot enable: Interface loopback 66070217"

# Enable Loopback66070217 interface
def disable():
    # Define Netconf configuration for disabling Loopback66070217 interface
    netconf_config = """
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>Loopback66070217</name>
                    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                    <enabled>false</enabled>
                </interface>
            </interfaces>
        </config>
    """

    try:
        # Check if interface Loopback66070217 exists
        checkExist = check_interface_exist()
        if not (checkExist):
            raise Exception("Interface Loopback66070217 doesn't exist")

        # Apply Netconf edit-config operation to disable the interface
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070217 is shutdowned successfully using Netconf"
    except:
        print("Error!")
        return "Cannot shutdown: Interface loopback 66070217 (checked by Netconf)"

# Get status of Loopback66070217 interface
def status():
    refresh_session()
    # Define Netconf filter to get interfaces-state information for Loopback66070217
    netconf_filter = """
        <filter>
            <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface><name>Loopback66070217</name></interface>
            </interfaces-state>
        </filter>
    """

    try:
        # Use Netconf operational operation to get interfaces-state information
        netconf_reply = m.get(filter=netconf_filter)
        print(netconf_reply)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

        # if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
        if not (netconf_reply_dict["rpc-reply"]["data"] == None):
            # extract admin_status and oper_status from netconf_reply_dict
            admin_status = netconf_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"]["admin-status"]
            oper_status = netconf_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"]["oper-status"]
            if admin_status == 'up' and oper_status == 'up':
                return "Interface loopback 66070217 is enabled (checked by Netconf)"
            elif admin_status == 'down' and oper_status == 'down':
                return "Interface loopback 66070217 is disabled (checked by Netconf)"
        else: # no operation-state data
            return "No Interface loopback 66070217 (checked by Netconf)"
    except:
       print("Error!")


# --------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------

# Applying Netconf edit-config operation
def netconf_edit_config(netconf_config):
    refresh_session()
    return  m.edit_config(target="running", config=netconf_config)

# Getting configuration data using Netconf get-config operation
def netconf_get_config(netconf_config):
    refresh_session()
    return m.get_config(source="running", filter=netconf_config)

# Check if interface Loopback66070217 exists
# Returns: True if exists, False otherwise
def check_interface_exist():
    findInterface = """
        <filter>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface><name>Loopback66070217</name></interface>
            </interfaces>
        </filter>
    """
    
    interfaceResult = netconf_get_config(findInterface).xml
    return ("Loopback66070217" in interfaceResult)

# Refresh Netconf session
def refresh_session():
    global m
    
    m = manager.connect(
        host=os.environ.get("ROUTER_HOST"),
        port=830,
        username=os.environ.get("ROUTER_USER"),
        password=os.environ.get("ROUTER_PASS"),
        hostkey_verify=False
    )