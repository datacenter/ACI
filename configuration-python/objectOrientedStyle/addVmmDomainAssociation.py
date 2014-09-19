from cobra.model.fv import AEPg, RsDomAtt
from createVmmDomain import input_key_args as input_vmm_domain
from createMo import *

DEFAULT_IMMEDIACY = 'lazy'

IMMEDIACY_CHOICES = ['immediate', 'lazy']


def input_key_args(msg='\nAssociating EPG to vCenter Domain:'):
    print msg
    return input_raw_input("EPG", required=True)


def input_optional_args(*args):
    args = {}
    args['deployment_immediacy'] = input_options('Deploy Immediacy', DEFAULT_IMMEDIACY, IMMEDIACY_CHOICES)
    args['resolution_immediacy'] = input_options('Resolution Immediacy', DEFAULT_IMMEDIACY, IMMEDIACY_CHOICES)
    return args


def add_vmm_domain_association(fv_epg, vmm_domain, **args):
    """Add Vmm Domain Association"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    fv_rsdomatt = RsDomAtt(fv_epg, 'uni/vmmp-VMware/dom-' + vmm_domain,
                           instrImedcy=get_value(args, 'deployment_immediacy', DEFAULT_IMMEDIACY),
                           resImedcy=get_value(args, 'resolution_immediacy', DEFAULT_IMMEDIACY))


class AddVmmDomainAssociation(CreateMo):

    def __init__(self):
        self.description = 'The VMM domain profile, which is a policy pertaining to a single VM management domain that also corresponds to a single policy enforcement domain. A cluster of VMware VCs forms such a domain. '
        self.tenant_required = True
        self.epg = None
        self.vmm_domain = None
        super(AddVmmDomainAssociation, self).__init__()

    def set_cli_mode(self):
        super(AddVmmDomainAssociation, self).set_cli_mode()
        self.parser_cli.add_argument('application', help='Application Name')
        self.parser_cli.add_argument('epg', help='EPG Name')
        self.parser_cli.add_argument('vmm_domain', help='VMM Domain Name')
        self.parser_cli.add_argument('-d', '--deployment_immediacy', default= DEFAULT_IMMEDIACY, choices=IMMEDIACY_CHOICES, help='Instrumentation Immediacy Specification for when policies are instrumented in HW immediate: instrument policy in hardware as soon as policy is resolved at the node lazy: instrument policy in hardware only when EP shows up This immediacy constraint is specified at EPG-level, and is copied into EPP, and is enforced per EPP.')
        self.parser_cli.add_argument('-r', '--resolution_immediacy', default= DEFAULT_IMMEDIACY, choices=IMMEDIACY_CHOICES, help='Resolution Immediacy Specification for CompMM/VMM binding: immediate: push to corresponding nodes ASAP as soon as policy is at CompMM/VMM lazy: push policies when VM/Comp is attached This immediacy constraint is specified at VMM/Comp Binding, and is copied into EPP, and is enforced per EPP.')

    def read_key_args(self):
        self.application = self.args.pop('application')
        self.epg = self.args.pop('epg')
        self.vmm_domain = self.args.pop('vmm_domain')

    def wizard_mode_input_args(self):
        self.args['application'] = self.input_application_name('')
        self.args['vmm_domain'] = input_vmm_domain(only_vmm_domain=True)
        self.args['epg'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/ap-' + self.application + '/epg-' + self.epg + '/rsdomAtt-[uni/vmmp-VMware/dom-' + self.vmm_domain + ']', '', RsDomAtt, description='VMM Domain Association')
        super(AddVmmDomainAssociation, self).delete_mo()

    def main_function(self):
        # Query a tenant
        fv_tenant = self.check_if_tenant_exist()
        fv_epg = self.check_if_mo_exist('uni/tn-' + self.tenant + '/ap-' + self.application + '/epg-', self.epg, AEPg, description='EPG')
        add_vmm_domain_association(fv_epg, self.vmm_domain, optional_args=self.args['optional_args'])


if __name__ == '__main__':
    mo = AddVmmDomainAssociation()