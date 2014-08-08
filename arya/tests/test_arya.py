#!/usr/bin/env python
import os
import pytest
import sys
import logging
import inspect
import pkgutil
import httplib
import subprocess

import cobra.model
import cobra.mit.access
import cobra.mit.session
import cobra.mit.request

from cobra.internal.codec.xmlcodec import toXMLStr
from cobra.internal.codec.jsoncodec import toJSONStr

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../bin')
import arya

needapic = pytest.mark.needapic

httplib.HTTPConnection.debuglevel = 1
logging.basicConfig(level=logging.DEBUG)


@needapic
@pytest.fixture(params=pytest.config.getvalue('apic'))
def moDir(request):
    url, user, password, secure = request.param
    secure = False if secure == 'False' else True
    session = cobra.mit.session.LoginSession(url, user, password,
                                             secure=secure)
    md = cobra.mit.access.MoDirectory(session)
    md.login()
    return md


def lookupSubtreeByDn(md, dn, propFilter=None):
    dnq = cobra.mit.request.DnQuery(dn)
    dnq.subtree = 'full'
    dnq.propInclude = 'config-only'
    if propFilter:
        dnq.propFilter = propFilter
    try:
        return md.query(dnq)[0]
    except:
        return None


class Namespace(object):

    def __init__(self, sourcedir=None, targetdir=None, ip=None, password=None,
                 nocommit=None, filein=None, stdin=False):
        super(Namespace, self).__init__()
        self.sourcedir = sourcedir
        self.targetdir = targetdir
        self.ip = ip
        self.password = password
        self.nocommit = nocommit
        self.filein = filein
        self.stdin = stdin

    def __repr__(self):
        return 'Namespace(sourcedir={0}, targetdir={1}, ip={2}, password={3}, '\
            + 'nocommit={4}, file={5}, stdin={6}'.format(self.sourcedir,
                                                         self.targetdir,
                                                         self.ip, self.password,
                                                         self.nocommit,
                                                         self.filein,
                                                         self.stdin)


def pytest_generate_tests(metafunc):

    if 'apic' in metafunc.fixturenames:
        if metafunc.config.getvalue('apic') != []:
            apics = [x for x in metafunc.config.getvalue('apic')]
            metafunc.parametrize('apic', apics)

    if 'testfiles' in metafunc.fixturenames:
        sourcedir = os.path.realpath(metafunc.config.getvalue('sourcedir'))
        targetdir = os.path.realpath(metafunc.config.getvalue('targetdir'))
        files = []
        os.chdir(sourcedir)
        for fil in os.listdir('.'):
            fil = os.path.abspath(fil)
            if fil.lower().endswith('.xml') or fil.lower().endswith('.json'):
                outfilename = os.path.abspath(
                    os.path.join(targetdir, os.path.basename(fil).split('.')[-2] + '.py'))
                files.append((fil, outfilename))
        metafunc.parametrize('testfiles', files)

    if 'sourcedir' in metafunc.fixturenames:
        sourcedir = os.path.realpath(pytest.config.getvalue('sourcedir'))
        metafunc.parametrize('sourcedir', [sourcedir])

    if 'targetdir' in metafunc.fixturenames:
        targetdir = os.path.realpath(pytest.config.getvalue('targetdir'))
        metafunc.parametrize('targetdir', [targetdir])

    if 'dn' in metafunc.fixturenames:
        metafunc.parametrize(
            'dn', ['uni/tn-mgmt', 'uni/controller/nodeidentpol'])

    if 'codec' in metafunc.fixturenames:
        metafunc.parametrize('codec', ['xml', 'json'])


@pytest.mark.arya_unit_func_test
class Test_arya:

    @needapic
    def test_generate_from_apic(self, moDir, dn, codec):
        mo = lookupSubtreeByDn(moDir, dn)
        assert mo
        if codec == 'xml':
            instr = toXMLStr(mo, includeAllProps=True)
            print instr
            pycode = arya.arya().getpython(xmlstr=instr)
        elif codec == 'json':
            instr = toJSONStr(mo, includeAllProps=True)
            print instr
            pycode = arya.arya().getpython(jsonstr=instr)

        assert pycode

    def test_generate_by_files(self, testfiles):
        apic = pytest.config.getoption('apic')
        if not apic:
            apic = [['http://mock', 'admin', 'password', False]]
        apic = apic[0]
        url, user, password, secure = apic
        url = str(url).split('//')[1]
        args = Namespace(
            filein=testfiles[0], ip=url, password=password, nocommit=True)
        assert arya.runfromcli(args)

    def test_clean_output(self, targetdir):
        os.chdir(targetdir)

        for f in os.listdir(targetdir):
            if f.endswith(".py"):
                os.remove(f)

    def test_generate_from_samples_directory(self, sourcedir, targetdir):
        apic = pytest.config.getoption('apic')
        if not apic:
            apic = [['http://mock', 'admin', 'password', False]]
        apic = apic[0]
        url, user, password, secure = apic
        url = str(url).split('//')[1]
        args = Namespace(sourcedir=sourcedir,
                         targetdir=targetdir,
                         ip=url, password=password, nocommit=True)
        assert arya.runfromcli(args)

    @needapic
    def test_execute_cobra_scripts(self, testfiles):
        cobrafile = testfiles[1]
        subprocess.check_call(['python', cobrafile])
