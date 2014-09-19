from cobra.model.fv import Ap, AEPg
from cobra.model.vmm import DomP, CtrlrP, RsAcc, UsrAccP
import createVlanPool
import createVmmDomain
import createVcenterCredential
import createVcenterController
import addVmmDomainAssociation
from createMo import *


class Lab5IntegratingWithVMware(CreateMo):
    """
    Integrating With VMware
    """
    def __init__(self):
        self.description = 'Integrating With VMware'
        self.tenant_required = True
        self.vlan = None
        self.vlan_allocation_mode = None
        self.vlan_range_from = None
        self.vlan_range_to = None
        self.vmm_provider = None
        self.vmm_domain = None
        self.vmm_credential_profile = None
        self.vmm_user = None 
        self.vmm_password = None 
        self.vcenter_controller = None
        self.host_or_ip = None
        self.data_center = None
        self.stats_mode = None
        self.vmm_domain_associations = []
        super(Lab5IntegratingWithVMware, self).__init__()

    def set_argparse(self):
        super(Lab5IntegratingWithVMware, self).set_argparse()
        self.parser_cli = self.subparsers.add_parser(
            'cli', help='Not Support.'
        )

    def delete_mo(self):
        print 'Delete method is not supported in this function.'
        sys.exit()

    def set_cli_mode(self):
        pass

    def run_cli_mode(self):
        print 'CLI mode is not supported in this method. Please try Yaml mode or Wizard mode.'
        sys.exit()

    def run_yaml_mode(self):
        super(Lab5IntegratingWithVMware, self).run_yaml_mode()
        self.application = self.args['application']
        self.vlan = self.args['vlan']['name']
        self.vlan_allocation_mode = self.args['vlan']['mode']
        self.vlan_range_from = self.args['vlan']['from']
        self.vlan_range_to = self.args['vlan']['to']
        self.vmm_provider = self.args['vmm_provider']
        self.vmm_domain = self.args['vmm_domain']
        self.vmm_credential_profile = self.args['vcenter_credential']['profile']
        self.vmm_user = self.args['vcenter_credential']['user']
        self.vmm_password = self.args['vcenter_credential']['password']
        self.vcenter_controller = self.args['vcenter_controller']['profile']
        self.host_or_ip = self.args['vcenter_controller']['host_or_ip']
        self.data_center = self.args['vcenter_controller']['data_center']
        self.stats_mode = self.args['vcenter_controller']['mode']
        self.vmm_domain_associations = self.args['associated_epgs']

    def read_opt_args(self):
        pass

    def wizard_mode_input_args(self):
        self.input_application_name('')
        self.vlan, self.vlan_allocation_mode, self.vlan_range_from, self.vlan_range_to = createVlanPool.input_key_args('')
        self.vmm_provider, self.vmm_domain = createVmmDomain.input_key_args('')
        self.vmm_credential_profile, self.vmm_user, self.vmm_password = createVcenterCredential.input_key_args('')
        self.vcenter_controller, self.host_or_ip, self.data_center = createVcenterController.input_key_args('')
        self.stats_mode = createVcenterController.input_optional_args(True)['stats_mode']
        vmm_domain_associations = add_mos('Add a VMM Domain Association', addVmmDomainAssociation.input_key_args, addVmmDomainAssociation.input_optional_args)
        for vmm_domain_association in vmm_domain_associations:
            arg = {'name': vmm_domain_association['key_args'],
                   'optional_args': vmm_domain_association['opt_args']}
            self.vmm_domain_associations.append(arg)

    def main_function(self):
        # check if tenant and application both are existed.

        fv_tenant = self.check_if_tenant_exist()
        fv_ap = self.check_if_mo_exist('uni/tn-' + self.tenant + '/ap-', self.application, Ap, description='Application')

        # set self.mo to be the parent of VLAN Pool
        self.look_up_mo('uni/infra', '')
        createVlanPool.create_vlan_pool(self.mo, self.vlan, self.vlan_allocation_mode, self.vlan_range_from, self.vlan_range_to)
        self.commit_change()

        # set self.mo to be the parent of VMM Domain
        self.check_if_mo_exist('uni/vmmp-' + self.vmm_provider)
        createVmmDomain.create_vmm_domain(self.mo, self.vmm_domain, vlan=self.vlan, vlan_mode=self.vlan_allocation_mode)
        self.commit_change()

        # set self.mo to be the parent of vCenter Credential or vCenter Controller
        self.check_if_mo_exist('uni/vmmp-' + self.vmm_provider + '/dom-', self.vmm_domain, DomP, description='VMM Domain')
        createVcenterCredential.create_vcenter_credential(self.mo, self.vmm_credential_profile, self.vmm_user, self.vmm_password)
        vmm_ctrlrp = createVcenterController.create_vcenter_controller(self.mo, self.vcenter_controller, self.host_or_ip, self.data_center, stats_mode=self.stats_mode)
        createVcenterController.define_associated_credential(vmm_ctrlrp, 'uni/vmmp-' + self.vmm_provider + '/dom-' + self.vmm_domain + '/usracc-' + self.vmm_credential_profile)
        self.commit_change()

        for epg in self.vmm_domain_associations:
            fv_epg = self.check_if_mo_exist('uni/tn-' + self.tenant + '/ap-' + self.application + '/epg-', epg['name'], AEPg, description='EPG')
            addVmmDomainAssociation.add_vmm_domain_association(fv_epg, self.vmm_domain, optional_args=epg['optional_args'])
            self.commit_change()


if __name__ == '__main__':
    mo = Lab5IntegratingWithVMware()