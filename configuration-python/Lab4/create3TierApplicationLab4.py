from createApplication import create_application
from createApplicationEPG import create_application_epg
from connectEpgContract import connect_epg_contract

from utility import *


def lab4(modir, tenant_name, application_name):
    """Following the lab guide, we create 3Tiers application profile"""

    # Create a application profile
    create_application(modir, tenant_name, application_name)
    # Create three EPGs: Web_EPG, App_EPG and DB_EPG
    create_application_epg(modir, tenant_name, application_name, 'Web_EPG', bridge_domain=tenant_name+'_BD1')
    create_application_epg(modir, tenant_name, application_name, 'App_EPG', bridge_domain=tenant_name+'_BD1')
    create_application_epg(modir, tenant_name, application_name, 'DB_EPG', bridge_domain=tenant_name+'_BD1')
    # Provide contracts between these EPGs
    connect_epg_contract(modir, tenant_name, application_name, 'Web_EPG', 'provided', 'Web_Con')
    connect_epg_contract(modir, tenant_name, application_name, 'App_EPG', 'provided', 'App_Con')
    connect_epg_contract(modir, tenant_name, application_name, 'DB_EPG', 'provided', 'DB_Con')
    connect_epg_contract(modir, tenant_name, application_name, 'Web_EPG', 'consumed', 'App_Con')
    connect_epg_contract(modir, tenant_name, application_name, 'App_EPG', 'consumed', 'DB_Con')


if __name__ == '__main__':

    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                    {'name': 'application', 'help': 'Application name'}
        ]

        host_name, user_name, password, args = set_cli_argparse('Apply contract to an EPG.', key_args)
        tenant_name = args.pop('tenant')
        application_name = args.pop('application')
        optional_args = args

    except: #?error

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        application_name = input_application_name()

    modir = apic_login(host_name, user_name, password)
    lab4(modir, tenant_name, application_name)
    modir.logout()
