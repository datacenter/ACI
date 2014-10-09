from cobra.model.vmm import DomP, CtrlrP, RsAcc, UsrAccP, RsMgmtEPg, RsVmmCtrlrP, RsVxlanNs, RsMcastAddrNs

from createVcenterDomain import input_key_args as input_vcenter_domain
from createMo import *


DEFAULT_MANAGEMENT_EPG = None
DEFAULT_ASSOCIATED_CREDENTIAL = None
DEFAULT_ASSOCIATED_VCENTER_CONTROLLER = None
DEFAULT_VXLAN_POOL = None
DEFAULT_MULTICAST_ADDRESS_POOL = None

VMM_PROVIDER_CHOICES = ['VMware', 'Microsoft']


def input_key_args(msg='\nPlease Specify vShield Controller:', delete_function=False):
    print msg
    args = [input_raw_input("The name of the vShield Controller profile", required=True)]
    if not delete_function:
        args.append(input_raw_input("Host Name or IP Address", required=True))
    else:
        args.extend([None])
    return args


def input_optional_args(stats_mode_only=False):
    args = {}
    args['management_epg'] = input_raw_input('Management EPG', default=DEFAULT_MANAGEMENT_EPG)
    args['associated_credential'] = input_raw_input('Associated Credential', default=DEFAULT_ASSOCIATED_CREDENTIAL)
    args['associated_vcenter_controller'] = input_raw_input('Associated vCenter Controller', default=DEFAULT_ASSOCIATED_VCENTER_CONTROLLER)
    args['associated_vxlan_pool'] = input_raw_input('VXLAN Pool', default=DEFAULT_VXLAN_POOL)
    args['associated_multicast_address_pool'] = input_raw_input('Multicast Address Pool', default=DEFAULT_MULTICAST_ADDRESS_POOL)
    return args


def create_vshieldr_controller(vmm_domp, provider, vcenter_domain, controller, host_or_ip, **args):
    """Create vShield Controller"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    vmm_ctrlrp = CtrlrP(vmm_domp, controller,
                        hostOrIp=host_or_ip,
                        scope='iaas')

    if is_valid_key(args, 'management_epg'):
        vmm_rsmgmtepg = RsMgmtEPg(vmm_ctrlrp, tDn='uni/tn-mgmt/out-vmm/instP-' + args['management_epg'])

    if is_valid_key(args, 'associated_vcenter_controller'):
        vmm_rsvmmctrlrp = RsVmmCtrlrP(vmm_ctrlrp, tDn='uni/vmmp-'+provider+'/dom-'+vcenter_domain+'/ctrlr-' + args['associated_vcenter_controller'])

    if is_valid_key(args, 'associated_vxlan_pool'):
        vmm_rsvxlanns = RsVxlanNs(vmm_ctrlrp, tDn='uni/infra/vxlanns-' + args['associated_vxlan_pool'])

    if is_valid_key(args, 'associated_multicast_address_pool'):
        vmm_rsmcastaddrns = RsMcastAddrNs(vmm_ctrlrp, tDn='uni/infra/maddrns-' + args['associated_multicast_address_pool'])

    return vmm_ctrlrp


def define_associated_credential(vmm_ctrlrp, vmm_usraccp_path):
    """define_associated_credential"""
    vmm_rtctrlrp = RsAcc(vmm_ctrlrp, tDn=vmm_usraccp_path)
    return vmm_ctrlrp


class CreateVShieldControlle(CreateMo):

    def __init__(self):
        self.description = 'Create vShield Controller'
        self.vcenter_provider = None
        self.vcenter_domain = None
        self.management_epg = None
        self.vshield_controller = None
        self.associated_credential = None
        self.associated_vxlan_pool = None
        self.associated_multicast_address_pool = None
        super(CreateVShieldControlle, self).__init__()

    def set_cli_mode(self):
        super(CreateVShieldControlle, self).set_cli_mode()
        self.parser_cli.add_argument('vcenter_provider', help='The provider profile vendor.', choices=VMM_PROVIDER_CHOICES)
        self.parser_cli.add_argument('vcenter_domain', help='Holds the domain profile name.')
        self.parser_cli.add_argument('vshield_controller', help='Holds the name of the controller profile.')
        self.parser_cli.add_argument('host_or_ip', help='Host Name or IP Address.')
        self.parser_cli.add_argument('-e', '--management_epg', help='A relation to a set of endpoints.')
        self.parser_cli.add_argument('-c', '--associated_vcenter_controller', help='A relation to the VMM controller profile, which specifies how to connect to a single VM management controller that is part of containing policy enforcement domain.')
        self.parser_cli.add_argument('-a', '--associated_credential', help='Associate a VM credential account to the controller.')
        self.parser_cli.add_argument('-x', '--associated_vxlan_pool', help='A relation to the VXLAN namespace policy definition.')
        self.parser_cli.add_argument('-m', '--associated_multicast_address_pool', help='A relation to the policy definition of the multicast IP address ranges.')

    def read_key_args(self):
        self.vcenter_provider = self.args.pop('vcenter_provider')
        self.vcenter_domain = self.args.pop('vcenter_domain')
        self.vshield_controller = self.args.pop('vshield_controller')
        self.host_or_ip = self.args.pop('host_or_ip')

    def wizard_mode_input_args(self):
        self.args['vcenter_provider'], self.args['vcenter_domain'] = input_vcenter_domain()
        self.args['vshield_controller'], self.args['host_or_ip'] = input_key_args(delete_function=self.delete)
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        vmm_domp = self.check_if_mo_exist('uni/vmmp-' + self.vcenter_provider + '/dom-', self.vcenter_domain, DomP, description='VMM Domain')
        CtrlrP(vmm_domp, self.vshield_controller).delete()

    def main_function(self):
        vmm_domp = self.check_if_mo_exist('uni/vmmp-' + self.vcenter_provider + '/dom-', self.vcenter_domain, DomP, description='VMM Domain')
        vmm_ctrlrp = create_vshieldr_controller(vmm_domp, self.vcenter_provider, self.vcenter_domain, self.vshield_controller, self.host_or_ip, optional_args=self.optional_args)
        if is_valid_key(self.optional_args, 'associated_credential'):
            vmm_usraccp_path = 'uni/vmmp-' + self.vcenter_provider + '/dom-' + self.vcenter_domain + '/usracc-' + self.optional_args['associated_credential']
            vmm_usraccp = self.check_if_mo_exist(vmm_usraccp_path, '', UsrAccP, description='vCenter Credential', set_mo=False)
            define_associated_credential(vmm_ctrlrp, vmm_usraccp_path)

if __name__ == '__main__':
    mo = CreateVShieldControlle()