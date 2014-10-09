from cobra.model.vmm import DomP
from cobra.model.infra import RsVlanNs

from createMo import *


DEFAULT_VLAN = 'None'

VMM_PROVIDER_CHOICES = ['VMware', 'Microsoft']
VLAN_MODE_CHOICES = ['dynamic', 'static']

CHOICES = []


def input_key_args(msg='\nPlease Specify VMM Domain:', only_vmm_domain=False):
    print msg
    args = []
    if not only_vmm_domain:
        args.append(input_options("VMM Provider Name", '', VMM_PROVIDER_CHOICES, required=True))
    args.append(input_raw_input("VMM Domain Name", required=True))
    return args


def input_optional_args():
    args = {}
    args['vlan'] = input_raw_input('Vlan Name', default=DEFAULT_VLAN)
    if args['vlan'] not in ['None', 'none', 'NONE', '']:
        args['vlan_mode'] = input_options("Vlan Mode", '', VLAN_MODE_CHOICES, required=True)
    return args


def create_vcenter_domain(vmm_provp, vmm_domain, **args):
    """Create a VMM Domain. This is a policy for grouping VM controllers with similar networking policy requirements. For example, the VM controllers can share VLAN or VXLAN space and application endpoint groups. The APIC communicates with the controller to publish network configurations such as port groups that are then applied to the virtual workloads."""
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    vmm_domp = DomP(vmm_provp, vmm_domain)
    if 'vlan' in args.keys() and 'vlan_mode' in args.keys() and is_valid(args['vlan'], args['vlan_mode']):
        infra_revlanns = RsVlanNs(vmm_domp,tDn='uni/infra/vlanns-[' + args['vlan'] + ']-' + args['vlan_mode'])
    return vmm_domp


class CreateVcenterDomain(CreateMo):

    def __init__(self):
        self.description = 'Create a VMM Domain. This is a policy for grouping VM controllers with similar networking policy requirements. For example, the VM controllers can share VLAN or VXLAN space and application endpoint groups. The APIC communicates with the controller to publish network configurations such as port groups that are then applied to the virtual workloads.'
        self.vmm_provider = None
        self.vmm_domain = None
        super(CreateVcenterDomain, self).__init__()

    def set_cli_mode(self):
        super(CreateVcenterDomain, self).set_cli_mode()
        self.parser_cli.add_argument('vmm_provider', help='The provider profile vendor.', choices=VMM_PROVIDER_CHOICES)
        self.parser_cli.add_argument('vmm_domain', help='Holds the domain profile name.')
        self.parser_cli.add_argument('-v', '--vlan',help='A relation to the policy definition for ID ranges used for VLAN encapsulation.')
        self.parser_cli.add_argument('-m', '--vlan_mode', help='Allocation Mode of the VLAN')

    def read_key_args(self):
        self.vmm_provider = self.args.pop('vmm_provider')
        self.vmm_domain = self.args.pop('vmm_domain')

    def wizard_mode_input_args(self):
        self.args['vmm_provider'], self.args['vmm_domain'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/vmmp-' + self.vmm_provider + '/dom-', self.vmm_domain, DomP, description='VMM Domain')
        super(CreateVcenterDomain, self).delete_mo()

    def main_function(self):
        self.check_if_mo_exist('uni/vmmp-' + self.vmm_provider)
        create_vcenter_domain(self.mo, self.vmm_domain, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateVcenterDomain()