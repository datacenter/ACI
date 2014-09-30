import createVlanPool
import createVmmDomain
import createVcenterCredential
import createVcenterController
import addVmmDomainAssociation

from utility import *

if __name__ == '__main__':

    # Login
    hostname, username, password = input_login_info(msg='')
    try:
        modir = apic_login(hostname, username, password)
        print 'Login succeed.'
    except KeyError:
        print 'Login fail.'
        sys.exit()

    # Wizard starts asking inputs step by step
    tenant_name = input_tenant_name()
    application_name = input_application_name()
    vlan_pool_array = add_mos(createVlanPool.input_key_args, 'Create a Vlan pool')
    vmm_domain_provider, vmm_domain_name = createVmmDomain.input_key_args()
    vmm_domain_options = createVmmDomain.input_optional_args()
    vcenter_credential_array = add_mos(createVcenterCredential.input_key_args, 'Create a vCenter Domain Credential')
    vcenter_controller = createVcenterController.input_key_args()
    vcenter_controller_options = createVcenterController.input_optional_args()
    vmm_domain_association_array = add_mos_with_options(
        addVmmDomainAssociation.input_key_args, addVmmDomainAssociation.input_optional_args, 'Add a VMM Domain Association')

    # Running
    for vlan_pool in vlan_pool_array:
        createVlanPool.create_vlan_pool(modir, vlan_pool[0], vlan_pool[1], vlan_pool[2], vlan_pool[3])
    createVmmDomain.create_vmm_domain(modir, vmm_domain_provider, vmm_domain_name, args_from_CLI=vmm_domain_options)
    for vcenter_credential in vcenter_credential_array:
        createVcenterCredential.create_vcenter_credential(modir, vmm_domain_provider, vmm_domain_name, vcenter_credential[0], vcenter_credential[1], vcenter_credential[2])
    createVcenterController.create_vcenter_controller(modir, vmm_domain_provider, vmm_domain_name, vcenter_controller[0], vcenter_controller[1], vcenter_controller[2], args_from_CLI=vcenter_controller_options)
    for vmm_domain_association in vmm_domain_association_array:
        addVmmDomainAssociation.add_vmm_domain_association(modir, tenant_name, application_name, vmm_domain_association[0][0], vmm_domain_association[0][1], args_from_CLI=vmm_domain_association[1])
    modir.logout()