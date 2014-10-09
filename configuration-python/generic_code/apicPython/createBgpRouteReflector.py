from cobra.model.bgp import RRNodePEp

from createMo import *

DEFAULT_CONSTANT = 'unspecified'

CHOICES = []


def input_key_args(msg='\nPlease Specify BGP Route Reflector:'):
    print msg
    return input_raw_input("Spine ID", required=True)


def create_bgp_route_reflector(bgp_rrp, reflector_id):
    """Set the route reflector node policy endpoint."""
    bgp_rrnodepep = RRNodePEp(bgp_rrp, reflector_id)


class CreateBgpRouteReflector(CreateMo):

    def __init__(self):
        self.description = 'Set the route reflector node policy endpoint.'
        self.reflector_id = None
        super(CreateBgpRouteReflector, self).__init__()

    def set_cli_mode(self):
        super(CreateBgpRouteReflector, self).set_cli_mode()
        self.parser_cli.add_argument('reflector_id', help=' The spine node ID.')

    def read_key_args(self):
        self.reflector_id = self.args.pop('reflector_id')

    def wizard_mode_input_args(self):
        self.args['reflector_id'] = input_key_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/fabric/bgpInstP-default/rr/node-', str(self.reflector_id), detail_description='Spine ID has been set as a route reflector node policy endpoint.')
        super(CreateBgpRouteReflector, self).delete_mo()

    def main_function(self):
        # Query a tenant
        bgp_rrp = self.look_up_mo('uni/fabric/bgpInstP-default/rr', '')
        create_bgp_route_reflector(bgp_rrp, self.reflector_id)

if __name__ == '__main__':
    mo = CreateBgpRouteReflector()
