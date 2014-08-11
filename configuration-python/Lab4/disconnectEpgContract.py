import sys
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import AEPg, RsCons, RsProv
from cobra.model.vz import BrCP

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


def disconnect_epg_contract(modir, tenant_name, application_name, epg_name, contract_type, contract_name):
    """Take out a consumed/provided contract from an EPG"""
    vz_brcp = modir.lookupByDn('uni/tn-' + tenant_name + '/brc-' + contract_name)
    if not isinstance(vz_brcp, BrCP):
        print 'There is no contract called', contract_name, 'in tenant', tenant_name, '.'
        return

    fv_aepg = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name + '/epg-' + epg_name)
    if isinstance(fv_aepg, AEPg):
        if contract_type.lower() == 'consumed':
            fv = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name + '/epg-' + epg_name + '/rscons-' + contract_name)
        elif contract_type.lower() == 'provided':
            fv = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name + '/epg-' + epg_name + '/rsprov-' + contract_name)
        else:
            print 'Contract_type is either \"consumed\" or \"provided\".'
            return
        if isinstance(fv, RsCons) or isinstance(fv, RsProv):
            fv.delete()
        else:
            print 'Contract', contract_name, 'is not connected to EPG', epg_name, '.'
            return
    else:
        print 'Wrong path! Please check if EPG', epg_name, 'is in application', application_name, 'in tenant', tenant_name, '.'
        return

    print toXMLStr(fv, prettyPrint=True)
    commit_change(modir, fv)

if __name__ == '__main__':

    try:
        host_name, user_name, password, tenant_name, application_name, epg_name, contract_type, contract_name = sys.argv[1:9]
    except ValueError:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <application_name> <EPG_name> <contract_type> <contract_name>'
        sys.exit()

    modir = apic_login(host_name, user_name, password)
    disconnect_epg_contract(modir, tenant_name,  application_name, epg_name, contract_type, contract_name)

    modir.logout()


