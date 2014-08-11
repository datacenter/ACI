import sys
import getopt
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Tenant
from cobra.model.vz import Filter, Entry

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


def create_filter(modir, tenant_name, filter_name, **args):
    """Create a filter"""

    # Query a tenant
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args

    # Check if the tenant exists
    if isinstance(fv_tenant, Tenant):
        # Create filter
        vz_filter = Filter(fv_tenant, filter_name)

        # Add an entry to the filter
        vz_entry = Entry(vz_filter,  get_value(args, 'entry_name', filter_name.lower()),
                         etherT=get_value(args, 'ether_type', 'unspecified').lower(),
                         prot=get_value(args, 'ip_protocol', 'unspecified').lower(),
                         applyToFrag=get_value(args, 'apply_frag', 'false'),
                         sFromPort=get_value(args, 'source_port_from', 'unspecified'),
                         sToPort=get_value(args, 'source_port_to', 'unspecified'),
                         dFromPort=get_value(args, 'destination_port_from', 'unspecified'),
                         dToPort=get_value(args, 'destination_port_to', 'unspecified'),
                         tcpRules=get_value(args, 'tcp_flag', ''))

    else:
        print 'Tenant', tenant_name, 'does not exist. Please create a tenant first'
        return

    print toXMLStr(fv_tenant, prettyPrint=True)
    commit_change(modir, fv_tenant)

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
        host_name, user_name, password, tenant_name, filter_name = sys.argv[1:6]
    except ValueError:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <filter_name>'
        sys.exit()

    # Obtain the optional arguments that with a flag.
    try:
        opts, args = getopt.getopt(opts, 'an:e:i:s:S:d:D:f',
                                   ['apply-frag=', 'entry-name=', 'ether-type=', 'ip-protocol=', 'source-port-from=',
                                    'source-port-to=', 'destination-port-from=', 'destination-port-to=', 'tcp-flag='])
    except getopt.GetoptError:
        sys.exit(2)

    args = {}

    for opt, arg in opts:
        if opt in ('-a', '--apply-frag'):
            args['apply_frag'] = True
        elif opt in ('-n', '--entry-name'):
            args['entry_name'] = arg
        elif opt in ('-e', '--ether-type'):
            args['ether_type'] = arg
        elif opt in ('-i', '--ip-protocol'):
            args['ip_protocol'] = arg
        elif opt in ('-s', '--source-port-from'):
            args['source_port_from'] = arg
        elif opt in ('-S', '--source-port-to'):
            args['source_port_to'] = arg
        elif opt in ('-d', '--destination-port-from'):
            args['destination_port_from'] = arg
        elif opt in ('-D', '--destination-port-to'):
            args['destination_port_to'] = arg
        elif opt in ('-f', '--tcp-flag'):
            args['tcp_flag'] = arg

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_filter(modir, tenant_name, filter_name, args_from_CLI=args)

    modir.logout()


