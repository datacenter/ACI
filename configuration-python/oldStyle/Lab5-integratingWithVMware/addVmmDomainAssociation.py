from cobra.model.fv import AEPg, RsDomAtt

from utility import *


def input_key_args(msg='\nAssociating EPG to vCenter Domain:'):
    print msg
    args = []
    args.append(get_raw_input("EPG (required): ", required=True))
    args.append(get_raw_input("vCenter Domain (required): ", required=True))
    return args


def input_optional_args(*args):
    args = {}
    args['deployment_immediacy'] = get_optional_input('Deploy Immediacy (default: "lazy")', ['immediate(i)', 'lazy(l)'])
    args['resolution_immediacy'] = get_optional_input('Resolution Immediacy (default: "lazy")', ['immediate(i)', 'lazy(l)'])
    return args


def add_vmm_domain_association(modir, tenant_name, application, epg, vmm_domain, **args):
    fv_epg = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application + '/epg-' + epg)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    if isinstance(fv_epg, AEPg):
        fv_rsdomatt = RsDomAtt(fv_epg, 'uni/vmmp-VMware/dom-' + vmm_domain,
                               instrImedcy=get_value(args, 'deployment_immediacy', 'lazy'),
                               resImedcy=get_value(args, 'resolution_immediacy', 'lazy'))
    else:
        print 'Fail to find EPG', epg, 'Please make sure you have the EPG in application', application
        return

    print_query_xml(fv_epg)
    commit_change(modir, fv_epg)

if __name__ == '__main__':

    # Obtain the arguments from CLI
    key_args = [{'name': 'tenant', 'help': 'Tenant Name'},
                {'name': 'application', 'help': 'Application Name'},
                {'name': 'epg', 'help': 'EPG Name'},
                {'name': 'vmm_domain', 'help': 'vCenter Domain Name'}
    ]
    opt_args = [{'flag': 'd', 'name': 'deployment_immediacy', 'dest': 'lazy', 'help': 'Deployment Immediacy.'},
                {'flag': 'r', 'name': 'resolution_immediacy', 'dest': 'lazy', 'help': 'rResolution Immediacy.'}
    ]

    try:
        host_name, user_name, password, args = set_cli_argparse('Associate a VMM domain to an EPG.', key_args, opt_args)
        tenant_name = args.pop('tenant')
        application = args.pop('application')
        epg = args.pop('epg')
        vmm_domain = args.pop('vmm_domain')
        optional_args = args

    except SystemExit:

        if check_if_requesting_help(sys.argv, opt_args):
            sys.exit('Help Page')

        if len(sys.argv)>1:
            print 'Invalid input arguments.'

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        application = input_application_name()
        epg, vmm_domain = input_key_args()
        optional_args = input_optional_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    add_vmm_domain_association(modir, tenant_name, application, epg, vmm_domain, args_from_CLI=optional_args)

    modir.logout()


