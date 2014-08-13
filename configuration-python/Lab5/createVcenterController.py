import sys
import getopt
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.vmm import DomP, CtrlrP, RsAcc, UsrAccP

from cobra.internal.codec.xmlcodec import toXMLStr


def apic_login(hostname, username, password):
    """Login to APIC"""
    epoint = EndPoint(hostname, secure=False, port=80)
    lsess = LoginSession(username, password)
    modir = MoDirectory(epoint, lsess)
    modir.login()
    return modir


def commit_change(modir, changed_object):
    """Commit the changes to APIC"""
    config_req = ConfigRequest()
    config_req.addMo(changed_object)
    modir.commit(config_req)


def get_value(args, key, default_value):
    """Return the value of an argument. If no such an argument, return a default value"""
    return args[key] if key in args.keys() else default_value


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
            else:
                print args['associated_credential'], 'has not been defined.'
                return
    else:
        print 'There is no VMM Domain', vmm_domain_name, 'in', vm_provider
        return

    print toXMLStr(vmm_domp, prettyPrint=True)
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
    except ValueError:
        print 'Usage:', __file__, '<hostname> <username> <password> <vm_provider> <vmm_domain_name> <controller_name> <host_or_ip> <data_center> [-s stats-collection?] [-d <data-center>] [-a <associated-credential>]'
        sys.exit()

    # Obtain the optional arguments that with a flag.
    try:
        opts, args = getopt.getopt(opts, 'sd:a:',
                                   ['stats-collection', 'data-center=', 'associated-credential='])
    except getopt.GetoptError:
        sys.exit(2)
    args = {}
    for opt, arg in opts:
        if opt in ('-s', '--stats-collection'):
            args['statsMode'] = 'enabled'
        elif opt in ('-a', '--associated-credential'):
            args['associated_credential'] = arg

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    if vm_provider not in ['VMware', 'Microsoft']:
        print 'VM provider has to be either be \"VMware\" or \"Microsoft\"'
    else:
        create_vcenter_controller(modir, vm_provider, vmm_domain_name, controller_name, host_or_ip, data_center, args_from_CLI=args)

    modir.logout()


