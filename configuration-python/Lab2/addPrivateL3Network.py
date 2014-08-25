from utility import *
from cobra.model.fv import Ctx


def input_key_args(msg='Please input Private L3 Network info:'):
    print msg
    return get_raw_input("Private L3 Network (required): ", required=True)


def add_private_l3_network(modir, tenant_name, private_l3_network):
    """Build a private L3 network"""

    # Query a tenant
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)

    # create a private network
    fv_ctx = Ctx(fv_tenant, private_l3_network)

    print_query_xml(fv_tenant)
    commit_change(modir, fv_tenant)

if __name__ == '__main__':
    try:
        host_name, user_name, password, tenant_name, private_l3_network = sys.argv[1:]
    except ValueError:
        try: 
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            tenant_name = data['tenant']
            private_l3_network = data['private_network']
        except (IOError, KeyError, TypeError):
            host_name, user_name, password = input_login_info()
            tenant_name = input_tenant_name()
            private_l3_network = input_key_args()

    modir = apic_login(host_name, user_name, password)
    add_private_l3_network(modir, tenant_name, private_l3_network)
    modir.logout()
