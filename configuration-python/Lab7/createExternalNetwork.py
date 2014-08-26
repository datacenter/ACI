import getopt
from createRoutedOutside import input_key_args as input_routed_outside_name
from cobra.model.l3ext import InstP, Subnet

from utility import *
from IPython import embed

def input_key_args(msg='\nPlease input External EPG Network info'):
    print msg
    return get_raw_input("EPG Network Name (required): ", required=True)


def input_optional_args(*arg):
    args = {}
    args['prio'] = get_optional_input('QoS Class (default: "unspecified"): ', ['level1', 'level2', "level3", "unspecified"])
    args['subnet_ip'] = get_raw_input('Subnet IP Address (optional): ')
    return args


def create_external_network(modir, tenant_name, routed_outside_name, external_network_name, **args):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    l3ext_out = modir.lookupByDn('uni/tn-'+tenant_name+'/out-'+routed_outside_name)

    if l3ext_out is None:
        print 'External Routed Network', routed_outside_name, 'does not existed.'
        return

    l3ext_instp = InstP(l3ext_out, external_network_name,
                        prio=get_value(args,'prio', 'unspecified'))

    if 'subnet_ip' in args.keys() and args['subnet_ip'] != '':
        l3ext_subnet = Subnet(l3ext_instp, args['subnet_ip'])

    print_query_xml(l3ext_out)
    commit_change(modir, l3ext_out)

if __name__ == '__main__':

    # Obtain the arguments from CLI
    opts = sys.argv[1:]
    opts.reverse()

    # Obtain the key parameters.
    keys = []
    while len(opts) > 0 and opts[len(opts)-1][0] != '-':
        keys.append(opts.pop())
    opts.reverse()

    try:
        host_name, user_name, password, tenant_name, routed_outside_name, external_network_name = sys.argv[1:7]

        # Obtain the optional arguments that with a flag.
        try:
            opts, args = getopt.getopt(opts, 'Q:s:', ['QoS=', 'subnet='])
        except getopt.GetoptError:
            sys.exit(2)
        optional_args = {}
        for opt, arg in opts:
            if opt in ('-Q', '--QoS'):
                optional_args['prio'] = arg
            elif opt in ('-s', '--subnet'):
                optional_args['subnet_ip'] = arg

    except ValueError:
        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name = input_routed_outside_name()
        external_network_name = input_key_args()
        optional_args = input_optional_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_external_network(modir, tenant_name, routed_outside_name, external_network_name, args_from_CLI=optional_args)

    modir.logout()


