import sys
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import BD

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


def delete_bridge_domain(modir, tenant_name, bridge_domain):
    """Delete a bridge domain"""
    fv_bd = modir.lookupByDn('uni/tn-' + tenant_name + '/BD-' + bridge_domain)
    if isinstance(fv_bd, BD):
        fv_bd.delete()
    else:
        print 'Bridge Domain', bridge_domain, 'does not existed.'
        return

    print toXMLStr(fv_bd, prettyPrint=True)

    commit_change(modir, fv_bd)

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <bridge_domain>'
        sys.exit()
    else:
        hostname, username, password, tenant_name, bridge_domain = sys.argv[1:]
        modir = apic_login(hostname, username, password)
        delete_bridge_domain(modir, tenant_name, bridge_domain)
        modir.logout()
