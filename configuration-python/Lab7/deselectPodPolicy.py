import sys
from selectPodPolicy import RsPodPGrp

from utility import *


def deselect_pod_selector(modir):
    # Query to Pod Selector
    bgp_rspodpgrp = modir.lookupByDn('uni/fabric/podprof-default/pods-default-typ-ALL/rspodPGrp')
    if isinstance(bgp_rspodpgrp, RsPodPGrp):
        bgp_rspodpgrp.delete()
    else:
        print 'No BGP policy group has been selected.'
        return

    print_query_xml(bgp_rspodpgrp)
    commit_change(modir, bgp_rspodpgrp)

if __name__ == '__main__':

    # Obtain the key parameters.
    try:
        host_name, user_name, password= sys.argv[1:4]
    except ValueError:
        host_name, user_name, password = input_login_info()

    # Login to APIC
    modir = apic_login(host_name, user_name, password)

    # Execute the main function
    deselect_pod_selector(modir)

    modir.logout()


