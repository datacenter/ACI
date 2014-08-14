from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest

from cobra.internal.codec.xmlcodec import toXMLStr


def apic_login(hostname, username, password):
    """Login to APIC"""
    epoint = EndPoint(hostname, secure=False, port=80)
    lsess = LoginSession(username, password)
    modir = MoDirectory(epoint, lsess)
    modir.login()
    return modir


def get_raw_input(prompt=''):
    return raw_input(prompt).strip()


def input_login_info(msg='\nInappropriate input arguments. Please fill in the arguments step by step.'):
    print msg
    print 'Login info:'
    return [get_raw_input("Host Name (required): "), get_raw_input("User Name (required): "),
            get_raw_input("Password (required): ")]


def input_tenant_name():
    print 'Please input Tenant info:'
    return get_raw_input("Tenant Name (required): ")


def commit_change(modir, changed_object):
    """Commit the changes to APIC"""
    config_req = ConfigRequest()
    config_req.addMo(changed_object)
    modir.commit(config_req)


def get_value(args, key, default_value):
    """Return the value of an argument. If no such an argument, return a default value"""
    return args[key] if key in args.keys() else default_value


def print_query_xml(xml_file, pretty_print=True):
    print toXMLStr(xml_file, prettyPrint=pretty_print)
