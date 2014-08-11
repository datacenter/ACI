import pytest
import sys
import os


def pytest_addoption(parser):
    filedir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    parser.addoption('--apic', nargs=4, action='append',
                     metavar=('url', 'user', 'passwd', 'secure'),
                     help='The URL to the APIC or switch, username, ' +
                     'password, secure (True/False)')
    parser.addoption(
        '--sourcedir', action='store', metavar='sourcedir',
        default='{0}'.format(os.path.join(filedir, 'tests', 'samples')))
    parser.addoption(
        '--targetdir', action='store', metavar='targetdir',
        default='{0}'.format(os.path.join(filedir, 'tests', 'testout')))


def pytest_runtest_setup(item):
    if 'needapic' in item.keywords and not item.config.getoption(
            'apic', default=None):
        pytest.skip('Test needs APIC target to test against')
