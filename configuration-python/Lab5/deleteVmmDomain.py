from cobra.model.vmm import DomP
from createVmmDomain import input_key_args

from utility import *


def delete_vmm_domain(modir, vm_provider, vmm_domain_name):

    vmm_domp = modir.lookupByDn('uni/vmmp-' + vm_provider + '/dom-' + vmm_domain_name)
    if isinstance(vmm_domp, DomP):
        vmm_domp.delete()
    else:
        print 'There is no VMM Domain', vmm_domain_name, 'in', vm_provider
        return
    print_query_xml(vmm_domp)
    commit_change(modir, vmm_domp)

if __name__ == '__main__':

    try:
        host_name, user_name, password, vm_provider, vmm_domain_name = sys.argv[1:6]
    except ValueError:
        host_name, user_name, password = input_login_info()
        vm_provider, vmm_domain_name = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    if vm_provider not in ['VMware', 'Microsoft']:
        print 'VM provider has to be either be \"VMware\" or \"Microsoft\"'
    else:
        delete_vmm_domain(modir, vm_provider, vmm_domain_name)

    modir.logout()


