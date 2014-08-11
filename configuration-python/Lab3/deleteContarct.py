#!/usr/bin/env python

import sys
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
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


def delete_contract(modir, tenant_name, contract_name):
    """Delete a contract"""

    # Check if the contract exists or not. If yes, delete it.
    vz_brcp = modir.lookupByDn('uni/tn-' + tenant_name + '/brc-' + contract_name)
    if isinstance(vz_brcp, BrCP):
        vz_brcp.delete()
    else:
        print 'There is no contract called', contract_name, 'in tenant' , tenant_name, '.'
        return

    print toXMLStr(vz_brcp, prettyPrint=True)

    commit_change(modir, vz_brcp)


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <contract_name>'
        sys.exit()
    else:
        hostname, username, password, tenant_name, contract_name = sys.argv[1:]
        modir = apic_login(hostname, username, password)
        delete_contract(modir, tenant_name, contract_name)
        modir.logout()
