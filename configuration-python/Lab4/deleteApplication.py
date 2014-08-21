from cobra.model.fv import Ap
from createApplication import input_key_args

from utility import *


def delete_application(modir, tenant_name, application_name):
    """Delete an application profile"""
    fv_ap = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name)
    if isinstance(fv_ap, Ap):
        fv_ap.delete()
    else:
        print 'There is no application called', application_name, 'in tenant', tenant_name, '.'
        return

    print toXMLStr(fv_ap, prettyPrint=True)

    commit_change(modir, fv_ap)


if __name__ == '__main__':
    try:
        hostname, username, password, tenant_name, application_name = sys.argv[1:]
    except ValueError:
        hostname, username, password = input_login_info()
        tenant_name = input_tenant_name()
        application_name = input_key_args()

    modir = apic_login(hostname, username, password)
    delete_application(modir, tenant_name, application_name)
    modir.logout()
