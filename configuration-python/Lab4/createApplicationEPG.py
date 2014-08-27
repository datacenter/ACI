from cobra.model.fv import Ap, AEPg, RsBd

from utility import *


def input_key_args(msg='\nPlease input Application EPG info:'):
    print msg
    return get_raw_input("EPG Name (required): ", required=True)


def input_optional_args(*args):
    args = {}
    args['bridge_domain'] = get_raw_input('Bridge Domain (default: None): ')
    args['prio'] = get_optional_input('QoS Class (default: "unspecified"): ', ['level1', 'level2', "level3", "unspecified"])
    return args


def create_application_epg(modir, tenant_name, application_name, epg_name, **args):
    """Create an EPG"""

    # Query the application
    fv_ap = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    if isinstance(fv_ap, Ap):
        # Create an EPG
        fv_aepg = AEPg(fv_ap, epg_name,
                       prio=get_value(args, 'prio', 'unspecified').lower())

        # Provide bridge_domain to the EPG.
        if 'bridge_domain' in args.keys():
            fv_rsbd = RsBd(fv_aepg, tnFvBDName=args['bridge_domain'])
    else:
        print 'There is no application', application_name, 'in tenant', tenant_name, '. Please create an application.'
        return

    print_query_xml(fv_ap)
    commit_change(modir, fv_ap)

if __name__ == '__main__':

    # Obtain the arguments from CLI
    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                    {'name': 'application', 'help': 'Application name'},
                    {'name': 'epg', 'help': 'Application EPG name'}
        ]
        opt_args = [{'flag': 'b', 'name': 'bridge_domain', 'help': 'A relation to the bridge domain associated to this endpoint group.'},
                    {'flag': 'Q', 'name': 'QoS_class', 'dest': 'prio', 'help': 'The priority level of a sub application running behind an endpoint group.'}
        ]

        host_name, user_name, password, args = set_cli_argparse('Create an Application EPG.', key_args, opt_args)
        tenant_name = args.pop('tenant')
        application_name = args.pop('application')
        epg_name = args.pop('epg')
        optional_args = args

    except SystemExit:

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        application_name = input_application_name()
        epg_name = input_key_args()
        optional_args = input_optional_args()



    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_application_epg(modir, tenant_name, application_name, epg_name, args_from_CLI=optional_args)

    modir.logout()


