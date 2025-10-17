from ncclient import manager
import xmltodict
from pprint import pprint

m = manager.connect(
        host="10.30.6.11",
        port=830,
        username="admin",
        password="cisco",
        hostkey_verify=False
    )

def create():
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
    
    findInterface = """
        <filter>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface><name>Loopback66070217</name></interface>
            </interfaces>
        </filter>
    """

    try:
        interfaceResult = netconf_get_config(findInterface)
        xml_interface = interfaceResult.xml
        if ("Loopback66070217" in xml_interface):
            raise Exception("Interface already exist.")
        
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if ('<ok/>' in xml_data):
            return "Interface loopback 66070217 is created successfully"
    except Exception as e:
        print("Error!", e)
        return "Cannot create: Interface loopback 66070217"


def delete():
    netconf_config = """
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface operation="delete">
                    <name>Loopback66070217</name>
                </interface>
            </interfaces>
        </config>
    """

    findInterface = """
        <filter>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface><name>Loopback66070217</name></interface>
            </interfaces>
        </filter>
    """

    try:
        findInterfaceResult = netconf_get_config(findInterface).xml
        if ("Loopback66070217" in findInterfaceResult):
            netconf_reply = netconf_edit_config(netconf_config)
            xml_data = netconf_reply.xml
            print(xml_data)
            if '<ok/>' in xml_data:
                return "Interface loopback 66070217 is deleted successfully"
        else:
            raise Exception("Interface Loopback66070217 doesn't exist")
    except:
        print("Error!")
        return "Cannot delete: Interface loopback 66070217"


def enable():
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

    findInterface = """
        <filter>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface><name>Loopback66070217</name></interface>
            </interfaces>
        </filter>
    """

    try:
        findInterfaceResult = netconf_get_config(findInterface).xml
        if not ("Loopback66070217" in findInterfaceResult):
            raise Exception("Interface Loopback66070217 doesn't exist")
        
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070217 is enabled successfully"
    except:
        print("Error!")
        return "Cannot enable: Interface loopback 66070217"


def disable():
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

    findInterface = """
        <filter>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface><name>Loopback66070217</name></interface>
            </interfaces>
        </filter>
    """

    try:
        findInterfaceResult = netconf_get_config(findInterface).xml
        if not ("Loopback66070217" in findInterfaceResult):
            raise Exception("Interface Loopback66070217 doesn't exist")

        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070217 is shutdowned successfully"
    except Exception as e:
        print("Error!", e)
        return "Cannot shutdown: Interface loopback 66070217"

def netconf_edit_config(netconf_config):
    return  m.edit_config(target="running", config=netconf_config)

def netconf_get_config(netconf_config):
    return m.get_config(source="running", filter=netconf_config)

def status():
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
                return "Interface loopback 66070123 is enabled"
            elif admin_status == 'down' and oper_status == 'down':
                return "Interface loopback 66070123 is disabled"
        else: # no operation-state data
            return "No Interface loopback 66070123"
    except:
       print("Error!")
