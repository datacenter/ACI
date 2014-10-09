from cobra.model.aaa import User, UserDomain, UserRole

from createMo import *

DEFAULT_ROLE_TYPE = 'readPriv'

ROLE_TYPE_CHOICES = ['readPriv', 'writePriv']


def input_user_name(msg=''):
    print msg
    return input_raw_input('User Name', required=True)


def input_security_domain(msg=''):
    print msg
    return input_raw_input("Security Domain Name", required=True)


def input_key_args(delete_function=False):
    args = []
    args.append(input_raw_input('The name of a privilege role', required=True))
    if not delete_function:
        args.append(input_options('The privilege type for a user role.', DEFAULT_ROLE_TYPE, ROLE_TYPE_CHOICES, required=True))
    else:
        args.extend([None])
    return args


def choose_role_for_user(aaa_domain, role, role_type):
    """The privilege bitmask of a user domain."""
    aaa_role = UserRole(aaa_domain, role, privType=role_type)


class ChooseRoleForUser(CreateMo):

    def __init__(self):
        self.description = 'The privilege bitmask of a user domain.'
        self.user_name = None
        self.security_domain = None
        self.role = None
        self.role_type = None
        super(ChooseRoleForUser, self).__init__()

    def set_cli_mode(self):
        super(ChooseRoleForUser, self).set_cli_mode()
        self.parser_cli.add_argument('user_name', help='The name of a locally-authenticated user account.')
        self.parser_cli.add_argument('security_domain', help='The name of the user domain')
        self.parser_cli.add_argument('role', help='The name of a privilege role.')
        self.parser_cli.add_argument('role_type', default= DEFAULT_ROLE_TYPE, choices=ROLE_TYPE_CHOICES, help='The privilege type for a user role.')

    def read_key_args(self):
        self.user_name = self.args.pop('user_name')
        self.security_domain = self.args.pop('security_domain')
        self.role = self.args.pop('role')
        self.role_type = self.args.pop('role_type')

    def wizard_mode_input_args(self):
        self.args['user_name'] = input_user_name()
        self.args['security_domain'] = input_security_domain()
        self.args['role'], self.args['role_type'] = input_key_args(delete_function=self.delete)

    def delete_mo(self):
        self.check_if_mo_exist('uni/userext/user-' + self.user_name + '/userdomain-' +self.security_domain + '/role-' + self.role)
        super(ChooseRoleForUser, self).delete_mo()

    def main_function(self):
        self.check_if_mo_exist('uni/userext/user-' , self.user_name, module=User, description='User')
        self.check_if_mo_exist('uni/userext/user-' + self.user_name + '/userdomain-', mo_name=self.security_domain, module=UserDomain, description='User Domain')
        choose_role_for_user(self.mo, self.role, self.role_type)

if __name__ == '__main__':
    mo = ChooseRoleForUser()