#!/usr/bin/env python
# Copyright 2016 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Example 7: Using the Adapter interface.
"""

import sys
import yaml
import requests.packages.urllib3
import time
import pprint

import zhmcclient

requests.packages.urllib3.disable_warnings()

if len(sys.argv) != 2:
    print("Usage: %s hmccreds.yaml" % sys.argv[0])
    sys.exit(2)
hmccreds_file = sys.argv[1]

with open(hmccreds_file, 'r') as fp:
    hmccreds = yaml.load(fp)

examples = hmccreds.get("examples", None)
if examples is None:
    print("examples not found in credentials file %s" % \
          (hmccreds_file))
    sys.exit(1)

example7 = examples.get("example7", None)
if example7 is None:
    print("example7 not found in credentials file %s" % \
          (hmccreds_file))
    sys.exit(1)

loglevel = example7.get("loglevel", None)
if loglevel is not None:
    level = getattr(logging, loglevel.upper(), None)
    if level is None:
        print("Invalid value for loglevel in credentials file %s: %s" % \
              (hmccreds_file, loglevel))
        sys.exit(1)
    logging.basicConfig(level=level)

hmc = example7["hmc"]

cred = hmccreds.get(hmc, None)
if cred is None:
    print("Credentials for HMC %s not found in credentials file %s" % \
          (hmc, hmccreds_file))
    sys.exit(1)

userid = cred['userid']
password = cred['password']

print(__doc__)

try:
    print("Using HMC %s with userid %s ..." % (hmc, userid))
    session = zhmcclient.Session(hmc, userid, password)
    cl = zhmcclient.Client(session)

    timestats = example7.get("timestats", None)
    if timestats:
        session.time_stats_keeper.enable()

    print("Listing CPCs ...")
    cpcs = cl.cpcs.list()
    for cpc in cpcs:
        print(cpc)
        print("\tListing Adapters for %s ..." % cpc.properties['name'])
        adapters = cpc.adapters.list()
        for i, adapter in enumerate(adapters):
            print('\t' + str(adapter))

    print("Logging off ...")
    session.logoff()

    if timestats:
        print(session.time_stats_keeper)

    print("Done.")

except zhmcclient.Error as exc:
    print("%s: %s" % (exc.__class__.__name__, exc))
    sys.exit(1)
