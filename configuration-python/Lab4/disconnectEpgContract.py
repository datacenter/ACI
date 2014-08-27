from cobra.model.fv import AEPg, RsCons, RsProv
from cobra.model.vz import BrCP
from createApplicationEPG import input_key_args as input_application_epg_name
from connectEpgContract import input_key_args

from utility import *


def disconnect_epg_contract(modir, tenant_name, application_name, epg_name, contract_type, contract_name):
    """Take out a consumed/provided contract from an EPG"""
    vz_brcp = modir.lookupByDn('uni/tn-' + tenant_name + '/brc-' + contract_name)
    if not isinstance(vz_brcp, BrCP):
        print 'There is no contract called', contract_name, 'in tenant', tenant_name, '.'
        return

    fv_aepg = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name + '/epg-' + epg_name)
    if isinstance(fv_aepg, AEPg):
        if contract_type.lower() == 'consumed':
            fv = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name + '/epg-' + epg_name + '/rscons-' + contract_name)
        elif contract_type.lower() == 'provided':
            fv = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name + '/epg-' + epg_name + '/rsprov-' + contract_name)
        else:
            print 'Contract_type is either \"consumed\" or \"provided\".'
            return
        if isinstance(fv, RsCons) or isinstance(fv, RsProv):
            fv.delete()
        else:
            print 'Contract', contract_name, 'is not connected to EPG', epg_name, '.'
            return
    else:
        print 'Wrong path! Please check if EPG', epg_name, 'is in application', application_name, 'in tenant', tenant_name, '.'
        return

    print_query_xml(fv)
    commit_change(modir, fv)

if __name__ == '__main__':

    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                    {'name': 'application', 'help': 'Application name'},
                    {'name': 'epg', 'help': 'Epg name'},
                    {'name': 'contract', 'help': 'Contract name'},
                    {'name': 'type', 'help': 'Contract type'}
        ]

        host_name, user_name, password, args = set_cli_argparse('Un-apply a contract from an EPG.', key_args)
        tenant_name = args.pop('tenant')
        application_name = args.pop('application')
        epg_name = args.pop('epg')
        contract_name = args.pop('contract')
        contract_type = args.pop('type')
        optional_args = args

    except SystemExit:

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        application_name = input_application_name()
        epg_name = input_application_epg_name()
        contract_type, contract_name = input_key_args()

    modir = apic_login(host_name, user_name, password)
    disconnect_epg_contract(modir, tenant_name,  application_name, epg_name, contract_type, contract_name)

    modir.logout()


