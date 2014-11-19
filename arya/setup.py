import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


with open('LICENSE') as f:
    license = f.read()

exec(open('arya/version.py').read())

setup(
    name='arya',
    version=__version__,
    description='APIC Rest to pYthon Adapter',
    long_description=open('README.md').read(),
    packages=['arya'],
    url='https://github.com/datacenter/ACI/arya',
    license=license,
    author='Paul Lesiak',
    author_email='palesiak@cisco.com',
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
    scripts=['arya/arya.py', 'arya/getconfigfromapic.py',
             'arya/apicxmljson.py'],
    entry_points={
        "console_scripts": [
            "arya=arya:main",
            "getconfigfromapic=getconfigfromapic:main",
            "apicxmljson=apicxmljson:main",
        ],
    },
    tests_require = ['pytest'],
    cmdclass = {'test': PyTest},
)
