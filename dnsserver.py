# pip install dnslib geoip2 dnspython
from dnslib.server import DNSServer, DNSHandler, BaseResolver
from dnslib import RR
import geoip2.database
import socket
import dns
import dns.resolver

class SimpleResolver(BaseResolver):
    def __init__(self, *args, **kwargs):
        print('init')
        self.reader = geoip2.database.Reader('./GeoLite2-City.mmdb')
        self.cache = {}

    def resolve(self, request, handler):
        qname = request.q.qname
        reply = request.reply()
        # 透過 dnslib 查詢 qname 的 ip
        
        res = dns.resolver.Resolver()
        res.nameservers = ['168.95.1.1']
        # 如果查不到 ip 就回傳找不到網域
        try:
            answers = res.query(str(qname))
        except dns.resolver.NoAnswer:
            if self.cache.get(str(qname)):
                return reply
            self.cache[str(qname)] = True
            print("%s is NoAnswer" % (qname))
            return reply
        except dns.resolver.NXDOMAIN:
            if self.cache.get(str(qname)):
                return reply
            self.cache[str(qname)] = True
            print("%s is NXDOMAIN" % (qname))
            return reply

        for rdata in answers:
            ip = rdata.address
            # 104.16.0.0 - 104.31.255.255 是 cloudflare
            ip_parts = ip.split('.')
            if ip_parts[0] == '104' and int(ip_parts[1]) in range(16, 32):
                if self.cache.get(str(qname)):
                    continue
                self.cache[str(qname)] = True
                print("%s is cloudflare" % (qname))
                continue
            # 透過 geoip 查詢 ip 的地理位置
            try:
                geoip_result = self.reader.city(ip)
            except geoip2.errors.AddressNotFoundError:
                if self.cache.get(str(qname)):
                    return reply
                self.cache[str(qname)] = True
                print("%s(%s) no geoip" % (qname, ip))
                continue
            # 如果結果不是 TW ，就回傳找不到網域
            if geoip_result.country.iso_code != 'TW':
                if self.cache.get(str(qname)):
                    continue
                self.cache[str(qname)] = True
                print("%s is not in TW: %s" % (qname, geoip_result.country.iso_code))
                continue
            
            reply.add_answer(*RR.fromZone("%s 60 A %s" % (qname, ip)))
        
        return reply

class DNSLogger:
    def log(self, handler, request, reply):
        print("DNS query: %s %s" % (request.q.qname, request.q.qtype))
        print("DNS reply: %s" % (reply.a))

    def log_recv(self,handler,data):
        pass
    def log_request(self,handler,data):
        pass
    def log_reply(self,handler,data):
        pass
    def log_send(self,handler,data):
        pass


if __name__ == '__main__':
    # disable logging
    server = DNSServer(SimpleResolver(), port=53, address='0.0.0.0', logger=DNSLogger(), tcp=False)
    print("Starting DNS server...")
    server.start_thread()
    while True:
        pass

