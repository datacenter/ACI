from cobra.model.fv import Ap
from createMo import *

DEFAULT_QOS = 'unspecified'

QOS_CHOICES = ['level1', 'level2', 'level3', 'unspecified']


def input_optional_args(*key):
    args = {}
    args['prio'], = input_options('Prio(QoS Class)', DEFAULT_QOS, QOS_CHOICES),
    return args


def create_application(fv_tenant, application, **args):
    """Create a Application. The application profile is a set of requirements that an application instance has on the virtualizable fabric. The policy regulates connectivity and visibility among endpoints within the scope of the policy. """
    args = args['optional_args'] if 'optional_args' in args.keys() else args

    fv_ap = Ap(fv_tenant, application,
               prio=get_value(args, 'prio', DEFAULT_QOS).lower())
    return fv_ap

class CreateApplication(CreateMo):

    def __init__(self):
        self.description = 'Create a Application. The application profile is a set of requirements that an application instance has on the virtualizable fabric. The policy regulates connectivity and visibility among endpoints within the scope of the policy. '
        self.tenant_required = True
        super(CreateApplication, self).__init__()

    def set_cli_mode(self):
        super(CreateApplication, self).set_cli_mode()
        self.parser_cli.add_argument('application', help='Application Name')
        self.parser_cli.add_argument('-Q', '--QoS_class', dest='prio', default= DEFAULT_QOS, choices=QOS_CHOICES, help='The priority level of a sub application running behind an endpoint group.')

    def read_key_args(self):
        self.application = self.args['application']

    def wizard_mode_input_args(self):
        self.args['application'] = self.input_application_name()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/ap-', self.application, Ap, description='Application')
        super(CreateApplication, self).delete_mo()

    def main_function(self):
        # Query a tenant
        fv_tenant = self.check_if_tenant_exist()
        create_application(fv_tenant, self.application, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateApplication()