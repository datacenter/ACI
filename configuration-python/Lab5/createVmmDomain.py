import sys
import getopt
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.vmm import DomP
from cobra.model.infra import RsVlanNs

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


def create_vmm_domain(modir, vm_provider, vmm_domain_name, **args):
    vmm_provp = modir.lookupByDn('uni/vmmp-' + vm_provider)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    vmm_domp = DomP(vmm_provp, vmm_domain_name)
    if 'vlan_name' in args.keys() and 'vlan_mode' in args.keys():
        infra_revlanns = RsVlanNs(vmm_domp,tDn='uni/infra/vlanns-[' + args['vlan_name'] + ']-' + args['vlan_mode'])
    elif 'vlan_name' in args.keys() or 'vlan_mode' in args.keys():
        print 'Please specify both [vlan-name] and [vlan-mode]'
    print toXMLStr(vmm_provp, prettyPrint=True)
    commit_change(modir, vmm_provp)

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
        host_name, user_name, password, vm_provider, vmm_domain_name = sys.argv[1:6]
    except ValueError:
        print 'Usage:', __file__, '<hostname> <username> <password> <vm_provider> <VMM_domain_name> [-v <vlan-name>] [-m <vlan-mode>]'
        sys.exit()

    # Obtain the optional arguments that with a flag.
    try:
        opts, args = getopt.getopt(opts, 'v:m:',
                                   ['vlan-name=','vlan-mode='])
    except getopt.GetoptError:
        sys.exit(2)
    args = {}
    for opt, arg in opts:
        if opt in ('-v', '--vlan-name'):
            args['vlan_name'] = arg
        elif opt in ('-m', '--vlan-mode'):
            args['vlan_mode'] = arg

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    if vm_provider not in ['VMware', 'Microsoft']:
        print 'VM provider has to be either be \"VMware\" or \"Microsoft\"'
    else:
        create_vmm_domain(modir, vm_provider, vmm_domain_name, args_from_CLI=args)

    modir.logout()
