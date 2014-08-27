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

    # Obtain the arguments from CLI
    try:
        key_args = [{'name': 'provider', 'help': 'VM Provider'},
                    {'name': 'domain', 'help': 'vCenter Domain Name'}
        ]

        host_name, user_name, password, args = set_cli_argparse('Delete a vCenter Domain.', key_args)
        vm_provider = args.pop('provider')
        vmm_domain_name = args.pop('domain')

    except SystemExit:

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

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


