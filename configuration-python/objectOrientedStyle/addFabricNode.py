from cobra.model.fabric import NodeIdentP

from createMo import *


def input_key_args(msg='\nPlease Specify the Fabric Node:', delete_function=False):
    print msg
    args = [input_raw_input('Serial Number', required=True)]
    if not delete_function:
        args.append(input_raw_input('Node ID', required=True))
        args.append(input_raw_input('Node Name', required=True))
    else:
        args.extend([None, None])
    return args


def add_fabric_node(fv_pod, serial_num, node_id, node_name):
    """Create a Fabric Node"""
    fv_node = NodeIdentP(fv_pod, serial_num, nodeId=node_id, name=node_name)


class AddFabricNode(CreateMo):
    """
    Create a Filter
    """
    def __init__(self):
        self.description = 'Discover a Switch or Spine'
        self.tenant_required = False
        self.serial_number = None
        self.node_id = None
        self.node_name = None
        super(AddFabricNode, self).__init__()

    def set_cli_mode(self):
        super(AddFabricNode, self).set_cli_mode()
        self.parser_cli.add_argument('serial_number', help='Serial Number')
        self.parser_cli.add_argument('node_id', help='Node ID')
        self.parser_cli.add_argument('node_name', help='Node Name')

    def read_key_args(self):
        self.serial_number = self.args.pop('serial_number')
        self.node_id = self.args.pop('node_id')
        self.node_name = self.args.pop('node_name')

    def wizard_mode_input_args(self):
        self.args['serial_number'], self.args['node_id'], self.args['node_name'] = input_key_args(delete_function=self.delete)

    def delete_mo(self):
        self.check_if_mo_exist('uni/controller/nodeidentpol/nodep-', self.serial_number, NodeIdentP, description='Fabric Node')
        super(AddFabricNode, self).delete_mo()

    def main_function(self):
        parent_mo = self.check_if_mo_exist('uni/controller/nodeidentpol', description='Fabric Node')
        add_fabric_node(parent_mo, self.serial_number, self.node_id, self.node_name)

if __name__ == '__main__':
    mo = AddFabricNode()