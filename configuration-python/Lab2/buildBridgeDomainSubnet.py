import sys
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import BD
from cobra.model.fv import Ctx
from cobra.model.fv import RsCtx
from cobra.model.fv import Subnet

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


def build_bridge_domain_subnet(modir, tenant_name, bridge_domain, subnet_ip, network_name):
    """Build a bridge domain and its associated subnet"""

    # Query to a tenant
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)

    # Create a bridge domain
    fv_bd = BD(fv_tenant, bridge_domain)

    # Create a subnet
    fv_subnet = Subnet(fv_bd, subnet_ip)

    # Connect the bridge domain to a network
    if isinstance(modir.lookupByDn('uni/tn-' + tenant_name + '/ctx-' + network_name), Ctx):
        fv_rsctx = RsCtx(fv_bd, tnFvCtxName=network_name)
    else:
        print 'Network', network_name, 'does not existe.'

    print toXMLStr(fv_tenant, prettyPrint=True)
    commit_change(modir, fv_tenant)

if __name__ == '__main__':
    if len(sys.argv) != 8:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <bridge_domain> <subnet_ip> <network_name>'
        sys.exit()
    else:
        hostname, username, password, tenant_name, bridge_domain, subnet_ip, network_name = sys.argv[1:]
        modir = apic_login(hostname, username, password)
        build_bridge_domain_subnet(modir, tenant_name, bridge_domain, subnet_ip, network_name)
        modir.logout()
