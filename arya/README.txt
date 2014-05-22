APIC Rest Python Adapter (arya)

Paul Lesiak - palesiak@cisco.com

==================================

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

==================================

arya is a tool that will convert APIC object documents from their XML or JSON
form into the equivalent Python code leveraging the Cobra SDK. arya supports
input in a number of formats, including XML, JSON, a directory containing
multiple xml or json documents, as well as standard input. The standard input
option is very useful for use as a filter in most text editors, where one
can copy the JSON or XML extracted from APIC Visore or API inspector, and quickly
generate the Python source code framework, which can then be modified, tokenized
and rapidly turned into functional prototypes.

Note that arya is a very useful tool for the heavy lifting of converting object
model into source code, however it does not validate configuration, perform
advanced lookup logic or implement a number of best practices that should be
implemented, such as performing lookups to validate targets, referencing object
attributes, instead of hardcoding Dns and names, and other proper coding practices

It is strongly recommended that for advanced use cases, getting expert advice
and validating your code, you reach out to Cisco Advanced Services for support
at as-aci-support@cisco.com