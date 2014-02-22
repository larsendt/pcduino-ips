#!/bin/bash

spawn-fcgi -d ../api -f ../api/pcduino_ips.py -a 127.0.0.1 -p 55057
