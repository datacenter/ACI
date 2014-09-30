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
    key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                {'name': 'routed_outside', 'help': 'Routed Outside Network Name.'},
                {'name': 'external_network', 'help': 'External Network Name.'},
                {'name': 'contract', 'help': 'Contract Name.'},
    ]
    opt_args = [{'flag': 'm', 'name': 'Match type', 'dest': 'matchT', 'help': 'The matched EPG type.'},
                {'flag': 'Q', 'name': 'QoS_class', 'dest': 'prio', 'help': 'The priority level of a sub application running behind an endpoint group.'}
    ]

    try:
        host_name, user_name, password, args = set_cli_argparse('Configure provider contract for outside network.', key_args, opt_args)
        tenant_name = args.pop('tenant')
        routed_outside_name = args.pop('routed_outside')
        external_network_name = args.pop('external_network')
        contract_name = args.pop('contract')
        optional_args = args

    except SystemExit:

        if check_if_requesting_help(sys.argv, opt_args):
            sys.exit('Help Page')

        if len(sys.argv)>1:
            print 'Invalid input arguments.'

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


