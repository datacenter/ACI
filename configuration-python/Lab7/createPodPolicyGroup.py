from cobra.model.fabric import PodPGrp, RsCommPol, RsPodPGrpBGPRRP, RsPodPGrpCoopP, RsPodPGrpIsisDomP, RsSnmpPol, RsTimePol

from utility import *


def input_key_args(msg='\nPlease input Pod Policy Group info:'):
    print msg
    return get_raw_input("Name (required): ", required=True)


def input_optional_args(*arg):
    def return_default(msg):
        default = raw_input('use default' + msg + ' (default "no") [yes(y)/no(n)]?: ')
        return 'default' if default in ['yes', 'y'] else ''
    args = {}
    args['tnDatetimePolName'] = return_default('Date Time Policy')
    args['tnIsisDomPolName'] = return_default('ISIS Policy')
    args['tnCoopPolName'] = return_default('COOP Group Policy')
    args['tnBgpInstPolName'] = return_default('BGP Route Reflector Policy')
    args['tnCommPolName'] = return_default('Communication Policy')
    args['tnSnmpPolName'] = return_default('SNMP Policy')
    return args


def create_pod_policy_group(modir, policy_group_name, **args):

    fabric_funcp = modir.lookupByDn('uni/fabric/funcprof/')
    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args
    fabric_podpgrp = PodPGrp(fabric_funcp, policy_group_name)
    fabric_podpgrp_children = RsTimePol(fabric_podpgrp, tnDatetimePolName=args['tnDatetimePolName'])
    fabric_podpgrp_children = RsPodPGrpIsisDomP(fabric_podpgrp, tnIsisDomPolName=args['tnIsisDomPolName'])
    fabric_podpgrp_children = RsPodPGrpCoopP(fabric_podpgrp, tnCoopPolName=args['tnCoopPolName'])
    fabric_podpgrp_children = RsPodPGrpBGPRRP(fabric_podpgrp, tnBgpInstPolName=args['tnBgpInstPolName'])
    fabric_podpgrp_children = RsCommPol(fabric_podpgrp, tnCommPolName=args['tnCommPolName'])
    fabric_podpgrp_children = RsSnmpPol(fabric_podpgrp, tnSnmpPolName=args['tnSnmpPolName'])

    print_query_xml(fabric_funcp)
    commit_change(modir, fabric_funcp)

if __name__ == '__main__':

    # Obtain the arguments from CLI
    try:
        key_args = [{'name': 'policy_group', 'help': 'Policy Group name'}]
        opt_args = [{'flag': 'd', 'name': 'date_time', 'dest': 'tnDatetimePolName', 'help': 'Date Time Policy'},
                    {'flag': 'I', 'name': 'isis', 'dest':  'tnIsisDomPolName', 'help': 'ISIS Policy'},
                    {'flag': 'C', 'name': 'coop', 'dest':  'tnCoopPolName',  'help': 'COOP Group Policy'},
                    {'flag': 'B', 'name': 'bgp', 'dest':  'tnBgpInstPolName', 'help': 'BGP Route Reflector Policy'},
                    {'flag': 'c', 'name': 'communication', 'dest':  'tnCommPolName', 'help': 'Communication Policy'},
                    {'flag': 'S', 'name': 'snmp', 'dest':  'tnSnmpPolName', 'help': 'SNMP Policy'}
        ]

        host_name, user_name, password, args = set_cli_argparse('Create a Pod Policy Group.', key_args, opt_args)
        policy_group_name = args.pop('policy_group')
        optional_args = args

    except: #?error

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
            sys.exit('Help Page')

        host_name, user_name, password = input_login_info()
        policy_group_name = input_key_args()
        optional_args = input_optional_args()


    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_pod_policy_group(modir, policy_group_name, args_from_CLI=optional_args)

    modir.logout()


