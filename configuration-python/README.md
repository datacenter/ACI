configuration-python
====================

Instead of doing ACI setup in the GUI window, now we can do the configuration in CLI by calling these python codes.

All the codes are in object oriented style.
They are functional codes and at the some time they are sample codes. Programmer can simply write their customized script by inheriting the class createMo in “createMo.py”.  


#How to use:

All the codes support three different input methods: wizard, yaml and cli.

1. wizard: configure a mo by following a wizard. Usage: 
<br>python createFilter.py wizard
<br>To get the help info: python createFilter.py wizard –h

2. yaml: configure a mo with a config file (yaml format). Usage:
<br>python createFilter.py yaml createFilter.yaml
<br>To get the help info: python createFilter.py yaml –h

3. cli: configure a mo based on you python arguments.  It contains key arguments and optional arguments. Flags are used in order to call the optional arguments. Usage:
<br>python createFilter.py cli 198.18.133.200 admin C1sco12345 tenantA filterA –e ip –i tcp 
<br>To get the help info: python createFilter.py cli –h


#What are those codes:
createMo.py: the basic class/module. It also contains useful functions that help programmers for writing their customized scripts.

template.py: it is not a valid script. But it is a good template for a programmer to start from if he wants to write a customized script. All he needs to do is to redefine the functions in template.py. 

The other scripts (except for the ones start from “lab”) are functional scripts. Each of them does a small work. For example, createTenant.py only creates an “empty” tenant without any other setup. In order to make a big configuration, we need to apply more than one script. For example: lab2CreateTenant.py, it imports createTenant.py, addSecurityDomain.py, addPrivateL3Network.py  and createBridgeDomain.py to setup a tenant with two security domains, one private layer 3 network and two bridge domains.

Again, scripts begin with “lab”: They are implements codes that utilize the other function (eg: create*.py or add*.py) in order to make a big configuration. All these labs are following the setup in “Nexus 9000 ACI Boot Camp Lab Guide” and “Cisco APIC Getting Started Guide”.


#How to delete a mo:

Using -d flag. Example if you want to delete a filter, you can call createFilter.py with a -d flag. The delete method is supported in all three input methods. For example:

<br>python createFilter -d yaml
<br>python createFilter -d wizard
<br>python createFilter -d cli 198.18.133.200 admin C1sco12345 tenantA filterA


#Reference:  
APIC Management Information Model Reference (http://mishield-bld.insieme.local/documentation/html/index.html)

Nexus 9000 ACI Boot Camp Lab Guide (version 1.19)

APIC Python Lab (by Manish Tandon)
