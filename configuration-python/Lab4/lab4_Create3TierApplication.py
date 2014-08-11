import sys
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from createApplication import create_application
from createApplicationEPG import create_application_epg
from connectEpgContract import connect_epg_contract

def apic_login(hostname, username, password):
    epoint = EndPoint(hostname, secure=False, port=80)
    lsess = LoginSession(username, password)
    modir = MoDirectory(epoint, lsess)
    modir.login()
    return modir


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
    if len(sys.argv) != 6:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <application_name>'
        sys.exit()
    else:
        hostname, username, password, tenant_name, application_name = sys.argv[1:]
        modir = apic_login(hostname, username, password)
        lab4(modir, tenant_name, application_name)
        modir.logout()
