from cobra.model.vmm import DomP, UsrAccP

from createVmmDomain import input_key_args as input_vmm_domian_args

from utility import *


def input_key_args(msg='\nPlease input vCenter Credential info:', from_delete_function=False):
    print msg
    args = []
    args.append(get_raw_input("Profile Name (required): ", required=True))
    if not from_delete_function:
        args.append(get_raw_input("User Name (required): ", required=True))
        args.append(get_raw_input("Password (required): ", required=True))
    return args


def create_vcenter_credential(modir, vm_provider, vmm_domain_name, profile_name, vm_user, vm_pw):
    vmm_domp = modir.lookupByDn('uni/vmmp-' + vm_provider + '/dom-' + vmm_domain_name)
    if isinstance(vmm_domp, DomP):
        vmm_usraccp = UsrAccP(vmm_domp, profile_name, usr=vm_user, pwd=vm_pw)

    else:
        print 'There is no VMM Domain', vmm_domain_name, 'in', vm_provider
        return

    print_query_xml(vmm_domp)
    commit_change(modir, vmm_domp)

if __name__ == '__main__':

    # Obtain the key parameters.
    try:
        key_args = [{'name': 'provider', 'help': 'VM Provider'},
                    {'name': 'domain', 'help': 'vCenter Domain Name'},
                    {'name': 'profile', 'help': 'Profile Name'},
                    {'name': 'vm_user', 'help': 'VMM Credential User Name'},
                    {'name': 'vm_password', 'help': 'VMM Credential Password'}
        ]

        host_name, user_name, password, args = set_cli_argparse('Create a vCenter Credential.', key_args)
        vm_provider = args.pop('provider')
        vmm_domain_name = args.pop('domain')
        profile_name = args.pop('profile')
        vm_user = args.pop('vm_user')
        vm_pw = args.pop('vm_password')

    except:

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        vm_provider, vmm_domain_name = input_vmm_domian_args()
        profile_name, vm_user, vm_pw = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    if vm_provider not in ['VMware', 'Microsoft']:
        print 'VM provider has to be either be \"VMware\" or \"Microsoft\"'
    else:
        create_vcenter_credential(modir, vm_provider, vmm_domain_name, profile_name, vm_user, vm_pw)
    modir.logout()


