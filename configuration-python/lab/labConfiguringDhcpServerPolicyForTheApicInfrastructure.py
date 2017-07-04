from cobra.model.fv import BD

from labScript import *
from apicPython import createDhcpRelayPolicy
from apicPython import createDhcpRelayLabel


class LabConfiguringDhcpServerPolicyForTheApicInfrastructure(LabScript):

    def __init__(self):
        self.description = 'Configuring a DHCP Server Policy for the APIC Infrastructure.'
        self.tenant_required = True
        self.bridge_domain = None
        self.dhcp_relay_policy = None
        self.dhcp_relay_label_scope = None
        super(LabConfiguringDhcpServerPolicyForTheApicInfrastructure, self).__init__()

    def run_yaml_mode(self):
        super(LabConfiguringDhcpServerPolicyForTheApicInfrastructure, self).run_yaml_mode()
        self.tenant = self.args['tenant']
        self.bridge_domain = self.args['bridge_domain']
        self.dhcp_relay_policy = self.args['dhcp_relay_policy']
        self.dhcp_relay_label_scope = self.args['dhcp_relay_label_scope']

    def wizard_mode_input_args(self):
        self.bridge_domain = input_raw_input("Bridge Domain", required=True)
        self.dhcp_relay_policy = input_raw_input("DHCP Relay Profile Name", required=True)
        self.dhcp_relay_label_scope = input_options('DHCP Label Scope', '', ['infra', 'tenant'], required=True)
        self.args['optional_args'] = createDhcpRelayPolicy.input_optional_args()

    def main_function(self):

        # create DHCP Relay Policy
        self.check_if_tenant_exist()
        createDhcpRelayPolicy.create_dhcp_relay_policy(self.mo, self.dhcp_relay_policy, optional_args=return_valid_optional_args(self.args))
        self.commit_change()

        # set DHCP Relay Label
        self.check_if_mo_exist('uni/tn-'+self.tenant+'/BD-', self.bridge_domain, BD, 'Bridge Domain')
        createDhcpRelayLabel.create_dhcp_relay_label(self.mo, self.dhcp_relay_label_scope, self.dhcp_relay_policy, optional_args=return_valid_optional_args(self.args))

if __name__ == '__main__':
    mo = LabConfiguringDhcpServerPolicyForTheApicInfrastructure()