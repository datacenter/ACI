import getopt
from cobra.model.l3ext import Out, RsEctx
from cobra.model.bgp import ExtP as bgpExtP
from cobra.model.ospf import ExtP as ospfExtP
from cobra.model.tag import Inst

from utility import *


def input_key_args(msg='\nPlease input Routed Outside Network info'):
    print msg
    return get_raw_input("External Routed Network Name (required): ", required=True)


def input_optional_args(*arg):
    args = {}
    args['tnFvCtxName'] = get_raw_input('Private Network? (default:"None"): ')
    args['tags'] = get_raw_input('Tags? (default:"None"): ')
    args['BGP'] = get_yes_no('Apply BGP (default:"None")')
    args['OSPF'] = get_yes_no('Apply OSPF (default:"None")')
    if args['OSPF']:
        args['areaId'] = get_optional_input('OSPF Area ID (default: "1")', [], num_accept=True)
    return args


def create_routed_outside(modir, tenant_name, routed_outside_name, **args):
    fv_tenant = check_if_tenant_exist(modir, tenant_name)
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    l3ext_out = Out(fv_tenant, routed_outside_name)
    if 'tnFvCtxName' in args.keys():
        l3ext_rsectx = RsEctx(l3ext_out, tnFvCtxName=args['tnFvCtxName'])
    if 'BGP' in args.keys() and args['BGP']:
        bgp_extp = bgpExtP(l3ext_out)
    if 'OSPF' in args.keys() and args['OSPF']:
        print get_value(args, 'areaId', '1')
        ospf_extp = ospfExtP(l3ext_out, areaId='0.0.0.' + str(get_value(args, 'areaId', '1')))
    if 'tags' in args.keys() and args['tags'] != '':
        tag_inst = Inst(l3ext_out, args['tags'])

    print_query_xml(fv_tenant)
    commit_change(modir, fv_tenant)


if __name__ == '__main__':

    # Obtain the arguments from CLI
    opts = sys.argv[1:]
    opts.reverse()

    # Obtain the key parameters.
    keys = []
    while len(opts) > 0 and opts[len(opts) - 1][0] != '-':
        keys.append(opts.pop())
    opts.reverse()

    try:
        host_name, user_name, password, tenant_name, routed_outside_name = sys.argv[1:6]

        # Obtain the optional arguments that with a flag.
        try:
            opts, args = getopt.getopt(opts, 'n:Bt:Oi:',
                                       ['private-network=', 'BGP', 'tags=', 'OSPF', 'OSPF-id='])
        except getopt.GetoptError:
            sys.exit(2)
        optional_args = {}
        for opt, arg in opts:
            if opt in ('-n', '--private-network'):
                optional_args['tnFvCtxName'] = arg
            elif opt in ('-t', '--tags'):
                optional_args['tags'] = arg
            elif opt in ('-B', '--BGP'):
                optional_args['BGP'] = True
            elif opt in ('-O', '--OSPF'):
                optional_args['OSPF'] = True
            elif opt in ('-i', '--OSPF-id'):
                optional_args['areaId'] = arg

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


