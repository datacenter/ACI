from cobra.model.vmm import DomP, UsrAccP
from createVmmDomain import input_key_args as input_vmm_domain_args

from createMo import *

VMM_PROVIDER_CHOICES = ['VMware', 'Microsoft']


def input_key_args(msg='\nPlease Specify vCenter Credential:', delete_function=False):
    print msg
    args = [input_raw_input("The user account profile name", required=True)]
    if not delete_function:
        args.append(input_raw_input("User Name", required=True))
        args.append(input_raw_input("Password", required=True))
    else:
        args.extend([None, None])
    return args


def create_vcenter_credential(vmm_domp, profile, vmm_user, vmm_pw):
    """Create a vCenter Credential"""
    vmm_usraccp = UsrAccP(vmm_domp, profile, usr=vmm_user, pwd=vmm_pw)


class CreateVcenterCredential(CreateMo):

    def __init__(self):
        self.description = 'Create a vCenter Credential, the user account profile, which contains a profile name, username, description, and other related information.'
        self.vmm_provider = None
        self.vmm_domain = None
        self.profile = False
        self.vmm_user = False
        self.vmm_password = False
        super(CreateVcenterCredential, self).__init__()

    def set_cli_mode(self):
        super(CreateVcenterCredential, self).set_cli_mode()
        self.parser_cli.add_argument('vmm_provider', help='The provider profile vendor.', choices=VMM_PROVIDER_CHOICES)
        self.parser_cli.add_argument('vmm_domain', help='Holds the domain profile name.')
        self.parser_cli.add_argument('profile', help='The user account profile name.')
        self.parser_cli.add_argument('vmm_user', help='User Name.')
        self.parser_cli.add_argument('vmm_password', help='User Password.')

    def read_key_args(self):
        self.vmm_provider = self.args.pop('vmm_provider')
        self.vmm_domain = self.args.pop('vmm_domain')
        self.profile = self.args.pop('profile')
        self.vmm_user = self.args.pop('vmm_user')
        self.vmm_password = self.args.pop('vmm_password')

    def wizard_mode_input_args(self):
        self.args['vmm_provider'], self.args['vmm_domain'] = input_vmm_domain_args()
        self.args['profile'], self.args['vmm_user'], self.args['vmm_password'] = input_key_args(delete_function=self.delete)

    def delete_mo(self):
        self.check_if_mo_exist('uni/vmmp-' + self.vmm_provider + '/dom-' + self.vmm_domain + '/usracc-', self.profile, UsrAccP, description='vCenter Credential')
        super(CreateVcenterCredential, self).delete_mo()

    def main_function(self):
        # Query a tenant
        parent_mo = self.check_if_mo_exist('uni/vmmp-' + self.vmm_provider + '/dom-', self.vmm_domain, DomP, description='VMM Domain')
        create_vcenter_credential(parent_mo, self.profile, self.vmm_user, self.vmm_password)

if __name__ == '__main__':
    mo = CreateVcenterCredential()