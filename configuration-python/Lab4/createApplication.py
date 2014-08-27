from cobra.model.fv import Ap

from utility import *


def input_optional_args():
    args = {}
    args['prio'] = get_optional_input('QoS Class (default: "unspecified"): ', ['level1', 'level2', "level3", "unspecified"])
    return args


def create_application(modir, tenant_name, application_name, **args):
    """Create an application profile"""

    # Query a tenant
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    if isinstance(fv_tenant, Tenant):
        # Create the Application profile
        fv_ap = Ap(fv_tenant, application_name,
                   prio=get_value(args, 'prio', 'unspecified').lower())
    else:
        print 'Tenant', tenant_name, 'does not exist. Please create a tenant first.'
        return

    print_query_xml(fv_tenant)
    commit_change(modir, fv_tenant)

if __name__ == '__main__':

    opts = sys.argv[1:]
    opts.reverse()

    # Obtain the key parameters.
    keys = []
    while len(opts) > 0 and opts[len(opts)-1][0] != '-':
        keys.append(opts.pop())
    opts.reverse()
    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                    {'name': 'application', 'help': 'Application name'}
        ]
        opt_args = [{'flag': 'Q', 'name': 'QoS_class', 'dest': 'prio', 'help': 'The priority level of a sub application running behind an endpoint group'}
        ]

        host_name, user_name, password, args = set_cli_argparse('Create a Application.', key_args, opt_args)
        tenant_name = args.pop('tenant')
        application_name = args.pop('application')
        optional_args = args

    except:

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        application_name = input_application_name()
        optional_args = input_optional_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_application(modir, tenant_name, application_name, args_from_CLI=optional_args)

    modir.logout()


