__author__ = 'ddastoli'

# connects to APIC and returns VLAN pool(s) where user-specified VLAN is found

import cobra.mit.access
import cobra.mit.session
import cobra.mit.request
import cobra.model.fvns
import cobra.mit.naming
import re

# log into an APIC and create a directory object
ip = "10.48.59.238"
username = "ddastoli"
password = "ins3965!"
vlan = 100
url = "https://" + ip

def apicLogin(ip, username, password):
    # log into an APIC and create a directory object
    url = "https://" + ip
    print('Logging into APIC ...')
    ls = cobra.mit.session.LoginSession(url, username, password, secure=False, timeout=180)
    moDir = cobra.mit.access.MoDirectory(ls)
    try:
        moDir.login()
    except:
        print("Login error (wrong username or password?)")
        exit(1)
    return moDir

def findVlan(vlanId, vlanPools, moDir):
    vlanBitMap = {}
    listOfPools = []
    for pool in vlanPools:
        #print pool.name + ' is ' + pool.allocMode
        VlanInstPChildren = moDir.lookupByClass(pool.children, pool.dn)
        vlanFromToList = []
        # per the object model, children are fvnsEncapBlk, RtVlanNs and VlanInstP
        for child in VlanInstPChildren:
            if 'EncapBlk' in child.dn.meta.moClassName:
                # extract VLANs in each EncapBlk
                # one of the naming props is called "from" which is a reserved keyword, use __dict__ workaround instead
                vlanFromTo = 'from {} to {}'.format(str(child.__dict__['from']), str(child.to))
                # print '\t --> ' + vlanFromTo
                p = re.compile('\d+')
                vlanList = p.findall(vlanFromTo)
                # expand VLAN ranges
                vlanRange = range(int(vlanList[0]),int(vlanList[1])+1)
                for vlan in vlanRange:
                    try:
                        vlanBitMap[vlan]
                    except KeyError:
                        vlanBitMap[vlan] = str(child.parentDn)
                    else:
                        vlanBitMap[vlan] += (" *and* " + str(child.parentDn))

    return vlanBitMap


def findDomain(vlanPoolsWhereVLANisPresent, VLAN, moDir):
    # in here find the Domains (phys, VMM, L2 and L3) where the VLAN pool is present
    listOfDomains = []
    try:
        vlanPools = vlanPoolsWhereVLANisPresent[VLAN].split(" *and* ")
    except KeyError:
        exit('No Vlans found corresping to the search')

    physDoms = moDir.lookupByClass('physDomP')
    l2Doms = moDir.lookupByClass('l2extDomP')
    l3Doms = moDir.lookupByClass('l3extDomP')
    VMMDoms = moDir.lookupByClass('vmmDomP')

    domsToProcess = [physDoms, l2Doms, l3Doms, VMMDoms]

    for doms in domsToProcess:
        for dom in doms:
            print "\t\t --> found {} domain".format(dom.dn)
            dn = str(dom.dn) + '/rsvlanNs'
            rsVlanNs = moDir.lookupByDn(dn)
            try:
                for vlanPool in vlanPools:
                    if str(vlanPool) == str(rsVlanNs.tDn):
                        listOfDomains.append(dom)
                        print "\tadded " + vlanPool + " to the list of Domains"
            except AttributeError:
                print "\t\t{} is not bound to any AEP!".format(dn)


    print '\n'
    print "found the following list of Domains where VLAN is present: "
    for domain in listOfDomains:
        print domain.dn
    print '\n'

    return listOfDomains

def findAEP(DomainsWhereVLANis, moDir):
    # in here find the AEP where the Domain pool is present

    listOfAEP = []

    AEPs = moDir.lookupByClass('infraAttEntityP')
    for AEP in AEPs:
        print " --> found {} AEP".format(AEP.dn)
        for domain in DomainsWhereVLANis:
            #print domain.dn
            dn = str(AEP.dn) + '/rsdomP-['+str(domain.dn)+']'
            #print dn
            rsDomP = moDir.lookupByDn(dn)
            #print "comparing " + str(domain.dn)+ " with " + str(rsDomP.tDn)
            try:
                if domain.dn == rsDomP.tDn:
                    if AEP not in listOfAEP:
                        listOfAEP.append(AEP)
            except AttributeError:
                print "\t\t{} is not bound to any AEP!".format(dn)


        print '\n'
        print "found the following list of AEP where the searched Domain is present: "
        for foundAEP in listOfAEP:
            print foundAEP.dn
        print '\n'

    return listOfAEP

def findAccPortGrp(AEPs, moDir):
    # in here we find what is the policy groups

    listPolicyGrp = []

    print "\nLooking for Interface Policy Groups ..."
    ifpolgrp = moDir.lookupByClass('infraAccPortGrp')
    print " --> found {} Interface Policy Groups".format(len(ifpolgrp))
    for policy in ifpolgrp:
        dn = str(policy.dn) + '/rsattEntP'
        # child of infraAccPortGrp 'infraRsAttEntP' points to AEP
        rsattenp = moDir.lookupByDn(dn)
        for AEP in AEPs:
            print AEP.dn
        try:
            if rsattenp.tDn == AEP.dn:
                print "\t\t{} is bound to {}".format(dn,str(rsattenp.tDn))
                listPolicyGrp.append(policy)
        except AttributeError:
            print "\t\t{} is not bound to any AEP!".format(dn)


    return listPolicyGrp

def findPorts(AccPortGrp,moDir):

     # finding the relationship between the policy group mapping the AEP and the interface selector
    listHPortS = []

    hPortS = moDir.lookupByClass('infraHPortS')
    for hPort in hPortS:
        #print hPort.dn
        dn = str(hPort.dn) + '/rsaccBaseGrp'
        #print dn
        rsacc = moDir.lookupByDn(dn)
        #print "comparing " + str(domain.dn)+ " with " + str(rsDomP.tDn)
        for elem in AccPortGrp:
            if rsacc.tDn == elem.dn:
                if hPort not in listHPortS:
                    print 'adding '+str(hPort.dn)
                    listHPortS.append(hPort)


    print "\nLooking for Interface Profiles ..."
    ifsel = moDir.lookupByClass('infraAccPortP')
    print " --> found {} Interface Profiles".format(len(ifsel))

    print "\nLooking for Leafs ..."
    leafs = moDir.lookupByClass('infraLeafS')
    print " --> found {} Leafs".format(len(leafs))

    print "\nLooking for Node Blocks ..."
    nBlocks = moDir.lookupByClass('infraNodeBlk')
    print " --> found {} Node Blocks".format(len(nBlocks))

    print "\nLooking for Nodes ..."
    nodes = moDir.lookupByClass('infraNodeP')
    print " --> found {} Nodes".format(len(nodes))

    print "\n\tLooking for all port blocks ..."
    portblk = moDir.lookupByClass('infraPortBlk')
    print "\n\tLooking for all h ports ..."


    for node in nodes:
        for elem in ifsel:
            #print elem.dn
            dn = str(node.dn) + '/rsaccPortP-[' + str(elem.dn) + ']'
            rsAccPortP = moDir.lookupByDn(dn)

            for elem2 in listHPortS:
                #print str(elem2.dn)[0:str(elem2.dn).find('/hports')]
                try:
                    if str(elem2.dn)[0:str(elem2.dn).find('/hports')] == rsAccPortP.tDn:
                    #print rsAccPortP.dn
                        for leaf in leafs:
                            #print str(leaf.dn)
                            str_node = str(rsAccPortP.dn)[0:str(rsAccPortP.dn).find('/rsaccPortP')]
                            #print str_node
                            if str_node in str(leaf.dn):
                                for nBlock in nBlocks:
                                    if str(leaf.dn) in str(nBlock.dn):
                                        print "\t\t" + str(leaf.dn) + ' --> ' + nBlock.from_ + ' to ' + nBlock.to_
                                        #print elem2.dn
                                        for block in portblk:
                                            if str(elem2.dn) in str(block.dn):
                                                print "\t\t" + str(elem2.dn) + ' --> ' + block.fromCard + '/' + block.fromPort + ' to ' + block.toCard + '/' + block.toPort
                except AttributeError:
                    print "\t\t{} is not bound to any AEP!".format(dn)

    return


def main(ip, username, password, VLAN):
    moDir = apicLogin(ip, username, password)
    vlanPools = moDir.lookupByClass('fvnsVlanInstP')
    vlanMatch = findVlan(VLAN, vlanPools, moDir)
    #if vlanMatch[VLAN]:
    #    print "VLAN {} found in {}".format(VLAN, vlanMatch[VLAN])
    #else:
    #    print "VLAN {} not found anywhere.".format(VLAN)
    domains = findDomain(vlanMatch,VLAN,moDir)
    AEP = findAEP(domains, moDir)
    AccPortGrp = findAccPortGrp(AEP, moDir)
    Ports = findPorts(AccPortGrp,moDir)


main(ip, username, password, vlan)