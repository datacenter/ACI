from cobra.model.fv import RsProv, RsCons, RsProtBy
from addContractToMgmtInBandEpg import input_key_args

from utility import *


key_args = [{'name': 'contract', 'help': 'Contract Name'},
            {'name': 'contract_type', 'help': 'Contract Type', 'choices': ['provided', 'consumed', 'taboo']},
    ]


def delete_contract_to_mgmt_inband_epg(modir, contract, contract_type):

    if contract_type.lower() == 'provided':
        mo_type = 'rsprov-'
    elif contract_type.lower() == 'consumed':
        mo_type = 'rscons-'
    elif contract_type.lower() == 'taboo':
        mo_type = 'rsprotBy-'
    else:
        print 'Invalid input Contract Type.'
        return

    # Query a parent
    fv_contract = modir.lookupByDn('uni/tn-mgmt/mgmtp-default/inb-default/' + mo_type + contract)
    fv_contract.delete()

    print_query_xml(fv_contract)
    commit_change(modir, fv_contract)

if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        host_name, user_name, password, args = set_cli_argparse('Delete Contract to mgmt In-Band EPG.', key_args)
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
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = input_login_info()
            contract, contract_type = input_key_args()


    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_contract_to_mgmt_inband_epg(modir, contract, contract_type)

    modir.logout()
