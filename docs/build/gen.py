#!/usr/bin/env python3
"""Generate the static pages in site/ from site/data/registrars.json and the content modules.
Run from anywhere:  python3 docs/build/gen.py [--live d1]
No dependencies. Output is plain HTML and CSS: no script, no cookies, no tracking."""
import os, sys, json, shutil
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import content as C
import regs as R
from designs import DESIGNS, LIVE_DESIGN, picker_body

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SITE = os.path.join(ROOT, 'site')
live = LIVE_DESIGN
if '--live' in sys.argv: live = sys.argv[sys.argv.index('--live') + 1]

def write(path, html):
    p = os.path.join(SITE, path.strip('/'), 'index.html') if path != '/' else os.path.join(SITE, 'index.html')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(html)

DESC = {
 '/': 'A researched guide for anyone registering domains for customers: how registration works, whether you can buy direct, brokers, transfers, and registrars with APIs, each claim sourced and dated.',
 '/how-it-works/': 'ICANN, registries, registrars, resellers and registrants; WHOIS, RDAP and EPP; and what each layer charges, with sources.',
 '/buy-direct/': 'Which registries sell to the public and which only through registrars, and what becoming an ICANN registrar or Nominet member involves.',
 '/aftermarket/': 'When a domain is taken: contacting the holder, brokers, escrow, expired and drop-catch names, premium names. No broker is recommended.',
 '/transfers/': 'Transfers, auth codes, the 60-day rules, renewals, redemption, DNSSEC and privacy, with the .uk change due in February 2027.',
 '/registrars/': 'Sixteen registrars with APIs compared from their own pages: API, sandbox, .uk, .eu, .pt, prices, privacy, DNSSEC, security and reseller options.',
 '/choosing/': 'Who should own a domain registered for a customer, the access and records to keep, and a checklist.',
}
TITLE = {'/': 'Registering domains: how it works, and who has an API', '/how-it-works/': 'How it works', '/buy-direct/': 'Can you buy direct?',
 '/aftermarket/': 'Brokers and the aftermarket', '/transfers/': 'Transfers, locks, renewals, DNSSEC and privacy', '/registrars/': 'Registrars with APIs', '/choosing/': 'Choosing for customers'}
ACTIVE = {'/how-it-works/': 'how-it-works', '/buy-direct/': 'buy-direct', '/aftermarket/': 'aftermarket', '/transfers/': 'transfers', '/registrars/': 'registrars', '/choosing/': 'choosing'}

def pages_for(base, theme):
    out = {}
    banner = ''
    if base:
        d = DESIGNS[base.split('/')[-1]]
        banner = f'<p class="banner"><strong>Design preview {esc(d["key"])}: {esc(d["name"])}.</strong> <span class="bn-long">The live pages use {esc(DESIGNS[live]["key"])}. </span><a href="/designs/">Back to the picker</a>.</p>\n'
    bodies = {'/': C.home(base), '/how-it-works/': C.how(), '/buy-direct/': C.buy(), '/aftermarket/': C.after(),
              '/transfers/': C.transfers(), '/registrars/': R.registrars_page(base), '/choosing/': C.choosing()}
    # links in prose point at the live paths; inside a preview, keep readers inside it
    def rebase(h):
        if not base: return h
        for k in ('how-it-works', 'buy-direct', 'aftermarket', 'transfers', 'registrars', 'choosing', 'sources'):
            h = h.replace(f'href="/{k}/', f'href="{base}/{k}/')
        return h
    for path, body in bodies.items():
        out[path] = page(TITLE[path], DESC[path], path, rebase(body), base, theme, banner, active=ACTIVE.get(path))
    for r in C.REGS:
        path = f'/registrars/{r["id"]}/'
        nm = r['name']['value']
        out[path] = page(nm, f'{nm}: API, extensions, prices, privacy and security, read from its own pages on {CHECKED}.', path,
                         rebase(R.registrar_detail(r, base)), base, theme, banner, active='registrars')
    return out

def sources_page(base, theme, banner):
    groups = [('Structure, policy and registries', lambda k: not k.startswith(('escrow', 'godaddy', 'nc_', 'ns_', 'alibaba', 'ncsc', 'lookup', 'icann_udrp', 'nominet_drs', 'nominet_expiry', 'icann_rdrp', 'icann_webforms'))),
              ('Aftermarket, disputes and risks', lambda k: k.startswith(('escrow', 'godaddy', 'nc_', 'ns_', 'alibaba', 'ncsc', 'lookup', 'icann_udrp', 'nominet_drs', 'nominet_expiry', 'icann_rdrp', 'icann_webforms')))]
    secs = ''
    for title, f in groups:
        items = ''.join(f'<li>{(f'<a href="{esc(SOURCES[k]["url"])}">{esc(SOURCES[k]["title"])}</a>' if SOURCES[k]["url"] not in BAD else esc(SOURCES[k]["title"]) + ' (address no longer resolves)')} <span class="small">{esc(SOURCES[k]["url"])}. Checked {CHECKED}. {"<strong>Search summary only: the page itself was not opened.</strong>" if SOURCES[k]["how"] == "summary" else "Opened and read."}</span></li>' for k in sorted(USED) if f(k))
        secs += f'<h2>{esc(title)}</h2><ul class="srcs">{items}</ul>'
    reg = ''
    for r in C.REGS:
        reg += f'<h3 id="{r["id"]}">{esc(r["name"]["value"])}</h3><ul class="srcs">' + ''.join(f'<li>{links(u, esc(u))} <span class="small">Checked {CHECKED}.</span></li>' for u in r['sources']) + '</ul>'
    body = f'''{C.h1('Sources')}
{C.lead(f'Every source used on this site, with its link and the date it was checked: {CHECKED}.')}
<h2>How the checking was done</h2>
<ul><li>Pages were read through a summarising fetch tool, so wording is paraphrase unless in quotation marks.</li>
<li>Where a point comes only from a search-result summary, the page is marked "search summary only" here and next to the claim. Treat those as leads to confirm, not settled facts.</li>
<li>Pages that refused our fetcher (Nominet's public pages, Namecheap, some others) are named in the text where they matter.</li>
<li>No account was opened, nothing was bought and no API that needs an account was called. No affiliate or referral links are used anywhere.</li></ul>
{secs}
<h2>Registrar pages</h2><p>Each entry on the <a href="{base}/registrars/">registrars page</a> lists the vendor pages it was read from. All were checked on {CHECKED}.</p>
{reg}'''
    return page('Sources', 'Every source used on this site, with its link and the date checked.', '/sources/', body, base, theme, banner, active='sources')

def data_page(base, theme, banner):
    body = f'''{C.h1('Data and schema')}
{C.lead('The comparison tables are built from one file you can download and reuse.')}
<p><a href="/data/registrars.json">registrars.json</a> and its <a href="/data/registrars.schema.json">JSON Schema</a>. Checked {CHECKED}. {DATA_COUNT} registrars.</p>
<h2>How the file is shaped</h2>
<ul>
<li>Top level: <code>schema_version</code>, <code>title</code>, <code>checked</code>, <code>about</code> and <code>registrars</code> (a list).</li>
<li>Every datum is a <strong>claim</strong>: <code>value</code> (text as the vendor showed it, or <code>null</code>), <code>source</code> (the vendor page it came from), <code>checked</code> (date) and <code>note</code>. A <code>null</code> value means <em>not stated</em>: it could not be sourced from the vendor's own public pages.</li>
<li>Per registrar: <code>id</code>, <code>tier</code> (<code>core</code> or <code>extra</code>), <code>name</code>, <code>homepage</code>, <code>api</code> (<code>exists</code>, <code>docs_url</code>, <code>auth_style</code>, <code>sandbox</code>, <code>capabilities</code>, <code>other</code>), <code>tlds</code> (<code>uk</code>, <code>eu</code>, <code>pt</code>), <code>pricing_model</code>, <code>prices</code> (<code>com</code>, <code>uk</code>, <code>eu</code>, <code>pt</code>), <code>whois_privacy</code>, <code>dnssec</code>, <code>account_security</code>, <code>bulk_reseller</code>, <code>other_notes</code>, <code>read_quality</code> (only where some fields came from search summaries: it lists them, and the site badges those cells), <code>unverified_flags</code> and <code>sources</code>.</li>
<li>A price has <code>first_year</code>, <code>renewal</code>, <code>transfer</code> (strings as displayed), <code>currency</code>, <code>tax_inclusive</code> (true, false or null), <code>reading</code> (how to read it), <code>source</code> and <code>checked</code>. Prices are never converted or rounded, and may be promotional.</li>
</ul>
<h2>Rules</h2>
<ul><li>Never invent a field: if the vendor's pages do not say, the value stays <code>null</code>.</li>
<li>Prices change: each carries the date it was checked and its currency.</li>
<li>The tables on this site are generated from this file by <code>docs/build/gen.py</code> in the repository.</li></ul>'''
    return page('Data and schema', 'The registrars comparison as a JSON file with a documented schema.', '/data/', body, base, theme, banner)

SCHEMA = {
 "$schema": "https://json-schema.org/draft/2020-12/schema", "$id": LIVE + "/data/registrars.schema.json",
 "title": "Registrars comparison", "type": "object", "required": ["schema_version", "checked", "registrars"],
 "properties": {"schema_version": {"const": 1}, "title": {"type": "string"}, "checked": {"type": "string", "format": "date"}, "keeper": {"type": "string"}, "about": {"type": "string"},
   "registrars": {"type": "array", "items": {"$ref": "#/$defs/registrar"}}},
 "$defs": {
  "claim": {"type": "object", "description": "One datum. value null means not stated: it could not be sourced from the vendor's own public pages.", "required": ["value", "source", "checked", "note"],
    "properties": {"value": {"type": ["string", "null"]}, "source": {"type": ["string", "null"], "format": "uri"}, "checked": {"type": ["string", "null"], "format": "date"}, "note": {"type": ["string", "null"]}}},
  "price": {"type": "object", "description": "Strings exactly as the vendor displayed them on the checked date, in the vendor's currency. Never converted.",
    "properties": {"first_year": {"type": ["string", "null"]}, "renewal": {"type": ["string", "null"]}, "transfer": {"type": ["string", "null"]}, "currency": {"type": ["string", "null"]},
      "tax_inclusive": {"type": ["boolean", "string", "null"]}, "reading": {"type": ["string", "null"]}, "source": {"type": ["string", "null"], "format": "uri"}, "checked": {"type": ["string", "null"]}, "note": {"type": ["string", "null"]}}},
  "registrar": {"type": "object", "required": ["id", "tier", "name", "api", "tlds", "prices"],
    "properties": {"id": {"type": "string"}, "tier": {"enum": ["core", "extra"]}, "name": {"$ref": "#/$defs/claim"}, "homepage": {"$ref": "#/$defs/claim"},
      "api": {"type": "object", "properties": {"exists": {"$ref": "#/$defs/claim"}, "docs_url": {"$ref": "#/$defs/claim"}, "auth_style": {"$ref": "#/$defs/claim"}, "sandbox": {"$ref": "#/$defs/claim"},
        "capabilities": {"type": "object", "additionalProperties": {"$ref": "#/$defs/claim"}}, "other": {"$ref": "#/$defs/claim"}}},
      "tlds": {"type": "object", "properties": {k: {"$ref": "#/$defs/claim"} for k in ("uk", "eu", "pt")}},
      "pricing_model": {"$ref": "#/$defs/claim"},
      "prices": {"type": "object", "properties": {k: {"$ref": "#/$defs/price"} for k in ("com", "uk", "eu", "pt")}},
      "price_notes": {"type": "array", "items": {"$ref": "#/$defs/claim"}},
      "whois_privacy": {"$ref": "#/$defs/claim"}, "dnssec": {"$ref": "#/$defs/claim"}, "account_security": {"$ref": "#/$defs/claim"},
      "bulk_reseller": {"$ref": "#/$defs/claim"}, "other_notes": {"$ref": "#/$defs/claim"}, "access_note": {"oneOf": [{"$ref": "#/$defs/claim"}, {"type": "null"}]},
      "read_quality": {"type": "object", "description": "Present when some fields came from search-result summaries rather than the official page itself. summary_only_fields lists them (* means all).", "properties": {"summary_only_fields": {"type": "array", "items": {"type": "string"}}, "note": {"type": "string"}}},
      "unverified_flags": {"type": "array"}, "sources": {"type": "array", "items": {"type": "string", "format": "uri"}}}}}}

DATA_COUNT = len(C.REGS)

def main():
    # live pages
    allp = pages_for('', live)
    for path, h in allp.items(): write(path, h)
    write('/sources/', '')  # placeholder so link checks resolve while building
    for k in DESIGNS:
        base = f'/designs/{k}'
        pg = pages_for(base, k)
        banner = pages_for.__doc__ or ''
        for path, h in pg.items(): write(base + path, h)
    # sources and data pages last, so USED is complete
    write('/sources/', sources_page('', live, ''))
    write('/data/', data_page('', live, ''))
    for k in DESIGNS:
        base = f'/designs/{k}'
        b = f'<p class="banner"><strong>Design preview {esc(DESIGNS[k]["key"])}: {esc(DESIGNS[k]["name"])}.</strong> <a href="/designs/">Back to the picker</a>.</p>\n'
        write(base + '/sources/', sources_page(base, k, b).replace('href="/registrars/"', f'href="{base}/registrars/"'))
    write('/designs/', page('Choose a design', 'Five design directions for this site. Open each, then tell Dinis Cruz which number to keep.', '/designs/', picker_body(live), '', live, active='designs'))
    json.dump(SCHEMA, open(os.path.join(SITE, 'data', 'registrars.schema.json'), 'w'), indent=1)
    print('pages written; live design', live)
main()
