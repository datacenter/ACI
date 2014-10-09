from cobra.model.aaa import User, UserDomain

from createLocalUser import input_key_args as input_local_user
from createMo import *


def input_key_args(msg='\nPlease Specify User Domain:'):
    print msg
    return input_raw_input("User Domain Name", required=True)


def add_user_domain(parent_mo, user_domain):
    """The AAA domain to which the user belongs. """
    aaa_userdomain = UserDomain(parent_mo, user_domain)
    return aaa_userdomain


class AddSecurityDomain(CreateMo):

    def __init__(self):
        self.description = 'The AAA domain to which the user belongs. '
        self.local_user = None
        self.user_domain = None
        super(AddSecurityDomain, self).__init__()

    def set_cli_mode(self):
        super(AddSecurityDomain, self).set_cli_mode()
        self.parser_cli.add_argument('local_user', help='The name of a locally-authenticated user account.')
        self.parser_cli.add_argument('user_domain', help='The name of the user domain')

    def read_key_args(self):
        self.local_user = self.args.pop('local_user')
        self.user_domain = self.args.pop('user_domain')

    def wizard_mode_input_args(self):
        self.args['local_user'] = input_local_user('\nPlease Specify User Domain:', user_only=True, delete_function=self.delete)[0]
        self.args['user_domain'] = input_key_args('')

    def delete_mo(self):
        self.check_if_mo_exist('uni/userext/user-' + self.local_user + '/userdomain-', self.user_domain, UserDomain, description='User Domain')
        super(AddSecurityDomain, self).delete_mo()

    def main_function(self):
        self.check_if_mo_exist('uni/userext/user-', self.local_user, User, 'User')
        add_user_domain(self.mo, self.user_domain)

if __name__ == '__main__':
    user_domain = AddSecurityDomain()