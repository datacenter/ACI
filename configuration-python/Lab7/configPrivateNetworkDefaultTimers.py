from cobra.model.fv import Ctx, RsBgpCtxPol, RsOspfCtxPol, RsCtxToEpRet, RsCtxMonPol

from utility import *

# use "None" to delete the configuration

def input_key_args(msg='Please input Private L3 Network info:'):
    print msg
    return get_raw_input("Private L3 Network (required): ", required=True)


def input_optional_args(*arg):
    args = {}
    args['bgp'] = get_raw_input("BGP Timers (default: 'None'): ")
    args['ospf'] = get_raw_input("OSPF Timers (default: 'None'): ")
    args['eprp'] = get_raw_input("End Point Retention Policy (default: 'None'): ")
    args['mp'] = get_raw_input("Monitoring Policy (default: 'None'): ")
    return args


def config_private_network_default_timers(modir, tenant_name, private_network, **args):
    fv_ctx = modir.lookupByDn('uni/tn-' + tenant_name + '/ctx-' + private_network)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args

    if isinstance(fv_ctx, Ctx):
        if 'bgp' in args and args['bgp'] != '':
            fv_rsbgpctxpol = RsBgpCtxPol(fv_ctx, tnBgpCtxPolName='' if args['bgp'].lower() == 'none' else args['bgp'])
        if 'ospf' in args and args['ospf'] != '':
            fv_rsospfctxpol = RsOspfCtxPol(fv_ctx, tnOspfCtxPolName='' if args['ospf'].lower() == 'none' else args['ospf'])
        if 'eprp' in args and args['eprp'] != '':
            fv_rsctxtoepret = RsCtxToEpRet(fv_ctx, tnFvEpRetPolName='' if args['eprp'].lower() == 'none' else args['eprp'])
        if 'mp' in args and args['mp'] != '':
            fv_rsctxmonpol = RsCtxMonPol(fv_ctx, tnMonEPGPolName='' if args['mp'].lower() == 'none' else args['mp'])
    else:
        print 'Private L3 Network', private_network, 'does not existed.'
        return

    print_query_xml(fv_ctx)

    commit_change(modir, fv_ctx)


if __name__ == '__main__':

    # Obtain the arguments from CLI
    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                    {'name': 'private_network', 'help': 'Private Network Name.'}
        ]
        opt_args = [{'flag': 'B', 'name': 'BGP Timer', 'dest': 'bgp', 'help': 'A relation to the BGP timer policy. This is an internal object.'},
                    {'flag': 'O', 'name': 'OSPF Timer', 'dest': 'ospf', 'help': 'A relation to the context-level OSPF timer policy. This is an internal object.'},
                    {'flag': 'e', 'name': 'End Point Retention Policy', 'dest': 'eprp', 'help': 'A relation to an endpoint retention policy. This is an internal object.'},
                    {'flag': 'm', 'name': 'Monitoring Policy', 'dest': 'mp', 'help': 'A relation to the monitoring policy model for the endpoint group semantic scope. This is an internal object.'}
        ]

        host_name, user_name, password, args = set_cli_argparse('Set Setting for Private Network.', key_args, opt_args)
        tenant_name = args.pop('tenant')
        private_network = args.pop('private_network')
        optional_args = args

    except SystemExit:

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        private_network = input_key_args()
        optional_args = input_optional_args()
    modir = apic_login(host_name, user_name, password)
    config_private_network_default_timers(modir, tenant_name, private_network, args_from_CLI=optional_args)
    modir.logout()
