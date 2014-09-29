from cobra.model.aaa import User, UserDomain

from createMo import *

DEFAULT_EMPTY = ''
DEFAULT_STATUS = 'active'
DEFAULT_EXPIRES = 'no'
DEFAULT_EXPIRATION = 'never'

STATUS_CHOICES = ['inactive', 'active']
EXPIRES_CHOICES = ['yes', 'no']


def input_password(length=8):
    pw = input_raw_input("Password", required=True)
    if len(pw) < length:
        print 'password must be minimum 8 characters'
        return input_password(length=length)
    return pw


def input_key_args(msg='\nPlease input User info:', user_only=False, delete_function=False):
    print msg
    args = []
    args.append(input_raw_input("Local User Name", required=True))
    if not delete_function and not user_only:
        args.append(input_password())
    else:
        args.extend([None])
    return args


def input_optional_args():
    args = {}
    args['first_name'] = input_raw_input('User First Name', DEFAULT_EMPTY)
    args['last_name'] = input_raw_input('User Last Name', DEFAULT_EMPTY)
    args['phone'] = input_raw_input('User Phone Number', DEFAULT_EMPTY)
    args['email'] = input_raw_input('User Email', DEFAULT_EMPTY)
    args['description'] = input_raw_input('User Description', DEFAULT_EMPTY)
    args['status'] = input_options('Accout Status', DEFAULT_STATUS, STATUS_CHOICES)
    args['expires'] = input_options('Account Status', DEFAULT_EXPIRES, EXPIRES_CHOICES)
    if args['expires'] == 'yes':
        args['expiration_date'], = input_raw_input('The Date that Account Expires (Format: YYYY-MM-DD HH:MM:SS AM/PM): ', required=True),
    return args


def create_local_user(aaa_userep, local_user, local_password, **args):
    """Create a locally-authenticated user account. """
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    if get_value(args, 'expires', DEFAULT_EXPIRES) != 'yes':
        args['expiration_date'] = DEFAULT_EXPIRATION
    aaa_user = User(aaa_userep, local_user, pwd=local_password,
                    firstName=get_value(args, 'first_name', DEFAULT_EMPTY),
                    lastName=get_value(args, 'last_name', DEFAULT_EMPTY),
                    phone=get_value(args, 'phone', DEFAULT_EMPTY),
                    email=get_value(args, 'email', DEFAULT_EMPTY),
                    descr=get_value(args, 'description', DEFAULT_EMPTY),
                    accountStatus=get_value(args, 'status', DEFAULT_STATUS),
                    expires=get_value(args, 'expires', DEFAULT_EXPIRES),
                    expiration=get_value(args, 'expiration_date', DEFAULT_EXPIRATION)
                    )
    return aaa_user

class CreateLocalUser(CreateMo):

    def __init__(self):
        self.description = 'Create a locally-authenticated user account. '
        self.local_user = None
        self.local_password = None
        super(CreateLocalUser, self).__init__()

    def set_cli_mode(self):
        super(CreateLocalUser, self).set_cli_mode()
        self.parser_cli.add_argument('local_user', help='The name of the locally-authenticated user.')
        self.parser_cli.add_argument('local_password', help='The system user password.')
        self.parser_cli.add_argument('-f', '--first_name', help='The first name of the locally-authenticated user.')
        self.parser_cli.add_argument('-l', '--last_name', help='The last name of the locally-authenticated user.')
        self.parser_cli.add_argument('-p', '--phone', help='The phone number of the locally-authenticated user.')
        self.parser_cli.add_argument('-E', '--email', help='The email address of the locally-authenticated user.')
        self.parser_cli.add_argument('--description', help='Specifies a description of the policy definition.')
        self.parser_cli.add_argument('-s', '--status', help='The status of the locally-authenticated user account.')
        self.parser_cli.add_argument('-e', '--expires', help='Enables an expiration date for the locally-authenticated user account.')
        self.parser_cli.add_argument('-d', '--expiration_date', help='The expiration date of the locally-authenticated user account. The expires property must be enabled to activate an expiration date. (Format: YYYY-MM-DD HH:MM:SS AM/PM)')

    def read_key_args(self):
        self.local_user = self.args.pop('local_user')
        self.local_password = self.args.pop('local_password')

    def wizard_mode_input_args(self):
        self.args['local_user'], self.args['local_password'] = input_key_args(delete_function=self.delete)
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/userext/user-', self.local_user, User, 'User')
        super(CreateLocalUser, self).delete_mo()

    def main_function(self):
        self.check_if_mo_exist('uni/userext')
        create_local_user(self.mo, self.local_user, self.local_password, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateLocalUser()


