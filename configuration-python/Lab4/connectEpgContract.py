import sys
import getopt
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import AEPg, RsCons, RsProv
from cobra.model.vz import BrCP

from cobra.internal.codec.xmlcodec import toXMLStr

from IPython import embed

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


def connect_epg_contract(modir, tenant_name, application_name, epg_name, contract_type, contract_name):
    """Assign a consumed/provided contract to an EPG"""

    # Check if the contract exist. If not, return.
    vz_brcp = modir.lookupByDn('uni/tn-' + tenant_name + '/brc-' + contract_name)
    if not isinstance(vz_brcp, BrCP):
        print 'There is no contract called', contract_name, 'in tenant', tenant_name, '.'
        return

    # Check if the EPG exist.
    fv_aepg = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name + '/epg-' + epg_name)
    if isinstance(fv_aepg, AEPg):

        # Check the contract type, consumed or provided.
        if contract_type.lower() == 'consumed':
            # Add a consumed contract to EPG
            fv_rscons = RsCons(fv_aepg, contract_name)
        elif contract_type.lower() == 'provided':
            # Add a provided contract to EPG
            fv_rsprov = RsProv(fv_aepg, contract_name)
        else:
            print 'Contract_type is either \"consumed\" or \"provided\".'
            return
    else:
        print 'Wrong path! Please check if EPG', epg_name, 'is in application', application_name, 'in tenant', tenant_name, '.'
        return

    print toXMLStr(fv_aepg, prettyPrint=True)
    commit_change(modir, fv_aepg)

if __name__ == '__main__':

    try:
        host_name, user_name, password, tenant_name, application_name, epg_name, contract_type, contract_name = sys.argv[1:9]
    except ValueError:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <application_name> <EPG_name> <contract_type> <contract_name>'
        sys.exit()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    connect_epg_contract(modir, tenant_name,  application_name, epg_name, contract_type, contract_name)

    modir.logout()


