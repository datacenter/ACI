from cobra.model.infra import AttEntityP, RsDomP, ProvAcc, FuncP, AccPortGrp, RsAttEntP

from createMo import *

DEFAULT_ENABLE_INFRASTRUCTURE_VLAN = 'False'

CHOICES = []


def input_key_args(msg='\nPlease Specify the Entity Profile:'):
    print msg
    return input_raw_input("Profile Name", required=True)


def input_domain_name():
    return input_raw_input('Domain name', required=True)


def input_optional_args():
    args = {}
    args['enable_infrastructure_vlan'] = input_raw_input('Enable Infrastructure VLAN', default=DEFAULT_ENABLE_INFRASTRUCTURE_VLAN)
    args['domain_profiles'] = read_add_mos_args(add_mos('Add a Domain Profile', input_domain_name))
    args['interface_policy_group'] = input_raw_input('Interface Policy Group')
    return args


def create_attachable_access_entity_profile(infra, entity_profile, **args):
    """Create an attached entity profile. This provides a template to deploy hypervisor policies on a large set of leaf ports. This also provides the association of a Virtual Machine Management (VMM) domain and the physical network infrastructure. """
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    
    infra_attentityp = AttEntityP(infra, entity_profile)

    if 'enable_infrastructure_vlan' in args.keys():
        if args['enable_infrastructure_vlan'] in [True, 'True']:
            infra_provacc = ProvAcc(infra_attentityp)
        elif args['enable_infrastructure_vlan'] in [False, 'False']:
            infra_provacc = ProvAcc(infra_attentityp)
            infra_provacc.delete()

    if 'domain_profiles' in args.keys() and is_valid(args['domain_profiles']):
        for domain in args['domain_profiles']:
            infra_rsdomp = RsDomP(infra_attentityp, 'uni/phys-'+domain)

    if is_valid_key(args, 'interface_policy_group'):
        infra_funcp = FuncP(infra)
        infra_accportgrp = AccPortGrp(infra_funcp, args['interface_policy_group'])
        infra_rsattentp = RsAttEntP(infra_accportgrp)

    return infra_attentityp


class CreateAttachableAccessEntityProfile(CreateMo):

    def __init__(self):
        self.description = 'Create an attached entity profile. This provides a template to deploy hypervisor policies on a large set of leaf ports. This also provides the association of a Virtual Machine Management (VMM) domain and the physical network infrastructure.'
        self.entity_profile = None
        super(CreateAttachableAccessEntityProfile, self).__init__()

    def set_cli_mode(self):
        super(CreateAttachableAccessEntityProfile, self).set_cli_mode()
        self.parser_cli.add_argument('entity_profile', help='The attached entity profile name.')
        self.parser_cli.add_argument('-v', '--enable_infrastructure_vlan', default= DEFAULT_ENABLE_INFRASTRUCTURE_VLAN, help='The provider access function. This is defined when the hypervisor is using an encapsulation protocol, such as VxLAN/NVGRE, and provides the policies to impacting VxLAN/NvGRE packets from NVGRE.')
        self.parser_cli.add_argument('-d', '--domains', dest='domain_profiles', nargs="*", help=' relation to a physical or virtual domain. Users need to create this to provide association between physical infrastructure policies and the domains.')
        self.parser_cli.add_argument('-g', '--interface_policy_group', help='The attachable policy group acts as an override of the policies given at the AccBaseGrp for the ports associated with the Attachable Entity Profile.')

    def read_key_args(self):
        self.entity_profile = self.args.pop('entity_profile')

    def wizard_mode_input_args(self):
        self.args['entity_profile'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/infra/attentp-', self.entity_profile, AttEntityP, description='Attachable Access Entity Profile')
        super(CreateAttachableAccessEntityProfile, self).delete_mo()

    def main_function(self):
        # Query a tenant
        self.look_up_mo('uni/infra','')
        create_attachable_access_entity_profile(self.mo, self.entity_profile, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateAttachableAccessEntityProfile()