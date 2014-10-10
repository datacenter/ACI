from labScript import *

from apicPython import createDnsProfile
from apicPython import addPrivateL3Network


class LabConfiguringDnsServerPolicy(LabScript):

    def __init__(self):
        self.description = 'Configuring a DNS Server Policy.'
        self.tenant_required = True
        self.private_network = None
        self.dns_profile = None
        super(LabConfiguringDnsServerPolicy, self).__init__()

    def run_yaml_mode(self):
        super(LabConfiguringDnsServerPolicy, self).run_yaml_mode()
        self.private_network = self.args['private_network']
        self.dns_profile = self.args['dns_profile']
        self.optional_args = self.args['optional_args']

    def wizard_mode_input_args(self):
        self.dns_profile = createDnsProfile.input_key_args()
        self.private_network = addPrivateL3Network.input_key_args()
        self.optional_args = createDnsProfile.input_optional_args()

    def main_function(self):
        # create DNS Policy
        self.look_up_mo('uni/fabric', '')
        createDnsProfile.create_dns_profile(self.mo, self.dns_profile, optional_args=self.optional_args)
        self.commit_change()

        self.check_if_tenant_exist()
        addPrivateL3Network.create_private_network(self.mo, self.private_network, dns_label=self.dns_profile)


if __name__ == '__main__':
    mo = LabConfiguringDnsServerPolicy()