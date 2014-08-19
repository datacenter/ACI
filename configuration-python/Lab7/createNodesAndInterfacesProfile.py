import getopt
from createRoutedOutside import input_key_args as input_routed_outside_name
from cobra.model.l3ext import Out, LNodeP

from utility import *


def input_key_args(msg='\nPlease input the Node Profile info'):
    print msg
    return get_raw_input("Node Profile Name (required): ", required=True)


def input_optional_args(*arg):
    args = {}
    args['targetDscp'] = get_optional_input('Target DSCP (default: "unspecified"): ', [], num_accept=True)
    return args


def create_node_profile(modir, tenant_name, routed_outside_name, node_profile_name, **args):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    l3ext_out = modir.lookupByDn('uni/tn-' + tenant_name + '/out-' + routed_outside_name)
    if isinstance(l3ext_out, Out):
        l3ext_lnodep = LNodeP(l3ext_out, node_profile_name,
                              targetDscp=get_value(args, 'targetDscp', 'unspecified'))
    else:
        print 'External Routed Network', routed_outside_name, 'does not existed.'
    print_query_xml(l3ext_out)
    commit_change(modir, l3ext_out)


if __name__ == '__main__':

    # Obtain the arguments from CLI
    opts = sys.argv[1:]
    opts.reverse()

    # Obtain the key parameters.
    keys = []
    while len(opts) > 0 and opts[len(opts) - 1][0] != '-':
        keys.append(opts.pop())
    opts.reverse()

    try:
        host_name, user_name, password, tenant_name, routed_outside_name, node_profile_name = sys.argv[1:7]

        # Obtain the optional arguments that with a flag.
        try:
            opts, args = getopt.getopt(opts, 'D:', ['DSCP='])
        except getopt.GetoptError:
            sys.exit(2)
        optional_args = {}
        for opt, arg in opts:
            if opt in ('-D', '--DSCP'):
                optional_args['targetDscp'] = arg

    except ValueError:
        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name = input_routed_outside_name()
        node_profile_name = input_key_args()
        optional_args = input_optional_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_node_profile(modir, tenant_name, routed_outside_name, node_profile_name, args_from_CLI=optional_args)

    modir.logout()


