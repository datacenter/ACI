from cobra.mit.access import EndPoint, MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest

from cobra.internal.codec.xmlcodec import toXMLStr


def apic_login(hostname, username, password):
    """Login to APIC"""
    epoint = EndPoint(hostname, secure=False, port=80)
    lsess = LoginSession(username, password)
    modir = MoDirectory(epoint, lsess)
    modir.login()
    return modir


def get_raw_input(prompt='', lower=False):
    r_input = raw_input(prompt).strip()
    return r_input.lower() if lower else r_input


def get_optional_input(prompt, options, num_accept=False):
    try:
        opt_string = '/'.join(options)
    except NameError:
        opt_string = ''
    opt_string = '[' + opt_string + ']: '
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


def input_login_info(msg='\nInappropriate input arguments. Please fill in the arguments step by step.'):
    print msg
    print 'Login info:'
    return [get_raw_input("Host Name (required): "), get_raw_input("User Name (required): "),
            get_raw_input("Password (required): ")]


def input_tenant_name():
    print '\nPlease input Tenant info:'
    return get_raw_input("Tenant Name (required): ")


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
