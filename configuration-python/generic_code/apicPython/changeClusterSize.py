from cobra.model.infra import ClusterPol

from createMo import *


def input_key_args(msg='\nPlease Specify Cluster Size:'):
    print msg
    return input_raw_input("Cluster Size", required=True)


def change_cluster_size(parent_mo, size):
    # set cluster size
    module = ClusterPol(parent_mo, size=size)


class ChangeClusterSize(CreateMo):

    def __init__(self):
        self.description = 'Change Cluster Size. The targeted size of the cluster, which is used to set the size of the cluster. '
        self.size = None
        super(ChangeClusterSize, self).__init__()

    def set_argparse(self):
        parser = argparse.ArgumentParser(description=self.description)
        self.subparsers = parser.add_subparsers(help='sub-command help')
        self.parser_yaml = self.subparsers.add_parser(
            'yaml', help='Config with a yaml file.'
        )
        self.parser_cli = self.subparsers.add_parser(
            'cli', help='Config base on the input arguments from Comment line.'
        )
        self.parser_wizard = self.subparsers.add_parser(
            'wizard', help='Config following a wizard.'
        )

        self.set_cli_mode()
        self.set_yaml_mode()
        self.set_wizard_mode()

        args = parser.parse_args()
        self.args = vars(args)

    def set_cli_mode(self):
        super(ChangeClusterSize, self).set_cli_mode()
        self.parser_cli.add_argument('size', help='The size of the cluster.')

    def read_key_args(self):
        self.size = self.args.pop('size')

    def wizard_mode_input_args(self):
        self.args['size'] = input_key_args()

    def main_function(self):
        # Query a parent
        self.look_up_mo('uni/controller', '')
        change_cluster_size(self.mo, self.size)


if __name__ == '__main__':
    mo = ChangeClusterSize()


