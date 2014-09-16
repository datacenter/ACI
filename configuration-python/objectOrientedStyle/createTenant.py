from createMo import *


def input_key_args(msg='\nPlease Specify the Tenant:'):
    print msg
    return input_raw_input("Tenant Name", required=True)


def create_tenant(parent_mo, tenant):
    """Create a tenant"""
    fvTenant = Tenant(parent_mo, tenant)


class CreateTenant(CreateMo):
    """
    Create a Tenant
    """
    def __init__(self):
        self.description = 'Create a Tenant'
        self.tenant_required = True
        super(CreateTenant, self).__init__()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-', self.tenant, Tenant, description='Tenant')
        super(CreateTenant, self).delete_mo()

    def createTenant(self):
        self.mo = self.modir.lookupByDn('uni')
        create_tenant(self.mo, self.tenant)

if __name__ == '__main__':
    mo = CreateTenant()