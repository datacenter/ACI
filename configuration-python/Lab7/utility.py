import sys
from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Tenant

from cobra.internal.codec.xmlcodec import toXMLStr
import pdb

def apic_login(hostname, username, password):
    """Login to APIC"""
    epoint = EndPoint(hostname, secure=False, port=80)
    lsess = LoginSession(username, password)
    modir = MoDirectory(epoint, lsess)
    modir.login()
    return modir


def check_if_tenant_exist(modir, tenant_name):
    fv_tenant = modir.lookupByDn('uni/tn-' + tenant_name)
    if not isinstance(fv_tenant, Tenant):
        print 'Tenant', tenant_name, 'does not existed. \nPlease create a tenant.'
        sys.exit()
    return fv_tenant


def get_raw_input(prompt='', lower=False, required=False):
    r_input = raw_input(prompt).strip()
    if required and r_input == '':
        get_raw_input(prompt, lower=lower, required=required)
    return r_input.lower() if lower else r_input


def get_optional_input(prompt, options, num_accept=False):
    try:
        opt_string = '/'.join(options)
    except NameError:
        opt_string = ''
    opt_string = '[' + opt_string + ']: ' if not opt_string == '' else ': '
    r_input = get_raw_input(prompt + opt_string)
    if r_input == '':
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
    get_optional_input(prompt, options)


def get_yes_no(prompt='', required=False):
    r_input = raw_input(prompt)
    if required and r_input == '':
        get_yes_no(prompt=prompt, required=required)
    if r_input.lower() in ['yes', 'y', 'true']:
        return True
    elif r_input.lower() in ['no', 'n', 'false'] or r_input == '':
        return False
    else:
        print 'Inappropriate input.'
        get_yes_no(prompt=prompt, required=required)


def input_login_info(msg='\nInappropriate input arguments. Please fill in the arguments step by step.'):
    print msg
    print 'Login info:'
    return [get_raw_input("Host Name (required): ", required=True),
            get_raw_input("User Name (required): ", required=True),
            get_raw_input("Password (required): ", required=True)]


def input_tenant_name(msg='\nPlease input Tenant info:'):
    print msg
    return get_raw_input("Tenant Name (required): ", required=True)


def commit_change(modir, changed_object):
    """Commit the changes to APIC"""
    config_req = ConfigRequest()
    config_req.addMo(changed_object)
    modir.commit(config_req)


def get_value(args, key, default_value):
    """Return the value of an argument. If no such an argument, return a default value"""
    return args[key] if key in args.keys() and args[key] != '' else default_value


def print_query_xml(xml_file, pretty_print=True):
    print toXMLStr(xml_file, prettyPrint=pretty_print)


def adding_a_mo(msg):
    r_input = raw_input('\n' + msg+' (y/n)? : ')
    if r_input == '':
        adding_a_mo(msg)
    return r_input.lower() in ['yes', 'y']


# add a list the the same type MOs that only have key arguments
def add_mos(function, msg):
    mos = []
    add_one_mo = adding_a_mo(msg)
    msg = msg.replace(' a ', ' another ')
    while add_one_mo:
        mos.append(function())
        add_one_mo = adding_a_mo(msg)
    return mos


# add a list the the same type MOs that with optional arguments
def add_mos_with_options(key_function, optional_function, msg):
    mos = []
    # pdb.set_trace()
    add_one_mo = adding_a_mo(msg)
    msg = msg.replace(' a ', ' another ')
    while add_one_mo:
        new_mo = []
        new_mo.append(key_function())
        new_mo.append(optional_function(new_mo[0]))
        mos.append(new_mo)
        add_one_mo = adding_a_mo(msg)
    return mos