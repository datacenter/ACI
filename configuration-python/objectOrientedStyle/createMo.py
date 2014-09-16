import sys
import re
from __builtin__ import str # A warning in my python editor suggests me to put this in
import yaml
import argparse
import getpass
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Tenant
from cobra.internal.codec.xmlcodec import toXMLStr
from IPython import embed


def input_raw_input(prompt='', lower=False, required=False):
    adjust_prompt = prompt + ' (required): ' if required else prompt + ': '
    r_input = raw_input(adjust_prompt).strip()
    if required and r_input == '':
        return input_raw_input(prompt, lower=lower, required=required)
    return r_input.lower() if lower else r_input


def input_options(prompt, default, options, num_accept=False, required=False):
    try:
        opt_string = '/'.join(options)
    except NameError:
        opt_string = ''
    adjust_prompt = prompt + '(required)' if required else prompt
    adjust_prompt += '(default: "' + default + '"): '
    opt_string = '[' + opt_string + ']' if not opt_string == '' else ''
    r_input = input_raw_input(adjust_prompt + opt_string)
    if r_input == '':
        if required:
            return input_options(prompt, default, options, num_accept=num_accept, required=required)
        else:
            return r_input

    opt = [a for a in options if a.startswith(r_input)]
    if len(opt) > 0:
        opt = opt[0].split('(')
        opt = opt[0]
        return opt
    elif num_accept:
        try:
            return int(r_input)
        except ValueError:
            pass
    print 'Not appropriate argument, please try again.'
    input_options(prompt, default, options, num_accept=num_accept, required=required)


def input_yes_no(prompt='', required=False):
    r_input = raw_input(prompt+' [yes(y)/no(n)]?: ')
    if required and r_input == '':
        return input_yes_no(prompt=prompt, required=required)
    if r_input.lower() in ['yes', 'y', 'true']:
        return True
    elif r_input.lower() in ['no', 'n', 'false'] or r_input == '':
        return False
    else:
        print 'Inappropriate input.'
        input_yes_no(prompt=prompt, required=required)


def input_ports(num):
    card_and_port = str(num)
    card_and_port = re.split('/|-',card_and_port)
    card = card_and_port[0]
    fromPort = card_and_port[1]
    toPort = fromPort if len(card_and_port) <= 2 else card_and_port[2]
    return card, fromPort, toPort


def input_login_info(msg='\nPlease follow the wizard and finish the configuration.'):
    print msg
    print 'Login info:'
    return [input_raw_input("Host Name", required=True),
            input_raw_input("User Name", required=True),
            getpass.getpass("Password (required): ")]


def get_value(args, key, default_value):
    """Return the value of an argument. If no such an argument, return a default value"""
    return args[key] if key in args.keys() and args[key] != '' and args[key] is not None else default_value


def print_query_xml(xml_file, pretty_print=True):
    print toXMLStr(xml_file, prettyPrint=pretty_print)


# add a list the the same type MOs.
def add_mos(msg, key_function, opt_args_function=None, do_first=False):
    mos = []
    add_one_mo = True if do_first else input_yes_no(prompt=msg, required=True)
    msg = msg.replace(' a ', ' another ')
    while add_one_mo:
        new_mo = {}
        new_mo['key_args'] = key_function()
        new_mo['opt_args'] = opt_args_function(new_mo['key_args'])
        mos.append(new_mo)
        add_one_mo = input_yes_no(prompt=msg, required=True)
    return mos


class CreateMo(object):
    """
    Create a mo
    """

    def __init__(self):
        self.description = self.description if hasattr(self, 'description') else ''
        self.tenant_required = self.tenant_required if hasattr(self, 'tenant_required') else False
        self.args = None
        self.host = '172.23.102.91'
        self.user = 'admin'
        self.password = 'ins3965!'
        self.tenant = 'bon'
        self.application = None
        self.modir = None
        self.mo = None
        self.config_mode = 'wizard'
        self.optional_args = None
        self.set_argparse()
        if list({'-h', '--help'} & set(sys.argv)):
            sys.exit()
        self.set_mode()
        self.__getattribute__('run_'+self.config_mode+'_mode')()
        self.apic_login()
        self.main_function()
        self.commit_change()

    def set_argparse(self):
        parser = argparse.ArgumentParser(description=self.description)
        self.subparsers = parser.add_subparsers(help='sub-command help')
        self.parser_yaml = self.subparsers.add_parser(
            'yaml', help='Config with a yaml file.'
        )
        self.parser_cli = self.subparsers.add_parser(
            'cli', help='Config following a wizard.'
        )
        self.parser_wizard = self.subparsers.add_parser(
            'wizard', help='Config following a wizard.'
        )

        self.set_cli_mode()
        self.set_yaml_mode()
        self.set_wizard_mode()

        self.args = vars(parser.parse_args())

    def set_cli_mode(self):
        self.parser_cli.add_argument('host', help='IP address of Host')
        self.parser_cli.add_argument('user', help='Username')
        self.parser_cli.add_argument('password', help='Password')
        if self.tenant_required:
            self.parser_cli.add_argument('tenant', help='Tenant')


    def set_yaml_mode(self):
        self.parser_yaml.add_argument('yaml_file', help='yaml file')

    def set_wizard_mode(self):
        pass  # wizard mode has no input args.

    def set_mode(self):
        self.config_mode = sys.argv[1].lower()
        print 'Config in', self.config_mode, 'Mode.'

    def run_cli_mode(self):
        self.set_host_user_password(self.args)

    def run_yaml_mode(self):
        f = open(self.args['yaml_file'], 'r')
        self.args = yaml.load(f)
        f.close()
        self.set_host_user_password(self.args)

    def run_wizard_mode(self):
        data = {
            'host': input_raw_input("Host Name", required=True),
            'user': input_raw_input("User Name", required=True),
            'password': getpass.getpass("Password (required): ")
        }
        if self.tenant_required:
            data['tenant'] = input_raw_input("Tenant Name", required=True)
        self.set_host_user_password(data)

    def set_host_user_password(self, data):
        self.host = data['host']
        self.user = data['user']
        self.password = data['password']
        if self.tenant_required:
            self.tenant = data['tenant']

    def apic_login(self):
        """Login to APIC"""
        lsess = LoginSession('https://' + self.host, self.user, self.password)
        modir = MoDirectory(lsess)
        modir.login()
        self.modir = modir

    def input_tenant_name(self, msg='\nPlease specify Tenant info:'):
        print msg
        self.tenant = input_raw_input("Tenant Name", required=True)

    def look_up_mo(self, path, mo_name):
        self.mo = self.modir.lookupByDn(path + mo_name)
        return self.mo

    def check_if_tenant_exist(self):
        fv_tenant = self.look_up_mo('uni/tn-', self.tenant)
        if not isinstance(fv_tenant, Tenant):
            print 'Tenant', self.tenant, 'does not existed. \nPlease create a tenant.'
            sys.exit()
        return fv_tenant

    def check_if_mo_exist(self, mo_name, path, module, description=''):
        self.mo = self.look_up_mo(path, mo_name)
        if not isinstance(mo, module):
            print description, mo_name, 'does not existed.'
            sys.exit()
        return self.mo

    def delete_mo(self):
        self.mo.delete()

    def input_application_name(self, msg='\nPlease specify Application info:'):
        print msg
        self.application = input_raw_input("Application Name", required=True)

    def commit_change(self, changed_object=None, print_xml=True, pretty_print=True):
        """Commit the changes to APIC"""
        changed_object = self.mo if changed_object is None else changed_object
        if print_xml:
            print_query_xml(changed_object, pretty_print=pretty_print)
        config_req = ConfigRequest()
        config_req.addMo(changed_object)
        self.modir.commit(config_req)

    def main_function(self):
        self.__getattribute__(re.split('/|.py', sys.argv[0])[-2])()


if __name__ == '__main__':
    mo = CreateMo()
