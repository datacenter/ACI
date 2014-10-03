from cobra.model.vmm import DomP, CtrlrP, RsAcc, UsrAccP, RsMgmtEPg
from createVcenterDomain import input_key_args as input_vcenter_domain

from createMo import *

DEFAULT_STATS_MODE = 'disabled'
DEFAULT_ASSOCIATED_CREDENTIAL = None
DEFAULT_MANAGEMENT_EPG = None

VMM_PROVIDER_CHOICES = ['VMware', 'Microsoft']
STATS_MODE_CHOICES = ['enabled', 'disabled']


def input_key_args(msg='\nPlease Specify vCenter Controller:', delete_function=False):
    print msg
    args = [input_raw_input("The name of the controller profile", required=True)]
    if not delete_function:
        args.append(input_raw_input("Host Name or IP Address", required=True))
        args.append(input_raw_input("Datacenter,top level container name.", required=True))
    else:
        args.extend([None, None])
    return args


def input_optional_args(stats_mode_only=False):
    args = {}
    args['stats_mode'] = input_options('The Statistics Mode.', DEFAULT_STATS_MODE , STATS_MODE_CHOICES)
    if not stats_mode_only:
        args['management_epg'] = input_raw_input('Management EPG', default=DEFAULT_MANAGEMENT_EPG)
        args['associated_credential'] = input_raw_input('Associated Credential', default=DEFAULT_ASSOCIATED_CREDENTIAL)
    return args


def create_vcenter_controller(vmm_domp, controller, host_or_ip, data_center, **args):
    """Create vCenter Controller"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    vmm_ctrlrp = CtrlrP(vmm_domp, controller,
                        hostOrIp=host_or_ip, rootContName=data_center,
                        statsMode=get_value(args, 'stats_mode', DEFAULT_STATS_MODE))

    if is_valid_key(args, 'management_epg'):
        vmm_rsmgmtepg = RsMgmtEPg(vmm_ctrlrp, tDn='uni/tn-mgmt/out-vmm/instP-' + args['management_epg'])

    return vmm_ctrlrp


def define_associated_credential(vmm_ctrlrp, vmm_usraccp_path):
    """define_associated_credential"""
    vmm_rtctrlrp = RsAcc(vmm_ctrlrp, tDn=vmm_usraccp_path)
    return vmm_ctrlrp


class CreateVcenterController(CreateMo):

    def __init__(self):
        self.description = 'Create vCenter Controller'
        self.vmm_provider = None
        self.vmm_domain = None
        self.vcenter_controller = None
        self.host_or_ip = None
        self.data_center = None
        super(CreateVcenterController, self).__init__()

    def set_cli_mode(self):
        super(CreateVcenterController, self).set_cli_mode()
        self.parser_cli.add_argument('vmm_provider', help='The provider profile vendor.', choices=VMM_PROVIDER_CHOICES)
        self.parser_cli.add_argument('vmm_domain', help='Holds the domain profile name.')
        self.parser_cli.add_argument('vcenter_controller', help='Holds the name of the controller profile.')
        self.parser_cli.add_argument('host_or_ip', help='Host Name or IP Address.')
        self.parser_cli.add_argument('data_center', help='Top level container name.')
        self.parser_cli.add_argument('-s', '--stats_mode', dest='statsMode', default= DEFAULT_STATS_MODE, choices=STATS_MODE_CHOICES, help='The Statistics Mode.')
        self.parser_cli.add_argument('-e', '--management_epg', help='A relation to a set of endpoints.')
        self.parser_cli.add_argument('-a', '--associated_credential', help='Associate a VM credential account to the controller.')

    def read_key_args(self):
        self.vmm_provider = self.args.pop('vmm_provider')
        self.vmm_domain = self.args.pop('vmm_domain')
        self.vcenter_controller = self.args.pop('vcenter_controller')
        self.host_or_ip = self.args.pop('host_or_ip')
        self.data_center = self.args.pop('data_center')

    def wizard_mode_input_args(self):
        self.args['vmm_provider'], self.args['vmm_domain'] = input_vcenter_domain()
        self.args['vcenter_controller'], self.args['host_or_ip'], self.args['data_center'] = input_key_args(delete_function=self.delete)
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        vmm_domp = self.check_if_mo_exist('uni/vmmp-' + self.vmm_provider + '/dom-', self.vmm_domain, DomP, description='VMM Domain')
        CtrlrP(vmm_domp, self.vcenter_controller).delete()

    def main_function(self):
        vmm_domp = self.check_if_mo_exist('uni/vmmp-' + self.vmm_provider + '/dom-', self.vmm_domain, DomP, description='VMM Domain')
        vmm_ctrlrp = create_vcenter_controller(vmm_domp, self.vcenter_controller, self.host_or_ip, self.data_center, optional_args=self.optional_args)
        if is_valid_key(self.optional_args, 'associated_credential'):
            vmm_usraccp_path = 'uni/vmmp-' + self.vmm_provider + '/dom-' + self.vmm_domain + '/usracc-' + self.optional_args['associated_credential']
            vmm_usraccp = self.check_if_mo_exist(vmm_usraccp_path, '', UsrAccP, description='vCenter Credential', set_mo=False)
            define_associated_credential(vmm_ctrlrp, vmm_usraccp_path)

if __name__ == '__main__':
    mo = CreateVcenterController()