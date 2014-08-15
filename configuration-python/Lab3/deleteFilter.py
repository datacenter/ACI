import sys
from cobra.model.vz import Filter

from utility import *


def input_key_args():
    print 'Please input Filter info:'
    return get_raw_input("Filter Name (required): ")


def delete_filter(modir, tenant_name, filter_name):
    # Check if the filter exists or not. If yes, delete it.
    fv_ct = modir.lookupByDn('uni/tn-' + tenant_name + '/flt-' + filter_name)
    if isinstance(fv_ct, Filter):
        fv_ct.delete()
    else:
        print 'There is no filter called', filter_name, 'in tenant', tenant_name, '.'
        return

    print toXMLStr(fv_ct, prettyPrint=True)

    commit_change(modir, fv_ct)


if __name__ == '__main__':
    if len(sys.argv) != 6:
        hostname, username, password = input_login_info()
        tenant_name = input_tenant_name()
        filter_name = input_key_args()
    else:
        hostname, username, password, tenant_name, filter_name = sys.argv[1:]
    modir = apic_login(hostname, username, password)
    delete_filter(modir, tenant_name, filter_name)
    modir.logout()
