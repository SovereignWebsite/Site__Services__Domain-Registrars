"""Corrections applied to site/data/registrars.json after the first research pass. Idempotent.
python3 docs/build/data_patches.py"""
import json, os
P = os.path.join(os.path.dirname(__file__), '..', '..', 'site', 'data', 'registrars.json')
d = json.load(open(P))
R = {r['id']: r for r in d['registrars']}
CK = '2026-11-25'
# Fields read from search-result summaries of official pages, not from the page itself.
RQ = {'namecheap': (['*'], 'namecheap.com returned 403 to our fetcher; every fact comes from search-result summaries of its official pages. Re-check by hand.'),
      'networksolutions': (['dnssec', 'account_security'], 'DNSSEC and account security come from a blog post and a help article seen through search summaries.'),
      'porkbun': (['tlds.uk', 'dnssec'], 'The .uk terms and the DNSSEC steps come from search summaries rather than full page reads.')}
for k, (fields, note) in RQ.items():
    R[k]['read_quality'] = {'summary_only_fields': fields, 'note': note}
r = R['route53']
r['api']['other'] = {'value': 'The ListPrices API action returns registration, renewal, transfer, change-of-owner and restoration prices per TLD (standard rates, not premium). Calling it needs an AWS account, so it was not called here.',
    'source': 'https://docs.aws.amazon.com/Route53/latest/APIReference/API_domains_ListPrices.html', 'checked': CK, 'note': None}
r['price_notes'] = [{'value': 'AWS publishes no per-TLD prices on the pricing page: it says prices vary by TLD and are per domain per year, and links a PDF price list whose filename suggests a 2014 date (not read). Treat any price from that PDF as possibly out of date.',
    'source': 'https://aws.amazon.com/route53/pricing/', 'checked': CK, 'note': None}] + [x for x in r.get('price_notes', []) if 'PDF' not in (x.get('value') or '')]
r['tlds']['pt'].update({'value': 'no (not in the supported TLD list)', 'source': 'https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/registrar-tld-list.html', 'checked': CK})
json.dump(d, open(P, 'w'), indent=1, ensure_ascii=False)
print('patched')
