from cobra.model.fv import RsDomAtt
from addVmmDomainAssociation import input_key_args
from utility import *


def add_vmm_domain_association(modir, tenant_name, application, epg, vmm_domain):
    fv_rsdomatt = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application + '/epg-' + epg + '/rsdomAtt-[uni/vmmp-VMware/dom-' + vmm_domain + ']')
    if isinstance(fv_rsdomatt, RsDomAtt):
        fv_rsdomatt.delete()
    else:
        print 'VMM Domain', vmm_domain, ' has been added to EPG', epg
        return

    print_query_xml(fv_rsdomatt)
    commit_change(modir, fv_rsdomatt)

if __name__ == '__main__':

    # Obtain the key parameters.
    try:
        host_name, user_name, password, tenant_name, application, epg, vmm_domain = sys.argv[1:8]
    except ValueError:
        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        application = input_application_name()
        epg, vmm_domain = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    add_vmm_domain_association(modir, tenant_name, application, epg, vmm_domain)

    modir.logout()


