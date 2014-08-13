import sys
import getopt
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import AEPg, RsDomAtt

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


def add_vmm_domain_association(modir, tenant_name, application, epg, vmm_domain, **args):
    fv_epg = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application + '/epg-' + epg)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    if isinstance(fv_epg, AEPg):
        fv_rsdomatt = RsDomAtt(fv_epg, 'uni/vmmp-VMware/dom-' + vmm_domain,
                               instrImedcy=get_value(args, 'deployment_immediacy', 'lazy'),
                               resImedcy=get_value(args, 'resolution_immediacy', 'lazy'))
    else:
        print 'Fail to find EPG', epg, 'Please make sure you have the EPG in application', application
        return

    print toXMLStr(fv_epg, prettyPrint=True)
    commit_change(modir, fv_epg)

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
        host_name, user_name, password, tenant_name, application, epg, vmm_domain = sys.argv[1:8]
    except ValueError:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <application> <epg> <vmm_domain> [-d deployment-immediacy?] [-r resolution-immediacy?]'
        sys.exit()

    # Obtain the optional arguments that with a flag.
    try:
        opts, args = getopt.getopt(opts, 'dr',
                                   ['deployment-immediacy','resolution-immediacy'])
    except getopt.GetoptError:
        sys.exit(2)
    args = {}
    for opt, arg in opts:
        if opt in ('-d', '--deployment-immediacy'):
            args['deployment_immediacy'] = 'immediate'
        elif opt in ('-r', '--resolution-immediacy'):
            args['resolution_immediacy'] = 'immediate'

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    add_vmm_domain_association(modir, tenant_name, application, epg, vmm_domain, args_from_CLI=args)

    modir.logout()


