import sys
import getopt
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
    opts = sys.argv[1:]
    opts.reverse()

    # Obtain the key parameters.
    keys = []
    while len(opts) > 0 and opts[len(opts)-1][0] != '-':
        keys.append(opts.pop())
    opts.reverse()
    try:
        host_name, user_name, password, policy_group_name = sys.argv[1:5]
        # Obtain the optional arguments that with a flag.
        try:
            opts, args = getopt.getopt(opts, 'dICBcS',
                                       ['date-time', 'ISIS', 'COOP', 'BGP-Route-Reflector', 'communication', 'SNMP'])
        except getopt.GetoptError:
            sys.exit(2)
        optional_args = {'tnDatetimePolName': '',
                'tnIsisDomPolName': '',
                'tnCoopPolName': '',
                'tnBgpInstPolName': '',
                'tnCommPolName': '',
                'tnSnmpPolName': '',
                }
        for opt, arg in opts:
            if opt in ('-d', '--date-time'):
                optional_args['tnDatetimePolName'] = 'default'
            elif opt in ('-I', '--ISIS'):
                optional_args['tnIsisDomPolName'] = 'default'
            elif opt in ('-C', '--COOP'):
                optional_args['tnCoopPolName'] = 'default'
            elif opt in ('-B', '--BGP-Route-Reflector'):
                optional_args['tnBgpInstPolName'] = 'default'
            elif opt in ('-c', '--communication'):
                optional_args['tnCommPolName'] = 'default'
            elif opt in ('-S', '--SNMP'):
                optional_args['tnSnmpPolName'] = 'default'
    except ValueError:
        host_name, user_name, password = '172.22.233.207','admin','Cisco123'#input_login_info()
        policy_group_name = input_key_args()
        optional_args = input_optional_args()


    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_pod_policy_group(modir, policy_group_name, args_from_CLI=optional_args)

    modir.logout()


