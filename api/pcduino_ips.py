#!/usr/bin/env python

import web
import json
import time
import re

urls = (
        "/", "ip_api",
)

app = web.application(urls, globals())


TEMPLATE = """
<html>
<head>
<title>PCDuino IP Adresses!</title>
</head>
<body>
<pre>%s</pre>
</body>
</html>
"""

class ip_api:
    def GET(self):
        with open("addrs.json", "r") as f:
            obj = json.load(f)

        out = "host\t\tip\t\t\tlast seen\n\n"

        for spot in ["spot-1", "spot-2", "spot-3", "spot-4"]:
            if spot in obj:
                ip, t = obj[spot]
            else:
                ip, t = "unreported", "never"

            out += "%s\t\t%s\t\t%s\n" % (spot, ip, t)
        return out

    def POST(self):
        data = web.input()
        host = data.host
        ip = data.ip
        t = time.strftime("%Y/%m/%d %H:%M:%S MST", time.localtime())

        if not re.match(r"spot\-[1-4]", host):
            raise web.notfound()

        if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
            raise web.notfound()

        with open("addrs.json", "r") as f:
            obj = json.load(f)

        obj[host] = (ip, t)

        with open("addrs.json", "w") as f:
            json.dump(obj, f)

if __name__ == "__main__":
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()