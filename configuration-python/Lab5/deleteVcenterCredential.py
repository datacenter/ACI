from cobra.model.vmm import UsrAccP
from createVmmDomain import input_key_args as input_vmm_domian_args
from createVcenterCredential import input_key_args

from utility import *


def delete_vcenter_credential(modir, vm_provider, vmm_domain_name, profile_name):
    vmm_usraccp = modir.lookupByDn('uni/vmmp-' + vm_provider + '/dom-' + vmm_domain_name + '/usracc-' + profile_name)
    if isinstance(vmm_usraccp, UsrAccP):
        vmm_usraccp.delete()
    else:
        print 'There is no vCenter credential', profile_name, 'in', vmm_domain_name
        return

    print_query_xml(vmm_usraccp)
    commit_change(modir, vmm_usraccp)

if __name__ == '__main__':

    # Obtain the key parameters.
    try:
        key_args = [{'name': 'provider', 'help': 'VM Provider'},
                    {'name': 'domain', 'help': 'vCenter Domain Name'},
                    {'name': 'profile', 'help': 'Profile Name'},
        ]

        host_name, user_name, password, args = set_cli_argparse('Delete a vCenter Credential.', key_args)
        vm_provider = args.pop('provider')
        vmm_domain_name = args.pop('domain')
        profile_name = args.pop('profile')

    except SystemExit:

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        vm_provider, vmm_domain_name = input_vmm_domian_args()
        profile_name = input_key_args(from_delete_function=True)[0]

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    if vm_provider not in ['VMware', 'Microsoft']:
        print 'VM provider has to be either be \"VMware\" or \"Microsoft\"'
    else:
        delete_vcenter_credential(modir, vm_provider, vmm_domain_name, profile_name)

    modir.logout()


