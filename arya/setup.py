try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

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
    scripts=['bin/arya.py', 'bin/getconfigfromapic.py'],
)

