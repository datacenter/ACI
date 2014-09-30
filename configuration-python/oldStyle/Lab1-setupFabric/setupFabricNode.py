from cobra.model.fabric import Pod, Node

from utility import *


def input_key_args(msg='\nPlease input fabric node info:'):
    print msg
    args = []
    args.append(get_raw_input('Pod ID (required): ', required=True))
    args.append(get_raw_input('Serial Number (required): ', required=True))
    args.append(get_raw_input('Node ID (required): ', required=True))
    args.append(get_raw_input('Node Name (required): ', required=True))
    return args


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
        host_name, user_name, password = input_login_info()
        pod_id, serial_num, node_id, node_name = input_key_args()


    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    setup_fabric_node(modir, pod_id, serial_num, node_id, node_name)

    modir.logout()


