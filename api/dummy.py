#!/usr/bin/env python

import json

obj = {"spot-1": ("127.0.0.1", 0),
       "spot-2": ("127.0.0.1", 0),
       "spot-3": ("127.0.0.1", 0),
       "spot-4": ("127.0.0.1", 0)}

with open("addrs.json", "w") as f:
    json.dump(obj, f)
