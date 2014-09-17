from cobra.model.fv import Ap, AEPg, RsBd
from createMo import *

DEFAULT_QOS = 'unspecified'
DEFAULT_BRIDGE_DOMAIN = None

QOS_CHOICES = ['level1', 'level2', 'level3', 'unspecified']


def input_key_args(msg='\nPlease input Application EPG info:'):
    print msg
    return input_raw_input("EPG Name", required=True)


def input_optional_args():
    args = {}
    args['bridge_domain'] = input_raw_input('Bridge Domain (default: None)')
    args['prio'], = input_options('Prio(QoS Class)', DEFAULT_QOS, QOS_CHOICES),
    return args


def create_application(fv_ap, epg, **args):
    """Create a Application"""
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    fv_aepg = AEPg(fv_ap, epg,
                   prio=get_value(args, 'prio', 'unspecified').lower())

    # Provide bridge_domain to the EPG.
    if 'bridge_domain' in args.keys():
        fv_rsbd = RsBd(fv_aepg, tnFvBDName=args['bridge_domain'])


class CreateApplicationEpg(CreateMo):

    def __init__(self):
        self.description = 'Create a Application EPG'
        self.tenant_required = True
        self.epg = None
        super(CreateApplicationEpg, self).__init__()

    def set_cli_mode(self):
        super(CreateApplicationEpg, self).set_cli_mode()
        self.parser_cli.add_argument('application', help='Application Name')
        self.parser_cli.add_argument('epg', help='Application EPG Name')
        self.parser_cli.add_argument('-Q', '--QoS_class', dest='prio', default= DEFAULT_QOS, choices=QOS_CHOICES, help='The priority level of a sub application running behind an endpoint group.')
        self.parser_cli.add_argument('-b', '--bridge_domain', help='A relation to the bridge domain associated to this endpoint group.')

    def read_key_args(self):
        self.application = self.args['application']
        self.epg = self.args['epg']

    def wizard_mode_input_args(self):
        self.args['application'] = self.input_application_name()
        self.args['epg'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/ap-' + self.application + '/epg-', self.epg, AEPg, description='Application EPG')
        super(CreateApplicationEpg, self).delete_mo()

    def main_function(self):
        # Query a Tenant
        fv_ap = self.check_if_mo_exist('uni/tn-' + self.tenant + '/ap-', self.application, Ap, description='Application')
        create_application(fv_ap, self.epg, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateApplicationEpg()
