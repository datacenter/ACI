from createFilter import create_filter
from createContract import create_contract

from utility import *


if __name__ == '__main__':
    try:
        data = read_config_yaml_file(sys.argv[1], login_info=False)
    except IOError:
        print 'No such file or directory:', sys.argv[1]
        sys.exit()
    else:
        host, user, password = get_login_info(data)
        tenant = data['tenant']
    modir = apic_login(host, user, password)

    # Create filters
    for filter in data['filters']:
        create_filter(modir, tenant, filter['name'],
                      ether_type=filter['ether_type'],
                      ip_protocol=filter['ip_protocol'],
                      destination_port_from=filter['destination_port_from'],
                      destination_port_to=filter['destination_port_to'])
    # Create contracts
    for contract in data['contracts']:
        create_contract(modir, tenant, contract['name'],
                        subject_name=contract['subject'],
                        filter_name=contract['filter'])


    modir.logout()
