configuration-python
====================

# Description
These scripts allow the APIC configuration to be done in a local terminal
and thus provide a convenient and fast way for users to do APIC configuration.


# Contents

* generic\_code
  - scripts in this folder are generic. Each of them does a small function,
    creating a particular MO.  For the installation and usage of this code
    please see the README in the generic_code folder.
* lab
  - scripts in this folder are implementation scripts. They implement the
    functionality that utilize the code in the **generic_code** folder to make
    configuration changes on the APIC.
* template.py
  - This is not a valid script, rather it is a good template for a programmer
    to start from if they want to write a customized script. All the
    programmer needs to do is to redefine the functions in template.py. 

# Installation

## Environment

Linux system is preferred. 

For windows users, strongly recommend installing [cygwin](https://www.cygwin.com/).

Required

* Python 2.7+
* [Cisco APIC Python SDK] (http://software.cisco.com/download/release.html?i=!y&mdfid=285968390&softwareid=286278832&release=1.0%281k%29&os),
  download the .egg file and follow the link to install acicobra:
  https://developer.cisco.com/media/apicDcPythonAPI_v0.1/install.html#

## Downloading 

* Option A:
  Install the scripts to your python library form using pip install
    
    pip install apicPython

* Option B:

 If you have git installed, clone the repository

    git clone https://github.com/datacenter/ACI.git
    cd ACI/configuration-python/generic_code/
    python setup.py install

* Option C:

  If you don't have git, [download a zip copy of the repository](https://github.com/datacenter/ACI/archive/master.zip) and extract.
  Then,

    cd ACI/configuration-python/generic_code/
    python setup.py install
    
# License

Copyright 2014-2015 Cisco Systems, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

# Reference: 
[APIC Management Information Model Reference](https://developer.cisco.com/site/apic-dc/documents/mim-ref/)

Nexus 9000 ACI Boot Camp Lab Guide (version 1.19) (Yet to be provided but is
available internal to Cisco and easy to find with a CEC search).
