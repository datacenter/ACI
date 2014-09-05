from cobra.model.aaa import RadiusProvider, RsSecProvToEpg
from utility import *

DEFAULT_PORT = '1812'
DEFAULT_PROTOCOL = 'pap'
DEFAULT_TIMEOUT = '5'
DEFAULT_RETRIES = '1'

key_args = [{'name': 'radius_provider', 'help': 'Host Name or IP Address'}]

opt_args = [{'flag': 'a', 'name': 'port', 'help': 'Authorization Port.'},
            {'flag': 'p', 'name': 'protocol', 'help': 'Authorization Protocol.'},
            {'flag': 'k', 'name': 'key', 'help': 'Key'},
            {'flag': 't', 'name': 'timeout', 'help': 'Timeout(sec)'},
            {'flag': 'r', 'name': 'retries', 'help': 'Retries'},
            {'flag': 'm', 'name': 'management_epg', 'help': 'Management EPG'},
]


def input_key_args(msg='\nPlease input Radius Provider info:'):
    print msg
    return get_raw_input("Host Name or IP Address (required): ", required=True)


def input_optional_args():
    args = {}
    args['port'], = get_optional_input('Authorization Port Name (default: '+DEFAULT_PORT+'): ', [], num_accept=True),
    args['protocol'], = get_optional_input('Authorization Protocol (default: '+DEFAULT_PROTOCOL+'): ', ['pap(p)', 'chap(c)', 'mschap(m)']),
    args['key'], = get_raw_input('Key (default: None): '),
    args['timeout'], = get_raw_input('Timeout(sec) (default: '+DEFAULT_TIMEOUT+')[0-60]: '),
    args['retries'], = get_raw_input('Retries (default: '+DEFAULT_RETRIES+')[0-5]: '),
    args['management_epg'], = get_optional_input('Management EPG (default: "None")', ['InBand(I)', 'OutOfBand(O)']),
    return args


def create_radius_provider(modir, radius_provider, **args):

    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args

    aaa_radiusep = modir.lookupByDn('uni/userext/radiusext')
    aaa_radiusprovider = RadiusProvider(aaa_radiusep,radius_provider,
                                        authPort = get_value(args, 'port', DEFAULT_PORT),
                                        authProtocol = get_value(args, 'protocol', DEFAULT_PROTOCOL),
                                        key = get_value(args, 'key', ''),
                                        timeout = get_value(args, 'timeout', DEFAULT_TIMEOUT),
                                        retries = get_value(args, 'retries', DEFAULT_RETRIES)
                                        )

    # check Management EPG
    if args['management_epg'] in ['inb', 'i', 'in-band', 'InBand']:
        aaa_rssecprovtoepg = RsSecProvToEpg(aaa_radiusprovider, tDn='uni/tn-mgmt/mgmtp-default/inb-default')
    elif args['management_epg'] in ['oob', 'o', 'out-of-band', 'OutOfBand']:
        aaa_rssecprovtoepg = RsSecProvToEpg(aaa_radiusprovider, tDn='uni/tn-mgmt/mgmtp-default/oob-default')

    print_query_xml(aaa_radiusep)
    commit_change(modir, aaa_radiusep)

if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        host_name, user_name, password, args = set_cli_argparse('Create Radius Provider.', key_args, opt_args)

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv, opt_args):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            radius_provider = data['radius_provider']
            optional_args = data['optional_args']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = input_login_info()
            radius_provider = input_key_args()
            optional_args = input_optional_args()

    else:
        radius_provider = args.pop('radius_provider')
        optional_args = args

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    create_radius_provider(modir, radius_provider, args_from_CLI=optional_args)

    modir.logout()


