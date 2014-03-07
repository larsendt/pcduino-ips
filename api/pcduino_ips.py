#!/usr/bin/env python

import web
import json
import time
import re
import arrow

urls = (
        "/", "ip_api",
        "/(.+)", "spot_api",
)

app = web.application(urls, globals())


class spot_api:
    def GET(self, spot_name):
        with open("addrs.json", "r") as f:
            obj = json.load(f)
            if spot_name in obj:
                ip, t = obj[spot_name]
                return ip
            else:
                return "none"

class ip_api:
    def GET(self):
        with open("addrs.json", "r") as f:
            obj = json.load(f)

        out = "host\t\tip\t\t\tlast seen (PCDuinos should report once per minute)\n\n"

        for spot in ["spot-1", "spot-2", "spot-3", "spot-4"]:
            if spot in obj:
                ip, t = obj[spot]
                t = arrow.get(t).to("US/Mountain")
                t = t.format("YYYY-MM-DD HH:mm:ss") + " (" + t.humanize() + ")"
            else:
                ip, t = "unreported", "never"

            out += "%s\t\t%s\t\t%s\n" % (spot, ip, t)
        return out

    def POST(self):
        data = web.input()
        host = data.host
        ip = data.ip
        t = arrow.utcnow().timestamp

        if not re.match(r"spot\-[1-4]", host):
            raise web.notfound()

        if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
            raise web.notfound()

        with open("addrs.json", "r") as f:
            obj = json.load(f)

        obj[host] = (ip, t)

        with open("addrs.txt", "w") as f:
            for host, (ip, t) in obj.items():
                f.write("%s %s %s\n" % (host, ip, t))

        with open("addrs.json", "w") as f:
            json.dump(obj, f)

if __name__ == "__main__":
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
