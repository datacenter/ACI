import sys
import re
from __builtin__ import str # A warning in my python editor suggests me to put this in
import yaml
import argparse
import getpass
import random
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Tenant
from cobra.internal.codec.xmlcodec import toXMLStr
import os
from IPython import embed


def null_function():
    pass


def is_valid(*arg, **kwargs):
    ban_list = ['undefined', 'unspecified', None, '']
    if 'ban' in kwargs.keys() and kwargs['ban'] is not None:
        if type(kwargs['ban']) == list:
            ban_list.extend(kwargs['ban'])
        else:
            ban_list.append(kwargs['ban'])
    for i in arg:
        if i in ban_list:
            return False
    return True


def is_valid_key(args, key, ban=None):
    return True if key in args.keys() and is_valid(args[key], ban=ban) else False


def return_valid_optional_args(args):
    if type(args) is dict and 'optional_args' in args.keys():
        return args['optional_args']
    else:
        return {}

def input_raw_input(prompt='', default='', lower=False, required=False):
    adjust_prompt = prompt + ' (required)' if required else prompt + ''
    adjust_prompt += '(default: "' + default + '"): ' if default != '' and default is not None else ': '
    r_input = raw_input(adjust_prompt).strip()
    if r_input == '':
        if required:
            return input_raw_input(prompt, lower=lower, required=required)
        else:
            return default
    return r_input.lower() if lower else r_input


def input_options(prompt, default, options, num_accept=False, required=False):
    try:
        opt_string = '/'.join(options)
    except NameError:
        opt_string = ''
    adjust_prompt = prompt + '(required)' if required else prompt
    if not required and default != '':
        adjust_prompt += '(default: "' + default + '")'
    opt_string = '[' + opt_string + ']' if not opt_string == '' else ''
    r_input = input_raw_input(adjust_prompt + opt_string)
    if r_input == '':
        if required:
            return input_options(prompt, default, options, num_accept=num_accept, required=required)
        else:
            return default

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
    return input_options(prompt, default, options, num_accept=num_accept, required=required)


def input_yes_no(prompt='', required=False, default=''):
    adjust_prompt = prompt + '(default: "' + default + '")' if not required and default != '' else prompt
    r_input = raw_input(adjust_prompt+' [yes(y)/no(n)]?: ')
    if r_input == '' and default != '':
        r_input = default
    if required and r_input == '':
        return input_yes_no(prompt=prompt, required=required)
    if r_input.lower() in ['yes', 'y', 'true']:
        return True
    elif r_input.lower() in ['no', 'n', 'false'] or r_input == '':
        return False
    else:
        print 'Inappropriate input.'
        return input_yes_no(prompt=prompt, required=required)


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
    return args[key] if type(args) is dict and key in args.keys() and args[key] != '' and args[key] is not None else default_value


def print_query_xml(xml_file, pretty_print=True):
    print toXMLStr(xml_file, prettyPrint=pretty_print)


# add a list the the same type MOs.
def add_mos(msg, key_function, opt_args_function=None, do_first=False, once=False):
    mos = []
    add_one_mo = True if do_first else input_yes_no(prompt=msg, required=True)
    msg = msg.replace(' a ', ' another ')
    msg = msg.replace(' an ', ' another ')
    while add_one_mo:
        new_mo = {}
        new_mo['key_args'] = key_function()
        if opt_args_function is not None:
            new_mo['opt_args'] = opt_args_function(new_mo['key_args'])
        mos.append(new_mo)
        if once:
            add_one_mo = False
        else:
            add_one_mo = input_yes_no(prompt=msg, required=True)
    return mos[0] if once else mos


def read_add_mos_args(add_mos_result, get_opt_args=False):
    key_args = []
    opt_args = []
    for i in add_mos_result:
        key_args.append(i['key_args'])
        if get_opt_args:
            opt_args.append(i['opt_args'])
    if get_opt_args:
        return key_args, opt_args
    else:
        return key_args


class CreateMo(object):
    """
    Create a mo
    """

    def __init__(self):
        self.description = self.description if hasattr(self, 'description') else ''
        self.tenant_required = self.tenant_required if hasattr(self, 'tenant_required') else False
        self.args = None
        self.delete = False
        self.host = '172.31.216.100' if os.uname()[1] == 'BONHUAN-M-D891' else None
        self.user = 'admin' if os.uname()[1] == 'BONHUAN-M-D891' else None
        self.password = 'ins3965!' if os.uname()[1] == 'BONHUAN-M-D891' else None
        self.tenant = self.tenant if hasattr(self, 'tenant') and os.uname()[1] == 'BONHUAN-M-D891' else 'bon'  # for testing myself
        # self.tenant = self.tenant if hasattr(self, 'tenant') else 'None'    # the proper way
        self.application = None
        self.modir = None
        self.mo = None
        self.config_mode = 'wizard'
        self.optional_args = {}
        self.set_argparse()
        if list({'-h', '--help'} & set(sys.argv)):
            sys.exit()
        self.set_mode()
        self.__getattribute__('run_'+self.config_mode+'_mode')()
        self.create_or_delete()
        self.commit_change()

    def set_argparse(self):
        parser = argparse.ArgumentParser(description=self.description)
        parser.add_argument('-d', '--delete', help='Flag to run a delete function.',  action='store_const', const=self.set_delete, default=null_function)
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
        args.delete()
        self.args = vars(args)

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
        self.config_mode = sys.argv[2].lower() if self.delete else sys.argv[1]
        print 'Config in', self.config_mode, 'Mode.'

    def run_cli_mode(self):
        self.set_host_user_password()
        self.read_key_args()
        self.read_opt_args()
        self.apic_login()

    def run_yaml_mode(self):
        f = open(self.args['yaml_file'], 'r')
        self.args = yaml.load(f)
        f.close()
        self.set_host_user_password()
        self.read_key_args()
        self.read_opt_args()
        self.apic_login()

    def run_wizard_mode(self):
        if os.uname()[1] != 'BONHUAN-M-D891':
            self.args = {
                'host': input_raw_input("Host Name", required=True),
                'user': input_raw_input("User Name", required=True),
                'password': getpass.getpass("Password (required): ")
            }
            if self.tenant_required:
                self.args['tenant'] = input_raw_input("Tenant Name", required=True)
            self.set_host_user_password()
        self.apic_login()
        self.wizard_mode_input_args()
        self.read_key_args()
        self.read_opt_args()

    def set_host_user_password(self):
        self.host = self.args['host']
        self.user = self.args['user']
        self.password = self.args['password']
        if self.tenant_required:
            self.tenant = self.args['tenant']

    def apic_login(self):
        """Login to APIC"""
        lsess = LoginSession('https://' + self.host, self.user, self.password)
        modir = MoDirectory(lsess)
        modir.login()
        self.modir = modir

    def input_tenant_name(self, msg='\nPlease specify Tenant info:'):
        print msg
        self.tenant = input_raw_input("Tenant Name", required=True)

    def look_up_mo(self, path, mo_name, set_mo=True):
        temp_mo = self.modir.lookupByDn(path + mo_name)
        if set_mo:
            self.mo = temp_mo
        return temp_mo

    def check_if_tenant_exist(self, return_boolean=False, set_mo=True):
        fv_tenant = self.look_up_mo('uni/tn-', self.tenant, set_mo=set_mo)
        if not isinstance(fv_tenant, Tenant):
            print 'Tenant', self.tenant, 'does not existed. \nPlease create a tenant.'
            return False if return_boolean else sys.exit()
        return fv_tenant

    def check_if_mo_exist(self, path, mo_name='', module=None, description='', detail_description='', set_mo=True, return_false=False):
        temp_mo = self.look_up_mo(path, mo_name, set_mo=set_mo)
        if module is not None and not isinstance(temp_mo, module):
            if detail_description != '':
                print detail_description
            else:
                print description, mo_name, 'does not existed.'
            if return_false:
                return False
            else:
                print 'The programing is exiting.'
                sys.exit()
        if set_mo:
            self.mo = temp_mo
        return temp_mo

    def set_delete(self):
        self.delete = True

    def delete_mo(self):
        self.mo.delete()

    def input_application_name(self, msg='\nPlease specify Application info:'):
        print msg
        self.application = input_raw_input("Application Name", required=True)
        return self.application

    def commit_change(self, changed_object=None, print_xml=True, pretty_print=True):
        """Commit the changes to APIC"""
        changed_object = self.mo if changed_object is None else changed_object
        if print_xml:
            print_query_xml(changed_object, pretty_print=pretty_print)
        config_req = ConfigRequest()
        config_req.addMo(changed_object)
        self.modir.commit(config_req)

    def create_or_delete(self):
        if self.delete:
            self.delete_mo()
        else:
            self.main_function()

    def wizard_mode_input_args(self):
        pass
    
    def read_key_args(self):
        pass

    def read_opt_args(self):
        self.optional_args = self.args['optional_args'] if 'optional_args' in self.args.keys() else self.args

    def main_function(self):
        pass


if __name__ == '__main__':
    mo = CreateMo()
