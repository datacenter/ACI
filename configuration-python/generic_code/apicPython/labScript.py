from createMo import *


class LabScript(CreateMo):

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
        pass

    def run_yaml_mode(self):
        super(LabScript, self).run_yaml_mode()
        if self.tenant_required:
            self.tenant = self.args['tenant']

    def run_cli_mode(self):
        print 'CLI mode is not supported in this method. Please try Yaml mode.'
        sys.exit()

    def read_opt_args(self):
        pass


if __name__ == '__main__':
    mo = LabScript()