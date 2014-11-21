#!/usr/bin/env python

from argparse import ArgumentParser
import httplib
import logging

from arya import arya

try:
    import cobra.mit.access
    import cobra.mit.session
    import cobra.mit.request
    from cobra.internal.codec.xmlcodec import toXMLStr
except ImportError:
    print("*"*60)
    print("This requires the ACI Python SDK")
    print ("*"*60)
    print
    raise


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
    parser.add_argument('-e', '--endpoint', help='Use old EndPoint object',
                        default=False)
    parser.add_argument('-p', '--port', help='APIC Port', default=80)
    parser.add_argument('-u', '--user', help='APIC Username', default='admin')
    parser.add_argument(
        '-s', '--secure', help='Verify certificate', default=False)
    parser.add_argument(
        '-pw', '--password', help='APIC Password', required=True)
    parser.add_argument('-d', '--dn', help='DN to query', required=True)
    parser.add_argument(
        '-v', '--verbose', help='Enable debugging', default=False)
    args = parser.parse_args()

    if args.verbose:
        httplib.HTTPConnection.debuglevel = 1
        logging.basicConfig(level=logging.DEBUG)

    if args.endpoint:
        ep = cobra.mit.access.EndPoint(
            args.apic, secure=False if args.port == 80 else True, port=args.port)
        ls = cobra.mit.session.LoginSession(args.user, args.password)
        md = cobra.mit.access.MoDirectory(ep, ls)
    else:
        if args.apic.startswith(('http://', 'https://')):
            if args.apic.endswith('/'):
                args.apic = args.apic[:-1]
            args.apic = str(args.apic) + ":" + str(args.port) + "/"
            ls = cobra.mit.session.LoginSession(
                args.apic, args.user, args.password, secure=args.secure)
            md = cobra.mit.access.MoDirectory(ls)
    md.login()

    mo = lookupSubtreeByDn(md, args.dn)
    if mo:
        xmlstr = toXMLStr(mo, includeAllProps=True, prettyPrint=True)
        print arya().getpython(xmlstr=xmlstr, apicip=args.apic, apicuser=args.user, apicpassword=args.password)
    else:
        print 'Nothing found for DN {0}'.format(args.dn)

if __name__ == '__main__':
    main()
