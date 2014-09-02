from createVcenterController import create_vcenter_controller
from createVcenterCredential import create_vcenter_credential
from createVlanPool import create_vlan_pool
from createVmmDomain import create_vmm_domain
from addVmmDomainAssociation import add_vmm_domain_association

from utility import *


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Integrate application EPG with VMware.')
    parser.add_argument('yaml', help='Imported yaml file.')
    args = vars(parser.parse_args())

    try:
        data = read_config_yaml_file(args['yaml'], login_info=False)
    except IOError:
        print 'No such file or directory:', args['yaml']
        sys.exit()
    else:
        host, user, password = get_login_info(data)
        tenant = data['tenant']
        application = data['application']
        vlan = tenant + '_' + data['vlan_pool']['name']
        vlan_mode = data['vlan_pool']['mode']
        vm_provider = data['vm_provider']
        vmm_domain = data['vmm_domain']

    modir = apic_login(host, user, password)

    # Create a VLAN_Pool
    create_vlan_pool(modir, vlan, vlan_mode, str(data['vlan_pool']['from']),
                     str(data['vlan_pool']['to']))

    # Create VMM domain
    create_vmm_domain(modir, vm_provider, vmm_domain, vlan=vlan,
                      vlan_mode=vlan_mode)

    # Set up VMM Credential
    if type(data['vcenter_credential']) == list:
        for credential in data['vcenter_credential']:
            create_vcenter_credential(modir, vm_provider, vmm_domain,
                                      credential['profile'],
                                      credential['user'],
                                      credential['password'])
    else:
        create_vcenter_credential(modir, vm_provider, vmm_domain,
                                  data['vcenter_credential']['profile'],
                                  data['vcenter_credential']['user'],
                                  data['vcenter_credential']['password'])

    # Set up VMM Controller
    create_vcenter_controller(modir, vm_provider, vmm_domain,
                              data['vcenter_controller']['profile'],
                              data['vcenter_controller']['host_or_ip'],
                              data['vcenter_controller']['data_center'],
                              associated_credential=data['vcenter_controller'][
                                  'associated_credential'])

    # Associating EPG to vCenter Domain.
    for epg in data['associated_epg']:
        add_vmm_domain_association(modir, tenant, application, epg['name'],
                                   vmm_domain,
                                   deployment_immediacy=epg['dep_immediacy'],
                                   resolution_immediacy=epg['res_immediacy'])
    modir.logout()