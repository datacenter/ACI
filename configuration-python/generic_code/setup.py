from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "apicPython",
    version = "0.1.3",
    scripts = ['README.md'
               ],

    # The project's main homepage
    url='https://github.com/datacenter/ACI/tree/master/configuration-python',

    packages = ['apicPython'],
    py_modules = ['apicPython'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    # install_requires = ['docutils>=0.3'],

    dependency_links = ['http://as-codehub-ci.cisco.com/palesiak/cobra-built-egg-repository/blob/master/acicobra-1.0.1_0e-py2.7.egg'],

    # metadata for upload to PyPI
    author = "Bon Huang",
    author_email = "bangyellow@hotmail.com",
    description = "This are codes for creating MO in APIC through CLI",
    long_description = read('README.md'),
    license = "Cisco",
    keywords = "Create MO in Cisco APIC",

    # could also include long_description, download_url, classifiers, etc.
)