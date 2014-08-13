import sys
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.vmm import DomP, CtrlrP

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


def delete_vcenter_controller(modir, vm_provider, vmm_domain_name, controller_name):
    vmm_domp = modir.lookupByDn('uni/vmmp-' + vm_provider + '/dom-' + vmm_domain_name)
    if isinstance(vmm_domp, DomP):
        CtrlrP(vmm_domp, controller_name).delete()
    else:
        print 'There is no VMM Domain', vmm_domain_name, 'in', vm_provider
        return

    print toXMLStr(vmm_domp, prettyPrint=True)
    commit_change(modir, vmm_domp)


if __name__ == '__main__':

    # Obtain the key parameters.
    try:
        host_name, user_name, password, vm_provider, vmm_domain_name, controller_name = sys.argv[1:7]
    except ValueError:
        print 'Usage:', __file__, '<hostname> <username> <password> <vm_provider> <vmm_domain_name> <controller_name>'
        sys.exit()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    if vm_provider not in ['VMware', 'Microsoft']:
        print 'VM provider has to be either be \"VMware\" or \"Microsoft\"'
    else:
        delete_vcenter_controller(modir, vm_provider, vmm_domain_name, controller_name)

    modir.logout()


