import sys
import getopt
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Ap, AEPg, RsBd

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


def create_application_epg(modir, tenant_name, application_name, epg_name, **args):
    """Create an EPG"""

    # Query the application
    fv_ap = modir.lookupByDn('uni/tn-' + tenant_name + '/ap-' + application_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    if isinstance(fv_ap, Ap):
        # Create an EPG
        fv_aepg = AEPg(fv_ap, epg_name,
                       prio=get_value(args, 'prio', 'unspecified').lower())

        # Provide bridge_domain to the EPG.
        if 'bridge_domain' in args.keys():
            fv_rsbd = RsBd(fv_aepg, tnFvBDName=args['bridge_domain'])
    else:
        print 'There is no application', application_name, 'in tenant', tenant_name, '. Please create an application.'
        return

    print toXMLStr(fv_ap, prettyPrint=True)
    commit_change(modir, fv_ap)

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
        host_name, user_name, password, tenant_name, application_name, epg_name = sys.argv[1:7]
    except ValueError:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <application_name> <EPG_name>'
        sys.exit()

    # Obtain the optional arguments that with a flag.
    try:
        opts, args = getopt.getopt(opts, 'b:Q:',
                                   ['bridge-domain=', 'QoS-class='])
    except getopt.GetoptError:
        sys.exit(2)
    args = {}
    for opt, arg in opts:
        if opt in ('-b', 'bridge-domain'):
            args['bridge_domain'] = arg
        elif opt in ('-Q', '--QoS-class'):
            args['prio'] = arg

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_application_epg(modir, tenant_name, application_name, epg_name, args_from_CLI=args)

    modir.logout()


