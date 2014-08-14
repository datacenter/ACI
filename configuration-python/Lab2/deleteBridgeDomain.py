import sys
from cobra.model.fv import BD

from utility import *


def input_key_args():
    print 'Please input Bridge Domain info:'
    args = []
    args.append(get_raw_input("Bridge Domain (required): "))
    return args


def delete_bridge_domain(modir, tenant_name, bridge_domain):
    """Delete a bridge domain"""
    fv_bd = modir.lookupByDn('uni/tn-' + tenant_name + '/BD-' + bridge_domain)
    if isinstance(fv_bd, BD):
        fv_bd.delete()
    else:
        print 'Bridge Domain', bridge_domain, 'does not existed.'
        return

    print_query_xml(fv_bd)
    commit_change(modir, fv_bd)

if __name__ == '__main__':
    if len(sys.argv) != 6:
        hostname, username, password = input_login_info()
        tenant_name = input_tenant_name()
        bridge_domain = input_key_args()
    else:
        hostname, username, password, tenant_name, bridge_domain = sys.argv[1:]
    modir = apic_login(hostname, username, password)
    delete_bridge_domain(modir, tenant_name, bridge_domain)
    modir.logout()
