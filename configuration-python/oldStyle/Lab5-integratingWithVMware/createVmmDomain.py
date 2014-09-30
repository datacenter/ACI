from cobra.model.vmm import DomP
from cobra.model.infra import RsVlanNs

from utility import *


def input_key_args(msg='\nPlease input VMM Domian info:'):
    print msg
    args = []
    args.append(get_optional_input("VMM Provider Name (required)", ['VMware(V)', 'Microsoft(M)'], required=True))
    args.append(get_raw_input("VMM Domain Name (required): ", required=True))
    return args

def input_optional_args():
    args = {}
    args['vlan_name'] = get_raw_input('Vlan Name (default: None): ')
    if args['vlan_name'] not in ['None', 'none', 'NONE', '']:
        args['vlan_mode'] = get_optional_input("Vlan Mode (required) ", ['dynamic(d)', 'static(s)'], required=True)
    return args


def create_vmm_domain(modir, vm_provider, vmm_domain_name, **args):
    vmm_provp = modir.lookupByDn('uni/vmmp-' + vm_provider)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    vmm_domp = DomP(vmm_provp, vmm_domain_name)
    if 'vlan_name' in args.keys() and 'vlan_mode' in args.keys():
        infra_revlanns = RsVlanNs(vmm_domp,tDn='uni/infra/vlanns-[' + args['vlan_name'] + ']-' + args['vlan_mode'])
    elif 'vlan_name' in args.keys() or 'vlan_mode' in args.keys():
        print 'Please specify both [vlan-name] and [vlan-mode]'

    print_query_xml(vmm_provp)
    commit_change(modir, vmm_provp)

if __name__ == '__main__':

    # Obtain the arguments from CLI
    key_args = [{'name': 'provider', 'help': 'VM Provider'},
                {'name': 'domain', 'help': 'vCenter Domain Name'}
    ]
    opt_args = [{'flag': 'v', 'name': 'vlan_name', 'help': 'Associate a VLAN to the vCenter Domain'},
                {'flag': 'm', 'name': 'vlan_mode', 'help': 'VLAN Mode: Static/Dynamic'}
    ]

    try:
        host_name, user_name, password, args = set_cli_argparse('Create a vCenter Domain.', key_args, opt_args)
        vm_provider = args.pop('provider')
        vmm_domain_name = args.pop('domain')
        optional_args = args

    except SystemExit:


        if check_if_requesting_help(sys.argv, opt_args):
            sys.exit('Help Page')

        if len(sys.argv)>1:
            print 'Invalid input arguments.'

        host_name, user_name, password = input_login_info()
        vm_provider, vmm_domain_name = input_key_args()
        optional_args = input_optional_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    if vm_provider not in ['VMware', 'Microsoft']:
        print 'VM provider has to be either be \"VMware\" or \"Microsoft\"'
    else:
        create_vmm_domain(modir, vm_provider, vmm_domain_name, args_from_CLI=optional_args)

    modir.logout()
