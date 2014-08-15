import sys
import getopt
from cobra.model.l3ext import Out

from utility import *

from IPython import embed


def input_key_args(msg='\nPlease input Routed Outside info'):
    print msg
    return get_raw_input("Name (required): ", required=True)


def input_optional_args(*arg):
    args = {}
    return args


def create_routed_outside(modir, tenant_name, routed_outside_name, **args):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    fv_out = Out(fv_tenant, routed_outside_name)

    print_query_xml(fv_tenant)
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
        host_name, user_name, password, tenant_name, routed_outside_name = sys.argv[1:6]

        # Obtain the optional arguments that with a flag.
        try:
            opts, args = getopt.getopt(opts, 's:S:',
                                       ['sth1=','sth2='])
        except getopt.GetoptError:
            sys.exit(2)
        optional_args = {}
        for opt, arg in opts:
            if opt in ('-s', '--sth1'):
                optional_args['sht1'] = True
            elif opt in ('-S', '--sth2'):
                optional_args['sht2'] = arg

    except ValueError:
        host_name, user_name, password = input_login_info() 
        tenant_name = input_tenant_name()
        routed_outside_name = input_key_args()
        optional_args = input_optional_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_routed_outside(modir, tenant_name, routed_outside_name, args_from_CLI=optional_args)

    modir.logout()


