import sys
import getopt
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fabric import Pod, Node

from cobra.internal.codec.xmlcodec import toXMLStr


def apic_login(hostname, username, password):
    """Login to APIC"""
    epoint = EndPoint(hostname, secure=False, port=80)
    lsess = LoginSession(username, password)
    modir = MoDirectory(epoint, lsess)
    modir.login()
    return modir


def commit_change(modir, changed_object):
    """Commit the changes to APIC"""
    config_req = ConfigRequest()
    config_req.addMo(changed_object)
    modir.commit(config_req)


def get_value(args, key, default_value):
    """Return the value of an argument. If no such an argument, return a default value"""
    return args[key] if key in args.keys() else default_value


def setup_fabric_node(modir, pod_id, serial_num, node_id, node_name):
    fv_pod = modir.lookupByDn('topology/pod-' + pod_id)
    if isinstance(fv_pod, Pod):
        fv_node = Node(fv_pod, node_id, name=node_name, serial=serial_num)

    else:
        print 'Pod', pod_id, 'does not exist.'
        return

    print toXMLStr(fv_pod, prettyPrint=True)
    print 'Fabric configuration takes up to 5 minutes. Please wait.'
    # commit_change(modir, fv_pod)

if __name__ == '__main__':

    # Obtain the arguments from CLI
    try:
        host_name, user_name, password, pod_id, serial_num, node_id, node_name = sys.argv[1:8]
    except ValueError:
        print 'Usage:', __file__, '<hostname> <username> <password> <pod_id> <serial_num> <node_id> <node_name>'
        sys.exit()


    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    setup_fabric_node(modir, pod_id, serial_num, node_id, node_name)

    modir.logout()


