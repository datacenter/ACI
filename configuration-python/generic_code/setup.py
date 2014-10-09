from setuptools import setup
import os

setup(
    name = "configuration-python",
    version = "0.0.1",
    scripts = ['addFabricNode.py',
               'addMgmtProvidedOutOfBandContract.py',
               'addPrivateL3Network.py',
               'addSecurityDomain.py',
               'addUserDomain.py',
               'addVmmDomainAssociation.py',
               'associateL3OutsideNetworkToBD.py',
               'chooseRoleForUser.py',
               'configureInBandEpgDefault.py',
               'configureInterfacePcAndVpc.py',
               'connectEpgContract.py',
               'createAccessPortPolicyGroup.py',
               'createApplication.py',
               'createApplicationEpg.py',
               'createAttachableAccessEntityprofile.py',
               'createBgpRouteReflector.py',
               'createBridgeDomainSubnet.py',
               'createContract.py',
               'createExternalManagementEntityInstance.py',
               'createExternalNetwork.py',
               'createFilter.py',
               'createInterfaceProfile.py',
               'createL3EpgProviderOrConsumerContract.py',
               'createLocalUser.py',
               'createMo.py',
               'createMulticastAddressBlock.py',
               'createNodeManagementAddress.py',
               'createNodes.py',
               'createNodesAndInterfacesProfile.py',
               'createOutOfBandContract.py',
               'createPhysicalDomain.py',
               'createPodPolicyGroup.py',
               'createRadiusProvider.py',
               'createRoutedInterfaceProfile.py',
               'createRoutedOutside.py',
               'createStaticRoute.py',
               'createSubnet.py',
               'createTenant.py',
               'createVcenterController.py',
               'createVcenterCredential.py',
               'createVcenterDomain.py',
               'createVlanPool.py',
               'createVshieldController.py',
               'createVxlanPool.py',
               'selectPodPolicy.py',
               'setAutonomousSystemNumber.py',
               'setDefaultSettingForPrivateNetwork.py'
               ],

    package_data={
        '': ['*.yaml'],
    },

    # The project's main homepage
    url='https://github.com/datacenter/ACI/tree/master/configuration-python',

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    # install_requires = ['docutils>=0.3'],

    dependency_links = ['http://as-codehub-ci.cisco.com/palesiak/cobra-built-egg-repository/blob/master/acicobra-1.0.1_0e-py2.7.egg'],

    # metadata for upload to PyPI
    author = "Bon Huang",
    author_email = "bonhuan@cisco.com",
    description = "This are codes for creating MO in APIC through CLI",
    long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    license = "Cisco",
    keywords = "Create MO in Cisco APIC",

    # could also include long_description, download_url, classifiers, etc.
)