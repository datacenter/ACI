from cobra.model.aaa import DomainRef
from createMo import *


def input_key_args(msg='\nPlease Specify Security Domain:'):
    print msg
    return input_raw_input("Security Domain Name", required=True)


def add_security_domain(parent_mo, security_domain):
    """Add a Security Domain to a Tenant. A reference to the domain that the parent object belongs. """
    aaa_domain_ref = DomainRef(parent_mo, security_domain)


class AddSecurityDomain(CreateMo):

    def __init__(self):
        self.description = 'Add a Security Domain to a Tenant. A reference to the domain that the parent object belongs. '
        self.tenant_required = True
        self.security_domain = None
        super(AddSecurityDomain, self).__init__()

    def set_cli_mode(self):
        super(AddSecurityDomain, self).set_cli_mode()
        self.parser_cli.add_argument('security_domain', help='Security Domain Name')

    def read_key_args(self):
        self.security_domain = self.args.pop('security_domain')

    def wizard_mode_input_args(self):
        self.args['security_domain'] = input_key_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-'+self.tenant+'/domain-', self.security_domain, DomainRef, description='Security Domain')
        super(AddSecurityDomain, self).delete_mo()

    def main_function(self):
        # Query a tenant
        parent_mo = self.check_if_tenant_exist()
        add_security_domain(parent_mo, self.security_domain)

if __name__ == '__main__':
    security_domain = AddSecurityDomain()