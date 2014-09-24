from cobra.model.aaa import RadiusProvider

from createRadiusProvider import input_key_args
from utility import *


key_args = [{'name': 'radius_provider', 'help': 'Host Name or IP Address'}]


def delete_radius_provider(modir, radius_provider, **args):

    args = args['args_from_CLI'] if 'args_from_CLI' in args.keys() else args

    aaa_radiusprovider = modir.lookupByDn('uni/userext/radiusext/radiusprovider-'+radius_provider)

    if isinstance(aaa_radiusprovider, RadiusProvider):
        aaa_radiusprovider.delete()
    else:
        print 'Radius Provider', radius_provider, 'does not existed.'
        return

    print_query_xml(aaa_radiusprovider)
    commit_change(modir, aaa_radiusprovider)

if __name__ == '__main__':

    # Try mode one: arguments from CLI
    try:
        host_name, user_name, password, args = set_cli_argparse('Create Radius Provider.', key_args)

    except SystemExit:

        # Check if calling help page
        if check_if_requesting_help(sys.argv):
            sys.exit('Help Page')

        try:
            # Try mode two: load a config file
            data, host_name, user_name, password = read_config_yaml_file(sys.argv[1])
            radius_provider = data['radius_provider']
        except (IOError, KeyError, TypeError, IndexError) as input_error:
            # If both mode one and two fail, try mode three: wizard
            if len(sys.argv)>1:
                print input_error
            host_name, user_name, password = input_login_info()
            radius_provider = input_key_args()

    else:
        radius_provider = args.pop('radius_provider')

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_radius_provider(modir, radius_provider)

    modir.logout()


