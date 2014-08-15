import sys
import getopt
from cobra.model.fv import Tenant
from cobra.model.vz import BrCP, Subj, RsSubjFiltAtt

from utility import *


DEFAULT_SCOPE = 'context'
DEFAULT_REVERSE_FILTER_PORTS = 'true'
DEFAULT_QOS = 'unspecified'


def input_key_args(msg='Please input Contract info:'):
    print msg
    return get_raw_input("Contract Name (required): ")


def input_optional_args(contract_name):
    args = {'subject_name': get_raw_input('Subject Name (default: "' + contract_name.lower() + '"): '),
            'scope': get_optional_input('Scope (default: "' + DEFAULT_SCOPE + '")',
                                        ['application-profile(a)', 'context(c)', 'global(g)', 'tenant(t)']),
            'revFltPorts': get_optional_input('Reverse Filter Ports (default: "' + DEFAULT_REVERSE_FILTER_PORTS + '")',
                                              ['true(t)', 'false(f)']),
            'prio': get_optional_input('QoS Class (default: "' + DEFAULT_QOS + '")', ['level1', 'level2', 'level3']),
            'filter_name': get_raw_input('Filter Name (default: "None")')}
    return args


def create_contract(modir, tenant_name, contract_name, **args):
    """Query a tenant"""
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    if isinstance(fv_tenant, Tenant):
        # Create contract
        vz_ct = BrCP(fv_tenant, contract_name, scope=get_value(args, 'scope', DEFAULT_SCOPE))

        # Add a subject to the contract
        vz_subj = Subj(vz_ct, get_value(args, 'subject_name', contract_name + '_subj'),
                       revFltPorts=get_value(args, 'revFltPorts', DEFAULT_REVERSE_FILTER_PORTS),
                       prio=get_value(args, 'prio', DEFAULT_QOS))

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
        # Obtain the optional arguments that with a flag.
        try:
            opts, args = getopt.getopt(opts, 's:n:rQ:f:',
                                       ['scope=', 'subject_name=', 'revFltPorts', 'QoS-class=', 'filter-name='])
        except getopt.GetoptError:
            sys.exit(2)
        optional_args = {}
        for opt, arg in opts:
            if opt in ('-s', '--scope'):
                optional_args['scope'] = arg
            elif opt in ('-n', '--subject_name'):
                optional_args['subject_name'] = arg
            elif opt in ('-r', '--revFltPorts'):
                optional_args['revFltPorts'] = 'no'
            elif opt in ('-Q', '--QoS-class'):
                optional_args['prio'] = arg
            elif opt in ('-f', '--filter-name'):
                optional_args['filter_name'] = arg

    except ValueError:
        host_name, user_name, password = '172.22.233.207', 'admin','Cisco123' #input_login_info()
        tenant_name = 'bon_python'#input_tenant_name()
        contract_name = 'test_con'#input_key_args()
        optional_args = input_optional_args(contract_name)

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_contract(modir, tenant_name, contract_name, args_from_CLI=optional_args)

    modir.logout()



