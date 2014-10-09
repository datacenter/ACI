configuration-python
====================

Instead of doing ACI setup in the GUI window, now we can do the configuration in CLI by calling these python codes.


#What are those codes:
generic_code: scripts in folder are generic scripts. Each of them does a small function, creating a particular MO.

lab: scripts in this folder are implement scripts. They are implements codes that utilize the generic scripts in the "generic_code" folder and make a big configuration in APIC. (About the installation and usage of the generic code please see the README under folder generic_code.)

template.py: it is not a valid script. But it is a good template for a programmer to start from if he wants to write a customized script. All he needs to do is to redefine the functions in template.py. 


#Reference:  
APIC Management Information Model Reference (http://mishield-bld.insieme.local/documentation/html/index.html)

Nexus 9000 ACI Boot Camp Lab Guide (version 1.19)

APIC Python Lab (by Manish Tandon)
