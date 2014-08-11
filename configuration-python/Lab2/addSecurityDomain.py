import sys
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.aaa import DomainRef

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


def add_security_domain(modir, tenant_name, security_domain):
    """Add security domain to tenant"""
    # to query the tenant
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)
    aaa_domain_ref = DomainRef(fv_tenant, security_domain)

    #print out in XML format
    print toXMLStr(fv_tenant, prettyPrint=True)

    commit_change(modir, fv_tenant)


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <security_domain>'
        sys.exit()
    else:
        hostname, username, password, tenant_name, security_domain = sys.argv[1:]
        modir = apic_login(hostname, username, password)
        add_security_domain(modir, tenant_name, security_domain)
        modir.logout()
    print('end')