#!/usr/bin/env python

import sys
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Ap, AEPg

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


def delete_application_epg(modir, tenant_name, application_name, epg_name):
    """Delete an EPG"""
    fv_ap = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name)
    if isinstance(fv_ap, Ap):
        fv_aepg = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name + '/epg-' + epg_name)
        if isinstance(fv_aepg, AEPg):
            fv_aepg.delete()
        else:
            print 'There is no application epg called', epg_name, 'in application', application_name, '.'
            return
    else:
        print 'There is no application called', application_name, 'in tenant', tenant_name, '.'
        return

    print toXMLStr(fv_aepg, prettyPrint=True)

    commit_change(modir, fv_aepg)


if __name__ == '__main__':
    if len(sys.argv) != 7:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <application_name> <EPG_name>'
        sys.exit()
    else:
        hostname, username, password, tenant_name, application_name, epg_name = sys.argv[1:]
        modir = apic_login(hostname, username, password)
        delete_application_epg(modir, tenant_name, application_name, epg_name)
        modir.logout()
