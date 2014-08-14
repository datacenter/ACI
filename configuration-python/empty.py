import sys
import getopt
from utility import *

from IPython import embed


def input_key_args():
    def get_raw_input(prompt=''):
        return raw_input(prompt).strip()
    print '\nInappropriate input arguments. Please fill in the arguments step by step.'
    args = []
    args.append(get_raw_input("something (required): "))
    return args


def some_function(modir, some_name, **args):
    mo = modir.lookupByDn('uni/tn-' + some_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    if isinstance(mo, MO):
        pass

    else:
        print 'Tenant', some_name, 'does not exist. Please create a tenant first'
        return

    print_query_xml(mo)
    commit_change(modir, mo)

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
        host_name, user_name, password, some_name = sys.argv[1:5]
    except ValueError:
        host_name, user_name, password = input_login_info() 
        some_name = input_key_args()

    # Obtain the optional arguments that with a flag.
    try:
        opts, args = getopt.getopt(opts, 's:S:',
                                   ['sth1=','sth2='])
    except getopt.GetoptError:
        sys.exit(2)
    args = {}
    for opt, arg in opts:
        if opt in ('-s', '--sth1'):
            args['sht1'] = True
        elif opt in ('-S', '--sth2'):
            args['sht2'] = arg

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    some_function(modir, some_name, args_from_CLI=args)

    modir.logout()


