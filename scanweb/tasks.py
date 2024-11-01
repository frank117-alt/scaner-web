# tasks.py
from celery import shared_task
import nmap
import dns.resolver

@shared_task
def perform_scan(host):
    nm = nmap.PortScanner()
    result = nm.scan(host, '1-1024')
    return nm.csv()  # Devuelve el resultado en formato CSV

@shared_task
def resolverdns(host):
    try:
        answers = dns.resolver.resolve(host, "MX")
        return [(rdata.exchange.to_text(), rdata.preference) for rdata in answers]
    except Exception as e:
        return str(e) 