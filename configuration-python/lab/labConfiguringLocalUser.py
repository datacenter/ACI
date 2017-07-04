from labScript import *
from apicPython import createLocalUser
from apicPython import addUserDomain
from apicPython import chooseRoleForUser


class ConfiguringLocalUser(LabScript):
    """
    Create A locally-authenticated user account.
    """
    def __init__(self):
        self.description = 'Create A locally-authenticated user account.'
        self.local_user = None
        self.local_password = None
        self.local_user_optional_args = None
        self.user_domains = []
        super(ConfiguringLocalUser, self).__init__()

    def run_yaml_mode(self):
        super(ConfiguringLocalUser, self).run_yaml_mode()
        self.local_user = self.args['local_user']
        self.local_password = self.args['local_password']
        self.local_user_optional_args = self.args['optional_args']
        self.user_domains = self.args['user_domains']

    def wizard_mode_input_args(self):
        self.local_user, self.password = createLocalUser.input_key_args()
        self.local_user_optional_args = createLocalUser.input_optional_args()
        user_domains = add_mos('Add a User Domain', addUserDomain.input_key_args)
        for user_domain in user_domains:
            roles = add_mos('Choose a role for User Domain "' + user_domain['key_args'] + '"', chooseRoleForUser.input_key_args)
            ud = {'name': user_domain['key_args'], 'roles': []}
            for role in roles:
                ud['roles'].append({'role_name': role['key_args'][0],
                                    'role_type': role['key_args'][1]})
            self.user_domains.append(ud)

    def main_function(self):
        self.look_up_mo('uni/userext', '')
        aaa_user = createLocalUser.create_local_user(self.mo, self.local_user, self.local_password, optional_args=self.local_user_optional_args)
        for user_domain in self.user_domains:
            aaa_userdomain = addUserDomain.add_user_domain(aaa_user, user_domain['name'])
            for role in user_domain['roles']:
                chooseRoleForUser.choose_role_for_user(aaa_userdomain, role['role_name'], role['role_type'])


if __name__ == '__main__':
    mo = ConfiguringLocalUser()