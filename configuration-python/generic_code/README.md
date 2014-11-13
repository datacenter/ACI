configuration-python
====================

All the codes are in object oriented style.

Each of them does a small configuration on APIC -- to create a MO. For example, createTenant.py would create a tenant.

Programmer can simply write their customized script by inheriting the class createMo in “createMo.py”.  


#Scripts descriptions:

createMo.py: the basic class/module. It also contains useful functions that help programmers for writing their customized scripts.

The others are generic scripts. Each of them does a small configuration. For example, createContract.py would create a contract.

#Usage:

All the codes support three different input methods: wizard, yaml and cli.

1. wizard: configure a mo by following a wizard. Usage: 
<br>python createFilter.py wizard
<br>To get the help info: python createFilter.py wizard –h

2. yaml: configure a mo with a config file (yaml format). Usage:
<br>python createFilter.py yaml createFilter.yaml
<br>To get the help info: python createFilter.py yaml –h

3. cli: configure a mo based on you python arguments.  It contains key arguments and optional arguments. Flags are used in order to call the optional arguments. Usage:
<br>python createFilter.py cli \<ip-address\> \<user-name\> \<password\> \<tenant\> \<filter\> [–e ip –i tcp] 
<br>To get the help info: python createFilter.py cli –h

#Delete a mo:

Using -d flag. Example if you want to delete a filter, you can call createFilter.py with a -d flag. The delete method is supported in all three input methods. For example:

<br>python createFilter -d yaml
<br>python createFilter -d wizard
<br>python createFilter -d cli \<ip-address\> \<user-name\> \<password\> \<tenant\> \<filter\>

