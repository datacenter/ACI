# APIC Rest Python Adapter (arya)

Original Author: Paul Lesiak - [palesiak@cisco.com](palesiak@cisco.com)  
Co-author: Mike Timm - [mtimm@cisco.com](mtimm@cisco.com)
Solution Validation Services contact: Tim Garner - [tigarner@cisco.com](tigarner@cisco.com)


# Description

arya is a tool that will convert APIC object documents from their XML or JSON
form into the equivalent Python code leveraging the Cobra SDK.

arya supports  input in a number of formats, including XML, JSON, a directory containing
multiple xml or json documents, as well as standard input. The standard input
option is very useful for use as a filter in most text editors, where one
can copy the JSON or XML extracted from APIC Visore or API inspector, and quickly
generate the Python source code framework, which can then be modified, tokenized
and rapidly turned into functional prototypes.

Note that arya is a very useful tool for the heavy lifting of converting object
model into source code, however it does not validate configuration, perform
advanced lookup logic or implement a number of best practices that should be
followed, such as performing lookups to validate targets, referencing object
attributes instead of hardcoding Dns and names, and other proper coding practices

It is strongly recommended that for advanced use cases, getting expert advice
and validating your code, you reach out to Cisco Advanced Services for support.
For more information, visit http://www.cisco.com/go/aci

If you run into issues with arya, please open an issue on github


# Installation

## Environment
Required

* Python 2.7+

Recommended:

* Git

## Downloading
Option A:

If you have git installed clone the repository

    git clone https://github.com/datacenter/ACI.git

Option B:

If you don't have git [download a zip copy of the repository](https://github.com/datacenter/ACI/archive/master.zip) and extract.  

## Installing
Change directory to the cloned/extracted repo

    cd ACI/arya

Run the setup script

    python setup.py install

Check that arya can be run from the command line

    $ arya.py


# Usage

Once installed arya will place the file `arya.py` in your path, so you should be able to call `arya.py` from any prompt.

Usage is as such:

    $ arya.py

    usage: Code generator for APIC cobra SDK [-h] [-f FILE] [-s] [-d SOURCEDIR]
                                             [-t TARGETDIR] [-i IP] [-p PASSWORD]

    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  Document containing post to be sent to REST API
      -s, --stdin           Parse input from stdin, for use as a filter, e.g., cat
                            doc.xml | arya.py -s
      -d SOURCEDIR, --sourcedir SOURCEDIR
                            Specify a source directory containing ACI object files
                            you want to convert to python.
      -t TARGETDIR, --targetdir TARGETDIR
                            Where to write the .py files that come from the -d
                            directory. If none is specified, it will default to
                            SOURCEDIR
      -i IP, --ip IP        IP address of APIC
      -p PASSWORD, --password PASSWORD
                            Password for admin account on APIC


# License

Copyright (C) 2014 Cisco Systems Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
