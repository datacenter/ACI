import sys
import getopt
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Tenant
from cobra.model.vz import BrCP, Subj, RsSubjFiltAtt

from cobra.internal.codec.xmlcodec import toXMLStr
from IPython import embed


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


def create_contract(modir, tenant_name, contract_name, **args):
    """Query a tenant"""
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    if isinstance(fv_tenant, Tenant):
        # Create contract
        vz_ct = BrCP(fv_tenant, contract_name, scope=get_value(args, 'scope', 'context'))

        # Add a subject to the contract
        vz_subj = Subj(vz_ct, get_value(args, 'subject_name', contract_name + '_subj'),
                       revFltPorts=get_value(args, 'revFltPorts', 'yes'),
                       prio=get_value(args, 'prio', 'unspecified'))

        # Assign an existed filter to the subject
        filters = get_value(args, 'filter_name', '')
        if filters != '':
            vz_rs_subj_filt_att = RsSubjFiltAtt(vz_subj, filters)

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
        host_name, user_name, password, tenant_name, contract_name = sys.argv[1:6]
    except ValueError:
        print 'Usage:', __file__, '<hostname> <username> <password> <tenant_name> <contract_name> [-s <scope>] [-n <contract_subject_name>] [-r reverse_filter_port?] [-Q <QoS_class>] [-f <filter_name>]'
        sys.exit()

    # Obtain the optional arguments that with a flag.
    try:
        opts, args = getopt.getopt(opts, 's:n:rQ:f:',
                                   ['scope=', 'subject_name', 'revFltPorts', 'QoS-class=', 'filter-name='])
    except getopt.GetoptError:
        sys.exit(2)
    args = {}
    for opt, arg in opts:
        if opt in ('-s', '--scope'):
            args['scope'] = arg
        elif opt in ('-n', '--subject_name'):
            args['subject_name'] = arg
        elif opt in ('-r', '--revFltPorts'):
            args['revFltPorts'] = 'no'
        elif opt in ('-Q', '--QoS-class'):
            args['prio'] = arg
        elif opt in ('-f', '--filter-name'):
            args['filter_name'] = arg

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_contract(modir, tenant_name, contract_name, args_from_CLI=args)

    modir.logout()



