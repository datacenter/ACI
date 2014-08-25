import getopt
from cobra.model.vmm import DomP, CtrlrP, RsAcc, UsrAccP
from createVmmDomain import input_key_args as input_vmm_domian_args

from utility import *


def input_key_args(msg='\nPlease input vCenter Controller info:'):
    print msg
    args = []
    args.append(get_raw_input("Profile Name (required): ", required=True))
    args.append(get_raw_input("Host Name or IP Address (required): ", required=True))
    args.append(get_raw_input("Datacenter (required): ", required=True))
    return args


def input_optional_args():
    args = {}
    args['statsMode'] = get_optional_input('Stats Collection (default: "disabled"): ', ['enabled(e)', 'disabled(d)'])
    args['associated_credential'] = get_raw_input('Associated Credential (default: None): ')
    return args


def create_vcenter_controller(modir, vm_provider, vmm_domain_name, controller_name, host_or_ip, data_center, **args):
    vmm_domp = modir.lookupByDn('uni/vmmp-' + vm_provider + '/dom-' + vmm_domain_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    if isinstance(vmm_domp, DomP):
        vmm_ctrlrp = CtrlrP(vmm_domp, controller_name,
                            hostOrIp=host_or_ip, rootContName=data_center,
                            statsMode=get_value(args, 'statsMode', 'disabled'))

        # define associated credential
        if 'associated_credential' in args.keys():
            vmm_usraccp_path = 'uni/vmmp-' + vm_provider + '/dom-' + vmm_domain_name + '/usracc-' + args['associated_credential']
            vmm_usraccp = modir.lookupByDn(vmm_usraccp_path)
            if isinstance(vmm_usraccp, UsrAccP):
                vmm_rtctrlrp = RsAcc(vmm_ctrlrp, tDn=vmm_usraccp_path)
            elif args['associated_credential'] != '':
                print 'Associated Credential', args['associated_credential'], 'has not been defined.'
                return
    else:
        print 'There is no VMM Domain', vmm_domain_name, 'in', vm_provider
        return

    print_query_xml(vmm_domp)
    commit_change(modir, vmm_domp)

if __name__ == '__main__':

    # Obtain the arguments from CLI
    opts = sys.argv[1:]
    opts.reverse()

    # Obtain the key parameters.
    keys = []
    while len(opts) > 0 and opts[len(opts)-1][0] != '-':
        keys.append(opts.pop())
    opts.reverse()
    try:
        host_name, user_name, password, vm_provider, vmm_domain_name, controller_name, host_or_ip, data_center = sys.argv[1:9]
        # Obtain the optional arguments that with a flag.
        try:
            opts, args = getopt.getopt(opts, 'sa:',
                                       ['stats-collection', 'associated-credential='])
        except getopt.GetoptError:
            sys.exit(2)
        optional_args = {}
        for opt, arg in opts:
            if opt in ('-s', '--stats-collection'):
                optional_args['statsMode'] = 'enabled'
            elif opt in ('-a', '--associated-credential'):
                optional_args['associated_credential'] = arg
    except ValueError:
        host_name, user_name, password = input_login_info()
        vm_provider, vmm_domain_name = input_vmm_domian_args()
        controller_name, host_or_ip, data_center = input_key_args()
        optional_args = input_optional_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    if vm_provider not in ['VMware', 'Microsoft']:
        print 'VM provider has to be either be \"VMware\" or \"Microsoft\"'
    else:
        create_vcenter_controller(modir, vm_provider, vmm_domain_name, controller_name, host_or_ip, data_center, args_from_CLI=optional_args)

    modir.logout()


