import getopt
from cobra.model.fv import RsProv
from cobra.model.l3ext import InstP

from createRoutedOutside import input_key_args as input_routed_outside_name
from createExternalNetwork import input_key_args as input_external_network_name

from utility import *


def input_key_args(msg='\nPlease input Provider Contract info'):
    print msg
    return get_raw_input("Provider Contract Name (default: 'default'): ")


def input_optional_args(*arg):
    args = {}
    args['prio'] = get_optional_input('QoS Class (default: "unspecified"): ', ['level1', 'level2', "level3", "unspecified"])
    args['matchT'] = get_optional_input('Match Type (default: "AtleastOne"): ', ['All', 'AtleastOne', "AtmostOne", "None"])
    return args


def create_L3_epg_provider_contract(modir, tenant_name, routed_outside_name, external_network_name, contract_name, **args):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    l3ext_instp = modir.lookupByDn('uni/tn-'+tenant_name+'/out-'+routed_outside_name+'/instP-'+external_network_name)

    if contract_name == '':
        contract_name = 'default'

    if isinstance(l3ext_instp, InstP):
        fv_l3epg_rsprov = RsProv(l3ext_instp, contract_name,
                                 prio=get_value(args, 'prio', 'unspecified'),
                                 matchT=get_value(args, 'matchT', 'AtleastOne'))
    else:
        print 'External Netwrok', external_network_name, 'does not existed.'
        return

    print_query_xml(l3ext_instp)
    commit_change(modir, l3ext_instp)

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
        host_name, user_name, password, tenant_name, routed_outside_name, external_network_name, contract_name = sys.argv[1:8]

        # Obtain the optional arguments that with a flag.
        try:
            opts, args = getopt.getopt(opts, 'Q:m:',
                                       ['QoS=','match-type='])
        except getopt.GetoptError:
            sys.exit(2)
        optional_args = {}
        for opt, arg in opts:
            if opt in ('-Q', '--m'):
                optional_args['prio'] = arg
            elif opt in ('-m', '--match-type'):
                optional_args['matchT'] = arg

    except ValueError:
        host_name, user_name, password = input_login_info() 
        tenant_name = input_tenant_name()
        routed_outside_name = input_routed_outside_name()
        external_network_name = input_external_network_name()
        contract_name = input_key_args()
        optional_args = input_optional_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_L3_epg_provider_contract(modir, tenant_name, routed_outside_name, external_network_name, contract_name, args_from_CLI=optional_args)

    modir.logout()


