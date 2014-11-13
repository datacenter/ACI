configuration-python
====================

# Description
Instead of doing ACI setup in the GUI window, now we can do the configuration in terminal with the python codes. It provide a more convenient way for users to do APIC configuration without knowing any programming skill.  


# What are those codes:
generic_code: scripts in folder are generic scripts. Each of them does a small function, creating a particular MO.

lab: scripts in this folder are implement scripts. They are implements codes that utilize the generic scripts in the "generic_code" folder and make a big configuration in APIC. (About the installation and usage of the generic code please see the README under folder generic_code.)

template.py: it is not a valid script. But it is a good template for a programmer to start from if he wants to write a customized script. All he needs to do is to redefine the functions in template.py. 

# Installation

## Environment

Required

* Python 2.7+
* [Cisco APIC Python SDK] (http://software.cisco.com/download/release.html?i=!y&mdfid=285968390&softwareid=286278832&release=1.0%281k%29&os)
To install APIC Python SDK, please follow this link: https://developer.cisco.com/media/apicDcPythonAPI_v0.1/install.html#

## Downloading 

Option A:
Install the scripts to your python library form using pip install
    
    pip install apicPython
    

Option B:

If you have git installed, clone the repository

    git clone https://github.com/datacenter/ACI.git
    cd ACI/configuration-python/generic_code/
    python setup.py install

Option C:

If you don't have git, [download a zip copy of the repository](https://github.com/datacenter/ACI/archive/master.zip) and extract.
Then,

    cd ACI/configuration-python/generic_code/
    python setup.py install
    
# License

Copyright 2014 Cisco Systems, Inc.

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
APIC Management Information Model Reference (http://mishield-bld.insieme.local/documentation/html/index.html)

Nexus 9000 ACI Boot Camp Lab Guide (version 1.19)
