from cobra.model.vmm import DomP, UsrAccP

from createVmmDomain import input_key_args as input_vmm_domian_args

from utility import *


def input_key_args(msg='\nPlease input vCenter Credential info:'):
    print msg
    args = []
    args.append(get_raw_input("Profile Name (required): ", required=True))
    args.append(get_raw_input("User Name (required): ", required=True))
    args.append(get_raw_input("Password (required): ", required=True))
    return args


def create_vcenter_credential(modir, vm_provider, vmm_domain_name, profile_name, username, password):
    vmm_domp = modir.lookupByDn('uni/vmmp-' + vm_provider + '/dom-' + vmm_domain_name)
    if isinstance(vmm_domp, DomP):
        vmm_usraccp = UsrAccP(vmm_domp, profile_name, usr=username, pwd=password)

    else:
        print 'There is no VMM Domain', vmm_domain_name, 'in', vm_provider
        return

    print_query_xml(vmm_domp)
    commit_change(modir, vmm_domp)

if __name__ == '__main__':

    # Obtain the key parameters.
    try:
        host_name, user_name, password, vm_provider, vmm_domain_name, profile_name, username, pw = sys.argv[1:9]
    except ValueError:
        host_name, user_name, password = input_login_info()
        vm_provider, vmm_domain_name = input_vmm_domian_args()
        profile_name, username, pw = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    if vm_provider not in ['VMware', 'Microsoft']:
        print 'VM provider has to be either be \"VMware\" or \"Microsoft\"'
    else:
        create_vcenter_credential(modir, vm_provider, vmm_domain_name, profile_name, username, pw)
    modir.logout()


