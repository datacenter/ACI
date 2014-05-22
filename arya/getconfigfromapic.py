#!/usr/bin/env python

import cobra.mit.access
import cobra.mit.session
import cobra.mit.request
from argparse import ArgumentParser
from cobra.internal.codec.xmlcodec import toXMLStr
from arya import arya

def lookupSubtreeByDn(md, dn, propFilter=None):
    dnq = cobra.mit.request.DnQuery(dn)
    dnq.subtree = 'full'
    dnq.propInclude = 'config-only'
    if propFilter:
        dnq.propFilter = propFilter
    try:
        return md.query(dnq)[0]
    except:
        return None


def main():
    parser = ArgumentParser('Generate cobra SDK code from APIC')
    parser.add_argument('-a', '--apic', help='Target APIC', required=True)
    parser.add_argument('-p', '--port', help='APIC Port', default=80)
    parser.add_argument('-u', '--user', help='APIC Username', default='admin')
    parser.add_argument('-pw', '--password', help='APIC Password', required=True)
    parser.add_argument('-d', '--dn', help='DN to query', required=True)
    args = parser.parse_args()

    ep = cobra.mit.access.EndPoint(args.apic, secure=False if args.port == 80 else True, port=args.port)
    ls = cobra.mit.session.LoginSession(args.user, args.password)
    md = cobra.mit.access.MoDirectory(ep, ls)
    md.login()

    mo = lookupSubtreeByDn(md, args.dn)
    if mo:
        xmlstr = toXMLStr(mo)
        print arya().getpython(xmlstr=xmlstr, apicip=args.apic, apicuser=args.user, apicpassword=args.password)
    else:
        print 'Nothing found for DN {0}'.format(args.dn)

if __name__ == '__main__':
    main()
