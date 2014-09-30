from cobra.model.fv import RsProv, RsCons, RsProtBy

from utility import *

DEFAULT_QOS = 'unspecified'
DEFAULT_MATCH_TYPE = 'AtleastOne'

key_args = [{'name': 'contract', 'help': 'Contract Name'},
            {'name': 'contract_type', 'help': 'Contract Type', 'choices': ['provided', 'consumed', 'taboo']},
    ]

opt_args = [{'flag': 'm', 'name': 'Match type', 'dest': 'matchT', 'help': 'The matched EPG type.'},
            {'flag': 'Q', 'name': 'QoS_class', 'dest': 'prio', 'help': 'The priority level of a sub application running behind an endpoint group.'}
    ]


def input_key_args(msg='Please specify the contract.'):
    print msg
    args = []
    args.append(get_raw_input("Contract Name (required): ", required=True))
    args.append(get_optional_input("Contract Type (required): ", ['provided(p)', 'consumed(c)', 'taboo(t)'], required=True))
    return args


def input_optional_args(contract_type):
    args = {}
    if contract_type.lower() in ['provided', 'consumed']:
        args['prio'] = get_optional_input('QoS Class (default: "' + DEFAULT_QOS + '")', ['level1', 'level2', 'level3', DEFAULT_QOS])
        if contract_type.lower() == 'provided':
            args['matchT'] = get_optional_input('Match Type (default: "'+ DEFAULT_MATCH_TYPE+'"): ', ['All', 'AtleastOne', "AtmostOne", "None"])
    return args

def add_contract_to_mgmt_inband_epg(modir, contract, contract_type, **args):

    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args

    # Query a parent
    fv_inb = modir.lookupByDn('uni/tn-mgmt/mgmtp-default/inb-default')

    if contract_type.lower() == 'provided':
        fv_rsprov = RsProv(fv_inb, contract,
                           prio=get_value(args, 'prio', DEFAULT_QOS),
                           matchT=get_value(args, 'matchT', DEFAULT_MATCH_TYPE)
        )

    elif contract_type.lower() == 'consumed':
        fv_rscons = RsCons(fv_inb, contract,
                           prio=get_value(args, 'prio', DEFAULT_QOS),
        )

    elif contract_type.lower() == 'taboo':
        fv_rsprotby = RsProtBy(fv_inb, contract)

    else:
        print 'Invalid input Contract Type.'
        return

    print_query_xml(fv_inb)
    commit_change(modir, fv_inb)

if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        host_name, user_name, password, args = set_cli_argparse('Add Contract to mgmt In-Band EPG.', key_args, opt_args)
        contract = args.pop('contract')
        contract_type = args.pop('contract_type')

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            contract = data['contract']
            contract_type = data['contract_type']
            optional_args = data['optional_args']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = '172.22.233.207','admin','Cisco123'#input_login_info()
            contract, contract_type = input_key_args()
            optional_args = input_optional_args(contract_type)
    else:
        optional_args = args


    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    add_contract_to_mgmt_inband_epg(modir, contract, contract_type, args_from_CLI=optional_args)

    modir.logout()
