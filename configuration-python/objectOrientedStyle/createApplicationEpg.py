from cobra.model.fv import Ap, AEPg, RsBd, RsCustQosPol, RsAEPgMonPol, RsDomAtt, RsNodeAtt, RsPathAtt
from createMo import *

DEFAULT_QOS = 'unspecified'
DEFAULT_BRIDGE_DOMAIN = 'None'
DEFAULT_CUSTOM_QOS = 'None'
DEFAULT_POLICY = 'None'
DEFAULT_IMMEDIACY = 'lazy'
DEFAULT_MODE = 'regular'

IMMEDIACY_CHOICES = ['immediate', 'lazy']
QOS_CHOICES = ['level1', 'level2', 'level3', 'unspecified']
MODE_CHOICES = ['regular', 'native', 'untagged']


def input_key_args(msg='\nPlease input Application EPG info:'):
    print msg
    return input_raw_input("EPG Name", required=True)


def input_domain_profile(msg='\nAssociating Domain Profile (VMs or bare metals):'):
    print msg
    return input_raw_input("domain_profile", required=True)


def input_domain_profile_optional_args(*args):
    args = {}
    args['deployment_immediacy'] = input_options('Deploy Immediacy', DEFAULT_IMMEDIACY, IMMEDIACY_CHOICES)
    args['resolution_immediacy'] = input_options('Resolution Immediacy', DEFAULT_IMMEDIACY, IMMEDIACY_CHOICES)
    return args


def input_leaf(msg='\nplease specify static links leaves'):
    print msg
    args = {'node_id': input_raw_input('Node ID', default='None')}
    if is_valid_key(args, 'node_id', ban=['None']):
        args['encap'] = input_raw_input('Encap', required=True)
        args['deployment_immediacy'] = input_options('Deploy Immediacy', DEFAULT_IMMEDIACY, IMMEDIACY_CHOICES)
        args['mode'] = input_options('Mode', DEFAULT_MODE, MODE_CHOICES)
    return args


def input_path(msg='\nplease specify static links paths'):
    print msg
    args = {'node_id': input_raw_input('Node ID', default='None'),
            'eth': input_raw_input('Eth number', default='None')}
    if is_valid_key(args, 'node_id', ban=['None']) and is_valid_key(args, 'eth', ban=['None']):
        args['encap'] = input_raw_input('Encap', required=True)
        args['deployment_immediacy'] = input_options('Deploy Immediacy', DEFAULT_IMMEDIACY, IMMEDIACY_CHOICES)
        args['mode'] = input_options('Mode', DEFAULT_MODE, MODE_CHOICES)
    return args


def input_optional_args(*key):
    args = {'bridge_domain': input_raw_input('Bridge Domain', default=DEFAULT_BRIDGE_DOMAIN),
            'prio': input_options('Prio(QoS Class)', DEFAULT_QOS, QOS_CHOICES),
            'custom_qos': input_raw_input('Custom QoS', default= DEFAULT_CUSTOM_QOS),
            'monitoring': input_raw_input("Monitoring Policy", default=DEFAULT_POLICY),
            'associated_domain_profile': read_add_mos_args(add_mos('Add an Associated Domain Profile', input_domain_profile, input_domain_profile_optional_args), get_opt_args=True),
            'statically_link': input_yes_no('Apply Statically Link with Leaves/Paths', default='False')
            }
    if args['statically_link']:
        args['leaf'] = input_leaf()
        args['path'] = input_path()
    return args


def create_application_epg(fv_ap, epg, **args):
    """Create a Application. A set of requirements for the application-level EPG instance. The policy regulates connectivity and visibility among the end points within the scope of the policy. """
    args = args['optional_args'] if 'optional_args' in args.keys() else args
    fv_aepg = AEPg(fv_ap, epg,
                   prio=get_value(args, 'prio', 'unspecified').lower())

    # Provide bridge_domain to the EPG.
    if is_valid_key(args, 'bridge_domain'):
        fv_rsbd = RsBd(fv_aepg, tnFvBDName=args['bridge_domain'])

    if is_valid_key(args, 'custom_qos'):
        fv_rscustqospol = RsCustQosPol(fv_aepg, tnQosCustomPolName=args['custom_qos'])

    if is_valid_key(args, 'monitoring'):
        fv_rsaepgmonpol = RsAEPgMonPol(fv_aepg, tnMonEPGPolName=args['monitoring'])

    if is_valid_key(args, 'associated_domain_profile'):
        for profile in args['associated_domain_profile']:
            fv_rsdomatt = RsDomAtt(fv_aepg, 'uni/phys-' + profile['domain_profile'],
                           instrImedcy=get_value(profile, 'deployment_immediacy', DEFAULT_IMMEDIACY),
                           resImedcy=get_value(profile, 'resolution_immediacy', DEFAULT_IMMEDIACY))

    if is_valid_key(args, 'statically_link') and args['statically_link']:
        if is_valid_key(args, 'leaf') and is_valid_key(args['leaf'], 'node_id', ban=['None']):
            fv_rsnodeatt = RsNodeAtt(fv_aepg, 'topology/pod-1/node-' + str(args['leaf']['node_id']),
                                     encap=args['leaf']['encap'],
                                     mode=get_value(args['leaf'], 'mode', DEFAULT_MODE),
                                     instrImedcy=get_value(args['leaf'], 'deployment_immediacy', DEFAULT_IMMEDIACY))

        if is_valid_key(args, 'path') and is_valid_key(args['path'], 'node_id', ban=['None']):
            fv_rsnodeatt = RsPathAtt(fv_aepg, 'topology/pod-1/paths-' + str(args['path']['node_id']) + '/pathep-[eth' + args['path']['eth'] + ']',
                                     encap=args['path']['encap'],
                                     mode=get_value(args['path'], 'mode', DEFAULT_MODE),
                                     instrImedcy=get_value(args['path'], 'deployment_immediacy', DEFAULT_IMMEDIACY))

    return fv_aepg

class CreateApplicationEpg(CreateMo):

    def __init__(self):
        self.description = 'Create a Application EPG. A set of requirements for the application-level EPG instance. The policy regulates connectivity and visibility among the end points within the scope of the policy. '
        self.tenant_required = True
        self.tenant = 'mgmt'
        self.epg = None
        super(CreateApplicationEpg, self).__init__()

    def set_cli_mode(self):
        super(CreateApplicationEpg, self).set_cli_mode()
        self.parser_cli.add_argument('application', help='Application Name')
        self.parser_cli.add_argument('epg', help='Application EPG Name')
        self.parser_cli.add_argument('-Q', '--QoS_class', dest='prio', default= DEFAULT_QOS, choices=QOS_CHOICES, help='The priority level of a sub application running behind an endpoint group.')
        self.parser_cli.add_argument('-q', '--custom_qos', help='A relation to a custom QoS policy that enables different levels of service to be assigned to network traffic, including specifications for the Differentiated Services Code Point (DSCP) value(s) and the 802.1p Dot1p priority. This is an internal object.')
        self.parser_cli.add_argument('-b', '--bridge_domain', help='A relation to the bridge domain associated to this endpoint group.')
        self.parser_cli.add_argument('-m', '--monitoring', default= DEFAULT_POLICY, help='The monitoring policy name.')
        self.parser_cli.add_argument('-s', '--statically_link', action='store_const', const=True, default=False, help='Statically link with Leaves/Paths')
        self.parser_cli.add_argument('-l', '--leaf', nargs=4, help='The static association with an access group, which is a bundled or unbundled group of ports. Arguments are: Node ID, Encap, Deployment Immediacy and Mode.')
        self.parser_cli.add_argument('-p', '--path', nargs=5, help='A static association with a path. Arguments are: Node ID, eth number, Encap, Deployment Immediacy and Mode.')

    def read_key_args(self):
        self.application = self.args['application']
        self.epg = self.args['epg']

    def wizard_mode_input_args(self):
        self.args['application'] = self.input_application_name()
        self.args['epg'] = input_key_args()
        if not self.delete:
            self.args['optional_args'] = input_optional_args()
            if is_valid_key(self.args['optional_args'], 'associated_domain_profile'):
                associated_domain_profile = []
                for i in range(len(self.args['optional_args']['associated_domain_profile'][0])):
                    associated_domain_profile.append(dict({'domain_profile': self.args['optional_args']['associated_domain_profile'][0][i]}.items() + self.args['optional_args']['associated_domain_profile'][1][i].items()))
                self.args['optional_args']['associated_domain_profile'] = associated_domain_profile

    def run_cli_mode(self):
        super(CreateApplicationEpg, self).run_cli_mode()
        if not self.delete:
            if is_valid_key(self.optional_args, 'leaf'):
                self.optional_args['leaf'] = {'node_id': self.optional_args['leaf'][0],
                                              'encap': self.optional_args['leaf'][1],
                                              'deployment_immediacy': self.optional_args['leaf'][2],
                                              'mode': self.optional_args['leaf'][3]}
            if is_valid_key(self.optional_args, 'path'):
                self.optional_args['path'] = {'node_id': self.optional_args['path'][0],
                                              'eth': self.optional_args['path'][1],
                                              'encap': self.optional_args['path'][2],
                                              'deployment_immediacy': self.optional_args['path'][3],
                                              'mode': self.optional_args['path'][4]}

    def delete_mo(self):
        self.check_if_mo_exist('uni/tn-' + self.tenant + '/ap-' + self.application + '/epg-', self.epg, AEPg, description='Application EPG')
        super(CreateApplicationEpg, self).delete_mo()

    def main_function(self):
        # Query a Tenant
        self.check_if_tenant_exist()
        fv_ap = self.check_if_mo_exist('uni/tn-' + self.tenant + '/ap-', self.application, Ap, description='Application')
        create_application_epg(fv_ap, self.epg, optional_args=self.optional_args)

if __name__ == '__main__':
    mo = CreateApplicationEpg()
