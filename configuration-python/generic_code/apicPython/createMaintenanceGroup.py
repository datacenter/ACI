from cobra.model.maint import MaintGrp, MaintP, RsMgrpp, RsPolScheduler
from cobra.model.fabric import NodeBlk

from createMo import *

RUN_MODE_CHOICES = ['pauseOnlyOnFailures', 'pauseNever', 'pauseAlwaysBetweenSets']

DEFAULT_RUN_MODE = RUN_MODE_CHOICES[0]


def input_key_args(msg='\nPlease Specify the Maintenance Group:'):
    print msg
    return input_raw_input("Maintenance Group Name", required=True)


def input_group_node_id():
    return input_raw_input('Group Node ID', required=True)


def input_optional_args():
    args = {}
    args['run_mode'] = input_options('Run Mode', DEFAULT_RUN_MODE, RUN_MODE_CHOICES)
    args['scheduler'] = input_raw_input('Scheduler')
    args['group_node_ids'] = read_add_mos_args(add_mos('Add a Group Node Id', input_group_node_id))
    return args


def create_maintenance_group(parent_mo, maintenance_group, **args):
    """Create Maintenance Group"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    # Create mo
    maint_maintgrp = MaintGrp(parent_mo, maintenance_group)
    maint_rsmgrpp = RsMgrpp(maint_maintgrp, tnMaintMaintPName=maintenance_group)
    if is_valid_key(args, 'group_node_ids'):
        for group_node_id in args['group_node_ids']:
            fabric_nodeblk = NodeBlk(maint_maintgrp, group_node_id)
    maint_maintp = MaintP(parent_mo, maintenance_group,
                             runMode=get_value(args, 'run_mode', DEFAULT_RUN_MODE))
    if is_valid_key(args, 'scheduler'):
        maint_rspolscheduler = RsPolScheduler(maint_maintp, tnTrigSchedPName=args['scheduler'])


class CreateMaintenanceGroup(CreateMo):

    def __init__(self):
        self.description = 'Create Maintenance Group. This is a set of nodes to which a maintenance policy may be applied. The maintenance policy determines the pre-defined action to take when there is a disruptive change made to the service profile associated with the node group. '
        self.maintenance_group = None
        super(CreateMaintenanceGroup, self).__init__()

    def set_cli_mode(self):
        super(CreateMaintenanceGroup, self).set_cli_mode()
        self.parser_cli.add_argument('maintenance_group', help='The name for a set of nodes that a maintenance policy can be applied to. The maintenance policy determines the pre-defined action to take when there is a disruptive change made to the service profile associated with the node group.')
        self.parser_cli.add_argument('-r', '--run_mode', default= DEFAULT_RUN_MODE, choices=RUN_MODE_CHOICES, help='Specifies whether to proceed automatically to next set of nodes once a set of nodes have gone through maintenance successfully.')
        self.parser_cli.add_argument('-s', '--scheduler', help='Maintenance schedule specification. Specifies a schedule for maintenance policy. ')
        self.parser_cli.add_argument('-g', '--group_node_ids', nargs='+', help='The node block. This is a range of nodes. Each node block begins with the first port and ends with the last port.')

    def read_key_args(self):
        self.maintenance_group = self.args.pop('maintenance_group')

    def wizard_mode_input_args(self):
        self.args['maintenance_group'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/fabric/maintgrp-', self.maintenance_group, MaintGrp, description='Maintenance Group')
        super(CreateMaintenanceGroup, self).delete_mo()
        self.commit_change()
        self.check_if_mo_exist('uni/fabric/maintpol-', self.maintenance_group, MaintP,)
        super(CreateMaintenanceGroup, self).delete_mo()

    def main_function(self):
        # Query to parent
        self.look_up_mo('uni/fabric', '')
        create_maintenance_group(self.mo, self.maintenance_group, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateMaintenanceGroup()


