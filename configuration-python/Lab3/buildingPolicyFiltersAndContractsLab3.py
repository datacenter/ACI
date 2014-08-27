from createFilter import create_filter
from createContract import create_contract

from utility import *


def lab3(modir, tenant_name):
    """Following the lab guide, we create three filters and three contracts"""

    # Create filters
    create_filter(modir, tenant_name, 'Web_Filter', ether_type='ip',
                  ip_protocol='tcp', destination_port_from='http',
                  destination_port_to='http')
    create_filter(modir, tenant_name, 'App_Filter', ether_type='ip',
                  ip_protocol='tcp', destination_port_from='1433',
                  destination_port_to='1433')
    create_filter(modir, tenant_name, 'DB_Filter', ether_type='ip',
                  ip_protocol='tcp', destination_port_from='1521',
                  destination_port_to='1521')
    # Create contracts
    create_contract(modir, tenant_name, 'Web_Con', subject_name='web_subj',
                    filter_name='Web_Filter')
    create_contract(modir, tenant_name, 'App_Con', subject_name='app_subj',
                    filter_name='App_Filter')
    create_contract(modir, tenant_name, 'DB_Con', subject_name='db_subj',
                    filter_name='DB_Filter')


if __name__ == '__main__':

    try:
        key_args = [{'name': 'tenant', 'help': 'Tenant name'}]
        host_name, user_name, password, args = set_cli_argparse('Create three filters and three contracts.', key_args)
        tenant_name = args.pop('tenant')

    except SystemExit:

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()

    modir = apic_login(host_name, user_name, password)
    lab3(modir, tenant_name)
    modir.logout()
