from cobra.model.fv import Ap, AEPg
from createApplication import input_key_args as input_application_name
from createApplicationEPG import input_key_args

from utility import *


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
    try:
        hostname, username, password, tenant_name, application_name, epg_name = sys.argv[1:]
    except ValueError:
        hostname, username, password = input_login_info()
        tenant_name = input_tenant_name()
        application_name = input_application_name()
        epg_name = input_key_args()

    modir = apic_login(hostname, username, password)
    delete_application_epg(modir, tenant_name, application_name, epg_name)
    modir.logout()