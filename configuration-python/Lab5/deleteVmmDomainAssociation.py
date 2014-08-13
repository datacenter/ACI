import sys
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import RsDomAtt

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


def add_vmm_domain_association(modir, tenant_name, application, epg, vmm_domain):
    fv_rsdomatt = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application + '/epg-' + epg + '/rsdomAtt-[uni/vmmp-VMware/dom-' + vmm_domain + ']')
    if isinstance(fv_rsdomatt, RsDomAtt):
        fv_rsdomatt.delete()
    else:
        print 'VMM Domain', vmm_domain, ' has been added to EPG', epg
        return

    print toXMLStr(fv_rsdomatt, prettyPrint=True)
    commit_change(modir, fv_rsdomatt)

if __name__ == '__main__':

    # Obtain the key parameters.
    try:
        host_name, user_name, password, tenant_name, application, epg, vmm_domain = sys.argv[1:8]
    except ValueError:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <application> <epg> <vmm_domain>'
        sys.exit()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    add_vmm_domain_association(modir, tenant_name, application, epg, vmm_domain)

    modir.logout()


