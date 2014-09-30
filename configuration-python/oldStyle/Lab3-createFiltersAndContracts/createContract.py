from cobra.model.vz import BrCP, Subj, RsSubjFiltAtt

from utility import *


DEFAULT_SCOPE = 'context'
DEFAULT_REVERSE_FILTER_PORTS = 'true'
DEFAULT_QOS = 'unspecified'


def input_key_args(msg='Please input Contract info:'):
    print msg
    return get_raw_input("Contract Name (required): ", required=True)


def input_optional_args(contract_name):
    args = {'subject_name': get_raw_input(
                'Subject Name (default: "' + contract_name.lower() + '"): '),
            'scope': get_optional_input(
                'Scope (default: "' + DEFAULT_SCOPE + '")',
                ['application-profile(a)', 'context(c)', 'global(g)',
                 'tenant(t)']),
            'revFltPorts': get_optional_input(
                'Reverse Filter Ports (default: "' + DEFAULT_REVERSE_FILTER_PORTS + '")',
                ['true(t)', 'false(f)']),
            'prio': get_optional_input(
                'QoS Class (default: "' + DEFAULT_QOS + '")',
                ['level1', 'level2', 'level3']),
            'filter_name': get_raw_input('Filter Name (default: "None")')}
    return args


def create_contract(modir, tenant_name, contract_name, **args):
    """Query a tenant"""
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    if isinstance(fv_tenant, Tenant):
        # Create contract
        vz_ct = BrCP(fv_tenant, contract_name,
                     scope=get_value(args, 'scope', DEFAULT_SCOPE))

        # Add a subject to the contract
        vz_subj = Subj(vz_ct, get_value(args, 'subject_name',
                                        contract_name + '_subj'),
                       revFltPorts=get_value(args, 'revFltPorts',
                                             DEFAULT_REVERSE_FILTER_PORTS),
                       prio=get_value(args, 'prio', DEFAULT_QOS))

        # Assign an existed filter to the subject
        filters = get_value(args, 'filter_name', '')
        if filters != '':
            vz_rs_subj_filt_att = RsSubjFiltAtt(vz_subj, filters)

    else:
        print 'Tenant', tenant_name, 'does not exist. Please create a tenant first'
        return

    print_query_xml(fv_tenant)
    commit_change(modir, fv_tenant)


if __name__ == '__main__':

    # Obtain the arguments from CLI
    key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                {'name': 'contract', 'help': 'Contract name'}
    ]
    opt_args = [{'flag': 's', 'name': 'scope', 'default': DEFAULT_SCOPE, 'help': 'Represents the scope of this contract.'},
                {'flag': 'n', 'name': 'subject_name', 'help': 'Name of a subject in the contract.'},
                {'flag': 'r', 'name': 'reverse_filter_ports', 'dest': 'revFltPorts', 'help': 'Enables the filter to apply on both ingress and egress traffic.'},
                {'flag': 'Q', 'name': 'QoS_class', 'dest': 'prio', 'help': 'The priority level of a sub application running behind an endpoint group'},
                {'flag': 'f', 'name': 'filter_name', 'help': 'The applied filter'}
    ]

    try:
        host_name, user_name, password, args = set_cli_argparse('Create a Contract.', key_args, opt_args)
        tenant_name = args.pop('tenant')
        contract_name = args.pop('contract')
        optional_args = args

    except SystemExit:

        if check_if_requesting_help(sys.argv, opt_args):
            sys.exit('Help Page')

        try:
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            tenant_name = data['tenant']
            contract_name = data['contract']
            optional_args = data['optional_args']
        except (IOError, KeyError, TypeError, IndexError):
            if len(sys.argv)>1:
                print 'Invalid input arguments.'
            host_name, user_name, password = input_login_info()
            tenant_name = input_tenant_name()
            contract_name = input_key_args()
            optional_args = input_optional_args(contract_name)

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_contract(modir, tenant_name, contract_name,
                    args_from_CLI=optional_args)

    modir.logout()



