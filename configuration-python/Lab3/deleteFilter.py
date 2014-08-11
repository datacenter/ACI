#!/usr/bin/env python

import sys
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.vz import Filter

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


def delete_filter(modir, tenant_name, filter_name):

    # Check if the filter exists or not. If yes, delete it.
    fv_ct = modir.lookupByDn('uni/tn-' + tenant_name + '/flt-' + filter_name)
    if isinstance(fv_ct, Filter):
        fv_ct.delete()
    else:
        print 'There is no filter called', filter_name, 'in tenant' , tenant_name, '.'
        return

    print toXMLStr(fv_ct, prettyPrint=True)

    commit_change(modir, fv_ct)


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <filter_name>'
        sys.exit()
    else:
        hostname, username, password, tenant_name, filter_name = sys.argv[1:]
        modir = apic_login(hostname, username, password)
        delete_filter(modir, tenant_name, filter_name)
        modir.logout()
