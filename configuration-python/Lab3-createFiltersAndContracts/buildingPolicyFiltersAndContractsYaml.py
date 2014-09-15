from createFilter import create_filter
from createContract import create_contract

from utility import *


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Create three filters and three contracts.')
    parser.add_argument('yaml', help='Imported yaml file.')
    args = vars(parser.parse_args())

    try:
        data = read_config_yaml_file(args['yaml'], login_info=False)
    except IOError:
        print 'No such file or directory:', args['yaml']
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
                        subject_name=contract['subject_name'],
                        filter_name=contract['filter_name'])


    modir.logout()
