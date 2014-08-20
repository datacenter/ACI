from cobra.model.fv import BD, RsBDToOut

from utility import *


def input_key_args(msg='Please input Bridge Domain and Network info:'):
    print msg
    args = []
    args.append(get_raw_input("Bridge Domain Name (required): ", required=True))
    args.append(get_raw_input("L3 Outside Network Name (required): ", required=True))
    return args


def disassociate_l3_outside_network_to_bd(modir, tenant_name, bridge_domain, network_name):

    fv_bd = modir.lookupByDn('uni/tn-' + tenant_name + '/BD-' + bridge_domain)
    if isinstance(fv_bd, BD):
        fv_rsbdtoout = modir.lookupByDn('uni/tn-' + tenant_name + '/BD-' + bridge_domain + '/rsBDToOut-' + network_name)
        if isinstance(fv_rsbdtoout, RsBDToOut):
            fv_rsbdtoout.delete()
        else:
            print 'Network', network_name, 'is not associating to Bridge Domain', bridge_domain
            return
    else:
        print 'Bridge Domain', bridge_domain, 'does not existed.'
        return

    print_query_xml(fv_rsbdtoout)
    commit_change(modir, fv_rsbdtoout)


if __name__ == '__main__':
    try:
        hostname, username, password, tenant_name, bridge_domain, network_name = sys.argv[1:7]
    except ValueError:
        hostname, username, password = input_login_info()
        tenant_name = input_tenant_name()
        bridge_domain, network_name = input_key_args()
    modir = apic_login(hostname, username, password)
    disassociate_l3_outside_network_to_bd(modir, tenant_name, bridge_domain, network_name)
    modir.logout()
