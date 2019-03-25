#!/usr/bin/env python

import argparse as ap

class Capture:
    def __init__(self,sip='localhost', hashtag="", silent=False):
        self.silent = silent
        self.sip = "".join(sip)
        self.ht = hashtag

if __name__ == '__main__':
    parser = ap.ArgumentParser(description="Launch the capture module for Assignemnt 2")

    parser.add_argument('--silent',action='store_true',dest='silent',help="Disable checkopoint output, enabled by default",default=True,required=False)
    parser.add_argument('-s',action='store',dest='IP',type=str,nargs='+',help="IP of repository",default='localhost',required=False)
    parser.add_argument('-t',action='store',dest='ht',type=str,nargs='+',help="Hashtag",default='#ECE4564T83',required=False)

    args = parser.parse_args()
    capture = Capture(sip=args.IP,hashtag=args.ht, silent=args.silent)
