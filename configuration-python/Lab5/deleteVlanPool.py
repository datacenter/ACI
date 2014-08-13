import sys
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fvns import VlanInstP

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


def delete_vlan_pool(modir, vlan_name, allocation_mode):

    # Query to the VLAN pool.
    fvns_vlaninstp = modir.lookupByDn('uni/infra/vlanns-' + vlan_name + '-' + allocation_mode)

    if isinstance(fvns_vlaninstp, VlanInstP):
        # delete the VLAN
        fvns_vlaninstp.delete()
    else:
        print 'There is no VLAN', vlan_name, '(', allocation_mode, ').'
        return

    print toXMLStr(fvns_vlaninstp, prettyPrint=True)
    commit_change(modir, fvns_vlaninstp)

if __name__ == '__main__':

    # Obtain the key parameters.
    try:
        host_name, user_name, password, vlan_name, allocation_mode = sys.argv[1:6]
    except ValueError:
        print 'Usage:', __file__, '<hostname> <username> <password> <vlan_name> <allocation_mode>'
        sys.exit()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    if allocation_mode.lower() not in ['dynamic', 'static']:
        print 'VM provider has to be either be \"dynamic\" or \"static\"'
    else:
        delete_vlan_pool(modir, vlan_name, allocation_mode.lower())

    modir.logout()


