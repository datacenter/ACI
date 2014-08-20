import getopt
from cobra.model.fv import Ctx, RsBgpCtxPol, RsOspfCtxPol, RsCtxToEpRet, RsCtxMonPol

from utility import *

# use "None" to delete the configuration

def input_key_args(msg='Please input Private L3 Network info:'):
    print msg
    return get_raw_input("Private L3 Network (required): ", required=True)


def input_optional_args(*arg):
    args = {}
    args['bgp'] = get_raw_input("BGP Timers (default: 'None'): ")
    args['ospf'] = get_raw_input("OSPF Timers (default: 'None'): ")
    args['eprp'] = get_raw_input("End Point Retention Policy (default: 'None'): ")
    args['mp'] = get_raw_input("Monitoring Policy (default: 'None'): ")
    return args


def config_private_network_default_timers(modir, tenant_name, private_network, **args):
    fv_ctx = modir.lookupByDn('uni/tn-' + tenant_name + '/ctx-' + private_network)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args

    if isinstance(fv_ctx, Ctx):
        if 'bgp' in args and args['bgp'] != '':
            fv_rsbgpctxpol = RsBgpCtxPol(fv_ctx, tnBgpCtxPolName='' if args['bgp'].lower() == 'none' else args['bgp'])
        if 'ospf' in args and args['ospf'] != '':
            fv_rsospfctxpol = RsOspfCtxPol(fv_ctx, tnOspfCtxPolName='' if args['ospf'].lower() == 'none' else args['ospf'])
        if 'eprp' in args and args['eprp'] != '':
            fv_rsctxtoepret = RsCtxToEpRet(fv_ctx, tnFvEpRetPolName='' if args['eprp'].lower() == 'none' else args['eprp'])
        if 'mp' in args and args['mp'] != '':
            fv_rsctxmonpol = RsCtxMonPol(fv_ctx, tnMonEPGPolName='' if args['mp'].lower() == 'none' else args['mp'])
    else:
        print 'Private L3 Network', private_network, 'does not existed.'
        return

    print_query_xml(fv_ctx)

    commit_change(modir, fv_ctx)


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

        hostname, username, password, tenant_name, private_network = keys[0:5]

        # Obtain the optional arguments that with a flag.
        try:
            opts, args = getopt.getopt(opts, 'B:O:e:m:',
                                       ['BGP=', 'OSPF=', 'end-point-retention=', 'monitoring='])
        except getopt.GetoptError:
            sys.exit(2)
        optional_args = {}
        for opt, arg in opts:
            print opt
            if opt in ('-B', '--BGP'):
                optional_args['bgp'] = arg
            elif opt in ('-O', '--OSPF'):
                optional_args['ospf'] = arg
            elif opt in ('-e', '--end-point-retention'):
                optional_args['eprp'] = arg
            elif opt in ('-m', '--monitoring'):
                optional_args['mp'] = arg


    except ValueError:
        hostname, username, password = input_login_info()
        tenant_name = input_tenant_name()
        private_network = input_key_args()
        optional_args = input_optional_args()
    modir = apic_login(hostname, username, password)
    config_private_network_default_timers(modir, tenant_name, private_network, args_from_CLI=optional_args)
    modir.logout()
