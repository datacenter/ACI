from cobra.model.bgp import AsP
from createMo import *


def input_key_args(msg='\nPlease Specify the Autonomous System Number:'):
    print msg
    return input_raw_input("Autonomous System Number", required=True)


def setAutonomousSystemNumber(bgp_instpol, autonomous_system_number):
    """Set the number that uniquely identifies an autonomous system """
    bgp_asp = AsP(bgp_instpol, asn=autonomous_system_number)


class SetAutonomousSystemNumber(CreateMo):

    def __init__(self):
        self.description = 'The BGP autonomous system profile information. Determine the number that uniquely identifies an autonomous system.'
        self.tenant_required = False
        self.autonomous_system_number = None
        super(SetAutonomousSystemNumber, self).__init__()

    def set_cli_mode(self):
        super(SetAutonomousSystemNumber, self).set_cli_mode()
        self.parser_cli.add_argument('autonomous_system_number', help='A number that uniquely identifies an autonomous system.')

    def read_key_args(self):
        self.autonomous_system_number = self.args.pop('autonomous_system_number')

    def wizard_mode_input_args(self):
        if not self.delete:
            self.args['autonomous_system_number'] = input_key_args()
        else:
            self.args['autonomous_system_number'] = None

    def delete_mo(self):
        self.check_if_mo_exist('uni/fabric/bgpInstP-default/as', '', AsP, description='Autonomous System Number')
        super(SetAutonomousSystemNumber, self).delete_mo()

    def main_function(self):
        # Query a tenant
        bgp_instpol = self.look_up_mo('uni/fabric/bgpInstP-default','')
        setAutonomousSystemNumber(bgp_instpol, self.autonomous_system_number)

if __name__ == '__main__':
    mo = SetAutonomousSystemNumber()