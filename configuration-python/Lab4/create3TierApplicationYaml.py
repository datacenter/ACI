from createApplication import create_application
from createApplicationEPG import create_application_epg
from connectEpgContract import connect_epg_contract

from utility import *


if __name__ == '__main__':

    try:
        data = read_config_yaml_file(sys.argv[1], login_info=False)
    except IOError:
        print 'No such file or directory:', sys.argv[1]
        sys.exit()
    else:
        host_name, user_name, password = get_login_info(data)
        tenant_name = data['tenant']
        application = data['application']
    modir = apic_login(host_name, user_name, password)

    # create application
    create_application(modir, tenant_name, application)
    # create application EPG
    for epg in data['application_epg']:
        create_application_epg(modir, tenant_name, application, epg['name'], bridge_domain=epg['bridge_domain'])

    # Provide contracts between these EPGs
    for con in data['applied_contracts']:
        connect_epg_contract(modir, tenant_name, application, con['applied_epg'], con['type'], con['name'])

    modir.logout()