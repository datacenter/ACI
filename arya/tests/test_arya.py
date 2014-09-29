#!/usr/bin/env python
import os
import pytest
import sys
import logging
import inspect
import pkgutil
import httplib
import subprocess
from argparse import Namespace

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


def pytest_generate_tests(metafunc):

    derefpath = lambda path: os.path.realpath(
        os.path.expanduser(os.path.expandvars(path)))

    if 'apic' in metafunc.fixturenames:
        if metafunc.config.getvalue('apic') != []:
            apics = [x for x in metafunc.config.getvalue('apic')]
            metafunc.parametrize('apic', apics)

    if 'testfiles' in metafunc.fixturenames:

        sourcedir = derefpath(metafunc.config.getvalue('sourcedir'))
        targetdir = derefpath(metafunc.config.getvalue('targetdir'))
        files = []
        os.chdir(sourcedir)
        for fil in os.listdir('.'):
            fil = os.path.abspath(fil)
            if fil.lower().endswith('.xml') or fil.lower().endswith('.json'):
                outfilename = os.path.abspath(
                    os.path.join(targetdir,
                                 os.path.basename(fil).split('.')[-2] + '.py'))
                files.append((fil, outfilename))
        metafunc.parametrize('testfiles', files)

    if 'sourcedir' in metafunc.fixturenames:
        sourcedir = derefpath(pytest.config.getvalue('sourcedir'))
        metafunc.parametrize('sourcedir', [sourcedir])

    if 'targetdir' in metafunc.fixturenames:
        targetdir = derefpath(pytest.config.getvalue('targetdir'))
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
            stdin=None, filein=testfiles[0], ip=url, password=password,
            nocommit=True)
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
        args = Namespace(sourcedir=sourcedir, filein=None, stdin=None,
                         targetdir=targetdir, ip=url, password=password,
                         nocommit=True)
        assert arya.runfromcli(args)

    @needapic
    def test_execute_cobra_scripts(self, testfiles):
        cobrafile = testfiles[1]
        subprocess.check_call(['python', cobrafile])
