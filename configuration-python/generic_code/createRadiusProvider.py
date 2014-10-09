from cobra.model.aaa import RadiusProvider, RsSecProvToEpg

from createMo import *

DEFAULT_PORT = '1812'
DEFAULT_PROTOCOL = 'pap'
DEFAULT_KEY = ''
DEFAULT_TIMEOUT = '5'
DEFAULT_RETRIES = '1'
DEFAULT_MANAGEMENT_EPG = ''

PROTOCOL_CHOICES = ['pap', 'chap', 'mschap']
MANAGEMENT_EPG_CHOICES = ['InBand', 'OutOfBand']


def input_key_args(msg='\nPlease Specify the Remote Server:'):
    print msg
    return input_raw_input("Host Name or IP Address", required=True)


def input_optional_args():
    args = {}
    args['port'] = input_options('Authorization Port Name', DEFAULT_PORT, [], num_accept=True)
    args['protocol'] = input_options('Authorization Protocol', DEFAULT_PROTOCOL, PROTOCOL_CHOICES)
    args['key'] = input_raw_input('Key', DEFAULT_KEY)
    args['timeout'] = input_options('Timeout(sec) [1-60]', DEFAULT_TIMEOUT, [], num_accept=True)
    args['retries'] = input_options('Retries [1-5]', DEFAULT_RETRIES, [], num_accept=True)
    args['management_epg'] = input_options('Management EPG', DEFAULT_MANAGEMENT_EPG, MANAGEMENT_EPG_CHOICES)
    return args


def create_radius_provider(aaa_radiusep, radius_provider, **args):
    """Create a remote server supporting the RADIUS protocol that will be used for authentication. """
    args = args['optional_args'] if 'optional_args' in args.keys() else args
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


class CreateRadiusProvider(CreateMo):

    def __init__(self):
        self.description = 'Create a remote server supporting the RADIUS protocol that will be used for authentication. '
        self.radius_provider = None
        super(CreateRadiusProvider, self).__init__()

    def set_cli_mode(self):
        super(CreateRadiusProvider, self).set_cli_mode()
        self.parser_cli.add_argument('radius_provider', help='The name of the RADIUS service provider.')
        self.parser_cli.add_argument('-a', '--authorization_port', dest='port', default= DEFAULT_PORT, help='The service port number for the RADIUS service.')
        self.parser_cli.add_argument('-p', '--authorization_protocol', dest='protocol', default= DEFAULT_PROTOCOL, choices=PROTOCOL_CHOICES, help='The RADIUS authentication protocol.')
        self.parser_cli.add_argument('-k', '--key', default= DEFAULT_KEY, help='A password for the AAA provider database.')
        self.parser_cli.add_argument('-t', '--timeout', default= DEFAULT_TIMEOUT, help='The timeout for communication with a RADIUS provider server.')
        self.parser_cli.add_argument('-r', '--retries', default= DEFAULT_RETRIES, help='Retries')
        self.parser_cli.add_argument('-m', '--management_epg', default= DEFAULT_MANAGEMENT_EPG, choices=MANAGEMENT_EPG_CHOICES, help='A relation to the endpoint group through which the provider server is reachable.')

    def read_key_args(self):
        self.radius_provider = self.args.pop('radius_provider')

    def wizard_mode_input_args(self):
        self.args['radius_provider'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/userext/radiusext/radiusprovider-', self.radius_provider, RadiusProvider, description='Radius Provider')
        super(CreateRadiusProvider, self).delete_mo()

    def main_function(self):
        # Query a tenant
        self.look_up_mo('uni/userext/radiusext', '')
        create_radius_provider(self.mo, self.radius_provider, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateRadiusProvider()


