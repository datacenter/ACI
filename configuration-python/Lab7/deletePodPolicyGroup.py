import sys
from createPodPolicyGroup import input_key_args, PodPGrp
from utility import *


def delete_pod_policy_group(modir, policy_name):

    # Query to the Route Reflector Node.
    fabric_podpgrp = modir.lookupByDn('uni/fabric/funcprof/podpgrp-' + policy_name)

    if isinstance(fabric_podpgrp, PodPGrp):
        fabric_podpgrp.delete()
    else:
        print 'Pod group policy', policy_name, 'is not existed.'
        return

    print toXMLStr(fabric_podpgrp, prettyPrint=True)
    commit_change(modir, fabric_podpgrp)

if __name__ == '__main__':

    # Obtain the key parameters.
    try:
        host_name, user_name, password, policy_name = sys.argv[1:5]
    except ValueError:
        host_name, user_name, password = input_login_info()
        policy_name = input_key_args()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    delete_pod_policy_group(modir, policy_name)

    modir.logout()


