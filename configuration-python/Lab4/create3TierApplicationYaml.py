from createApplication import create_application
from createApplicationEPG import create_application_epg
from connectEpgContract import connect_epg_contract

from utility import *


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Create a three tier application.')
    parser.add_argument('yaml', help='Imported yaml file.')
    args = vars(parser.parse_args())

    try:
        data = read_config_yaml_file(args['yaml'], login_info=False)
    except IOError:
        print 'No such file or directory:', sys.argv[1]
        sys.exit()
    else:
        host, user, password = get_login_info(data)
        tenant = data['tenant']
        application = data['application']
    modir = apic_login(host, user, password)

    # create application
    create_application(modir, tenant, application)
    # create application EPG
    for epg in data['application_epg']:
        create_application_epg(modir, tenant, application, epg['name'], bridge_domain=epg['bridge_domain'])

    # Provide contracts between these EPGs
    for con in data['applied_contracts']:
        connect_epg_contract(modir, tenant, application, con['applied_epg'], con['type'], con['name'])

    modir.logout()