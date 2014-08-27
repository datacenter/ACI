from cobra.model.fv import Ap

from utility import *


def delete_application(modir, tenant_name, application_name):
    """Delete an application profile"""
    fv_ap = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name)
    if isinstance(fv_ap, Ap):
        fv_ap.delete()
    else:
        print 'There is no application called', application_name, 'in tenant', tenant_name, '.'
        return

    print_query_xml(fv_ap)

    commit_change(modir, fv_ap)


if __name__ == '__main__':

    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                    {'name': 'application', 'help': 'Application name'}
        ]

        host_name, user_name, password, args = set_cli_argparse('Delete a Application.', key_args)
        tenant_name = args.pop('tenant')
        application_name = args.pop('application')

    except: #?error

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        application_name = input_application_name()

    modir = apic_login(host_name, user_name, password)
    delete_application(modir, tenant_name, application_name)
    modir.logout()
