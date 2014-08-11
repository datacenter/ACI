import sys
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Ctx

from cobra.internal.codec.xmlcodec import toXMLStr


def apic_login(hostname, username, password):
    """Login to APIC"""
    epoint = EndPoint(hostname, secure=False, port=80)
    lsess = LoginSession(username, password)
    modir = MoDirectory(epoint, lsess)
    modir.login()
    return modir


def commit_change(modir, changed_object):
    """Commit the changes to APIC"""
    config_req = ConfigRequest()
    config_req.addMo(changed_object)
    modir.commit(config_req)


def build_private_l3_network(modir, tenant_name, private_l3_network):
    """Build a private L3 network"""

    # Query a tenant
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)

    # create a private network
    fv_ctx = Ctx(fv_tenant, private_l3_network)

    print toXMLStr(fv_tenant, prettyPrint=True)

    commit_change(modir, fv_tenant)

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <network_name>'
        sys.exit()
    else:
        hostname, username, password, tenant_name, private_l3_network = sys.argv[1:]
        modir = apic_login(hostname, username, password)
        build_private_l3_network(modir, tenant_name, private_l3_network)
        modir.logout()
