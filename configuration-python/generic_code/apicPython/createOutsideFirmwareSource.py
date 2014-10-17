from cobra.model.firmware import OSource

from createMo import *

PROTOCOL_CHOICES = ['scp', 'http']

DEFAULT_PROTOCOL = PROTOCOL_CHOICES[0]
DEFAULT_NONE = None


def input_key_args(msg='\nPlease Specify the Outside Firmware Source:'):
    print msg
    return input_raw_input("Source Name", required=True)


def input_optional_args():
    args = {'protocol': input_options('Protocol', DEFAULT_PROTOCOL, PROTOCOL_CHOICES),
            'url': input_raw_input('URL')}
    if args['protocol'] == PROTOCOL_CHOICES[0]:
        args['source_user'] = input_raw_input('The username for the source.')
        args['source_password'] = input_raw_input('The password for the source.')
    return args


def create_outside_firmware_source(parent_mo, source, **args):
    """Create Outside Firmware Source"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    # Create mo
    protocol = get_value(args, 'protocol', DEFAULT_PROTOCOL)
    if protocol != 'scp':
        args['source_user'] = DEFAULT_NONE
        args['source_password'] = DEFAULT_NONE
    firmware_osource = OSource(parent_mo, source, proto=protocol,
                               url=get_value(args, 'url', DEFAULT_NONE),
                               user=get_value(args, 'source_user', DEFAULT_NONE),
                               password=get_value(args, 'source_password', DEFAULT_NONE))
    return firmware_osource


class CreateOutsideFirmwareSource(CreateMo):

    def __init__(self):
        self.description = 'Create Outside Firmware Source. An outside source of images, such as an HTTP or SCP server. '
        self.source = None
        super(CreateOutsideFirmwareSource, self).__init__()

    def set_cli_mode(self):
        super(CreateOutsideFirmwareSource, self).set_cli_mode()
        self.parser_cli.add_argument('source', help='The identifying name for the outside source of images, such as an HTTP or SCP server.')
        self.parser_cli.add_argument('-P', '--protocol', default= DEFAULT_PROTOCOL, choices=PROTOCOL_CHOICES, help='The Firmware download protocol.')
        self.parser_cli.add_argument('-u', '--source_user', help='The username for the source.')
        self.parser_cli.add_argument('-p', '--source_password', help='The password for the source.')

    def read_key_args(self):
        self.source = self.args.pop('source')

    def wizard_mode_input_args(self):
        self.args['source'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/fabric/fwrepop/osrc-', self.source, OSource, description='Outside firmware Source')
        super(CreateOutsideFirmwareSource, self).delete_mo()

    def main_function(self):
        # Query a parent
        self.look_up_mo('uni/fabric/fwrepop', '')
        create_outside_firmware_source(self.mo, self.source, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateOutsideFirmwareSource()


