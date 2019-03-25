#!/usr/bin/env python

import argparse as ap
import rabbit

class Repository:
    def __init__(self,silent=False):
        self.silent = silent
        self.tmp = "tmp"
        self.messenger = Messenger()
        self.messenger.consume()

if __name__ == '__main__':
    parser = ap.ArgumentParser(description="Launch the repository module for Assignemnt 2")

    parser.add_argument('--silent',action='store_true',dest='silent',help="Disable checkopoint output, enabled by default",default=True,required=False)

    args = parser.parse_args()
    repo = Repository(silent=args.silent)
