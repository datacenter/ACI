from cobra.model.fv import Ap, AEPg
from createApplicationEPG import input_key_args

from utility import *


def delete_application_epg(modir, tenant_name, application_name, epg_name):
    """Delete an EPG"""
    fv_ap = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name)
    if isinstance(fv_ap, Ap):
        fv_aepg = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name + '/epg-' + epg_name)
        if isinstance(fv_aepg, AEPg):
            fv_aepg.delete()
        else:
            print 'There is no application epg called', epg_name, 'in application', application_name, '.'
            return
    else:
        print 'There is no application called', application_name, 'in tenant', tenant_name, '.'
        return

    print_query_xml(fv_aepg)

    commit_change(modir, fv_aepg)


if __name__ == '__main__':

    key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                {'name': 'application', 'help': 'Application name'},
                {'name': 'epg', 'help': 'Application EPG name'}
    ]

    try:
        host_name, user_name, password, args = set_cli_argparse('Delete an Application EPG.', key_args)
        tenant_name = args.pop('tenant')
        application_name = args.pop('application')
        epg_name = args.pop('epg')

    except SystemExit:

        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        if len(sys.argv)>1:
            print 'Invalid input arguments.'

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        application_name = input_application_name()
        epg_name = input_key_args()

    modir = apic_login(host_name, user_name, password)
    delete_application_epg(modir, tenant_name, application_name, epg_name)
    modir.logout()