from cobra.model.fv import AEPg, RsCons, RsProv
from cobra.model.vz import BrCP

from utility import *


def input_key_args(msg=''):
    print msg
    args = []
    args.append(get_raw_input("EPG Name (required): ", required=True))
    args.append(get_optional_input("Contract Type (required): ", ['provided(p)', 'consumed(c)']))
    args.append(get_raw_input("Contract Name (required): ", required=True))
    return args


def connect_epg_contract(modir, tenant_name, application_name, epg_name, contract_type, contract_name):
    """Assign a consumed/provided contract to an EPG"""

    # Check if the contract exist. If not, return.
    vz_brcp = modir.lookupByDn('uni/tn-' + tenant_name + '/brc-' + contract_name)
    if not isinstance(vz_brcp, BrCP):
        print 'There is no contract called', contract_name, 'in tenant', tenant_name, '.'
        return

    # Check if the EPG exist.
    fv_aepg = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name + '/epg-' + epg_name)
    if isinstance(fv_aepg, AEPg):

        # Check the contract type, consumed or provided.
        if contract_type.lower() == 'consumed':
            # Add a consumed contract to EPG
            fv_rscons = RsCons(fv_aepg, contract_name)
        elif contract_type.lower() == 'provided':
            # Add a provided contract to EPG
            fv_rsprov = RsProv(fv_aepg, contract_name)
        else:
            print 'Contract_type is either \"consumed\" or \"provided\".'
            return
    else:
        print 'Wrong path! Please check if EPG', epg_name, 'is in application', application_name, 'in tenant', tenant_name, '.'
        return

    print_query_xml(fv_aepg)
    commit_change(modir, fv_aepg)

if __name__ == '__main__':

    key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                {'name': 'application', 'help': 'Application name'},
                {'name': 'epg', 'help': 'Epg name'},
                {'name': 'contract', 'help': 'Contract name'},
                {'name': 'type', 'help': 'Contract type'}
    ]

    try:
        host_name, user_name, password, args = set_cli_argparse('Apply contract to an EPG.', key_args)
        tenant_name = args.pop('tenant')
        application_name = args.pop('application')
        epg_name = args.pop('epg')
        contract_name = args.pop('contract')
        contract_type = args.pop('type')
        optional_args = args

    except SystemExit:

        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        if len(sys.argv)>1:
            print 'Invalid input arguments.'

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        application_name = input_application_name()
        epg_name, contract_type, contract_name = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    connect_epg_contract(modir, tenant_name,  application_name, epg_name, contract_type, contract_name)

    modir.logout()


