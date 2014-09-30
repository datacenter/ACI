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
    key_args = [{'name': 'tenant', 'help': 'Tenant name'},
                {'name': 'routed_outside', 'help': 'Routed Outside Network Name.'}
    ]
    opt_args = [{'flag': 'n', 'name': 'tnFvCtxName', 'help': 'The target name of the relation that defines which private network (layer 3 context or VRF) is associated with the external endpoint group networks (layer 3 instance profile).'},
                {'flag': 't', 'name': 'tags', 'help': 'A tag allows you to group multiple objects by a descriptive name.'},
                {'flag': 'B', 'name': 'BGP', 'help': 'When created, this profile indicates that IBGP will be configured for the endpoint groups in this external network.'},
                {'flag': 'O', 'name': 'OSPF', 'help': 'The OSPF external profile information.'},
                {'flag': 'i', 'name': 'areaId', 'help': 'The OSPF Area ID.'}
    ]

    try:
        host_name, user_name, password, args = set_cli_argparse('Create a Routed Outside Network.', key_args, opt_args)
        tenant_name = args.pop('tenant')
        routed_outside_name = args.pop('routed_outside')
        optional_args = args

    except SystemExit:

        if check_if_requesting_help(sys.argv, opt_args):
            sys.exit('Help Page')

        if len(sys.argv)>1:
            print 'Invalid input arguments.'

        host_name, user_name, password = input_login_info()
        tenant_name = input_tenant_name()
        routed_outside_name = input_key_args()
        optional_args = input_optional_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_routed_outside(modir, tenant_name, routed_outside_name, args_from_CLI=optional_args)

    modir.logout()


