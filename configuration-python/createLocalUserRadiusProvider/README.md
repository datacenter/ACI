GettingStartedGuide
====================

There are three ways to run the scripts: 

1)	Simply calling: execute the python code directly without any arguments:
eg: python createFilter.py
In this situation, a wizard will show up. Users can finish configuration by following wizard. The wizard tells you what are the key arguments and what are the optional arguments and the default value.

2)	Execute the python code with arguments:
eg: python createFilter.py 172.22.233.207 admin Cisco123 tenant_cisco web_filter
Users can do 
python createFilter.py -h
to get the script information, for example, they key and optional arguments of python code.

3)	Execute the python code with a yaml format config file.
This might be the most convenient way to make configuration especially for making a big configuration. Users can write down a list of configuration in a yaml file format. There are a few sample yaml files in this directory.
