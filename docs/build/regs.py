from lib import *
from content import REGS, table, td, h1, lead, note, gap, matrix_table, cell_claim

BADGE = '<span class="badge">Not read on the official page: from a search summary</span>'
def B(r, field):
    q = r.get('read_quality') or {}
    f = q.get('summary_only_fields') or []
    return (' ' + BADGE) if ('*' in f or field in f) else ''

def price_cell(p, tld):
    if not (p['first_year'] or p['renewal'] or p['transfer']):
        n = p.get('note') or 'not stated'
        return '<span class="ns">not stated</span>' + ('' if n == 'not stated' else f'<details><summary>why</summary>{esc(n)}</details>')
    cur = p.get('currency') or ''
    def f(v): 
        if v is None: return '-'
        return clean(v) if (cur and cur in v) else clean(v)
    tax = '' if p.get('tax_inclusive') is None else (' ex VAT' if p['tax_inclusive'] is False else (' incl. tax' if p['tax_inclusive'] is True else f' ({esc(p["tax_inclusive"])})'))
    line = f'<span class="pr">first year <b>{esc(f(p["first_year"]))}</b><br>renewal <b>{esc(f(p["renewal"]))}</b><br>transfer <b>{esc(f(p["transfer"]))}</b></span>'
    meta = f'<span class="small">{esc(cur)}{tax}. Checked {esc(p.get("checked") or CHECKED)}.</span>'
    rd = f'<details><summary>how to read</summary>{esc(p["reading"])}</details>' if p.get('reading') else ''
    sl = (' ' + links(p['source'])) if p.get('source') else ''
    return f'{line}<br>{meta}{sl}{rd}'

def registrars_page(base):
    name = lambda r: f'<a href="{base}/registrars/{r["id"]}/">{esc(r["name"]["value"])}</a>'
    api = table('APIs: documentation, authentication, sandbox and what the API can do',
      ['Registrar', 'API', 'Docs', 'Auth style', 'Sandbox', 'Register, transfer, renew'],
      [[td(name(r), True), td(cell_claim(r['api']['exists'], 60) + B(r, 'api')),
        td(links(r['api']['docs_url']['value'], 'docs') if r['api']['docs_url']['value'] and r['api']['docs_url']['value'].startswith('http') else cell_claim(r['api']['docs_url'], 60)),
        td(cell_claim(r['api']['auth_style'], 80) + B(r, 'api')), td(cell_claim(r['api']['sandbox'], 80) + B(r, 'api')),
        td('<ul class="tight">' + ''.join(f'<li>{lab}: {cell_claim(r["api"]["capabilities"][k], 45, False)}</li>' for k, lab in (('can_register', 'register'), ('can_transfer', 'transfer'), ('can_renew', 'renew'))) + '</ul>' + B(r, 'api'))] for r in REGS])
    tl = table('Extensions and prices: .uk, .eu and .pt support, and first-year, renewal and transfer prices',
      ['Registrar', 'Pricing model', '.uk', '.eu', '.pt', '.com price', '.uk price', '.eu price', '.pt price'],
      [[td(name(r), True), td(cell_claim(r['pricing_model'], 70) + B(r, 'pricing_model'))] +
       [td(cell_claim(r['tlds'][t], 55) + B(r, 'tlds.' + t)) for t in ('uk', 'eu', 'pt')] +
       [td(price_cell(r['prices'][t], t) + B(r, 'prices.' + t)) for t in ('com', 'uk', 'eu', 'pt')] for r in REGS])
    sec = table('Privacy, DNSSEC, account security, and bulk or reseller options',
      ['Registrar', 'WHOIS privacy', 'DNSSEC', 'Account security (2FA, lock)', 'Bulk and reseller'],
      [[td(name(r), True)] + [td(cell_claim(r[k], 90) + B(r, k)) for k in ('whois_privacy', 'dnssec', 'account_security', 'bulk_reseller')] for r in REGS])
    hint = '<p class="hint">Swipe the table sideways to see more columns. The registrar name stays in view.</p>'
    return f'''{h1('Registrars with APIs')}
{lead(f'{len(REGS)} registrars, read from their own public pages on {CHECKED}. Every cell is either sourced (with a link) or says <em>not stated</em>. No account was opened, nothing was bought and no API call needing an account was made.')}
<h2 id="glance">Coverage at a glance</h2>
{hint}{matrix_table(False, base)}
<h2 id="api">APIs</h2>{hint}{api}
<h2 id="prices">Extensions and prices</h2><details class="readme"><summary><strong>How to read the prices, and the pricing model</strong></summary>
<p>Every price was checked on 25 Nov 2026 and is shown in the vendor's own currency. First year and renewal are different numbers, so compare both, and the transfer price too. VAT or sales tax is not included unless the cell says so. An empty cell means <em>not stated</em>, not free. Prices change, and many first-year prices are promotions: check the vendor before you buy.</p>
<p class="ours"><strong>Our reading, not a sourced fact.</strong> Cloudflare states it charges at cost; other vendors in the data show retail margin, volume tiers, or do not say. Compare renewal against first-year price, which often differs.</p></details>
{hint}{tl}
<h2 id="security">Privacy, security and resellers</h2>{hint}{sec}
<h2>Confidence</h2>
<ul><li>Namecheap's pages returned 403 to our fetcher, so its entry comes from search-result summaries of official pages and needs a manual re-check. The same applies to parts of Porkbun and Network Solutions.</li>
<li>Route 53 and Cloudflare publish few prices on readable pages; their price cells are empty rather than guessed.</li>
<li>Where two pages conflicted, the entry's page lists the flag.</li></ul>
<p class="small">Prices are shown exactly as each vendor displayed them on that date, in its currency, and may be promotional or exclude tax. They are strings, not converted. Machine-readable: <a href="/data/registrars.json">registrars.json</a> (<a href="/data/">schema</a>).</p>
'''

def registrar_detail(r, base):
    SUMF = (r.get('read_quality') or {}).get('summary_only_fields') or []
    FIELD = {'API': 'api', 'Docs': 'api', 'Auth style': 'api', 'Sandbox': 'api', 'Register': 'api', 'Transfer in': 'api', 'Renew': 'api', 'Manage DNS': 'api', 'Set nameservers': 'api', 'Other': 'api',
             'Pricing model': 'pricing_model', 'WHOIS privacy': 'whois_privacy', 'DNSSEC': 'dnssec', 'Account security': 'account_security', 'Bulk and reseller': 'bulk_reseller', 'Other notes': 'other_notes', 'Access note': 'other_notes'}
    def row(label, c): return f'<tr><th scope="row">{label}</th><td>{cell_claim(c, 100000)}{B(r, FIELD.get(label, ""))}</td></tr>'
    caps = ''.join(row(lab, r['api']['capabilities'][k]) for k, lab in (('can_register', 'Register'), ('can_transfer', 'Transfer in'), ('can_renew', 'Renew'), ('can_manage_dns', 'Manage DNS'), ('can_set_nameservers', 'Set nameservers')))
    a = ''.join([row('API', r['api']['exists']), row('Docs', r['api']['docs_url']), row('Auth style', r['api']['auth_style']), row('Sandbox', r['api']['sandbox'])]) + caps + (row('Other', r['api']['other']) if r['api']['other']['value'] else '')
    tl = ''.join(f'<tr><th scope="row">.{t}</th><td>{cell_claim(r["tlds"][t], 100000)}{B(r, "tlds." + t)}{("<p>"+ esc(r["tlds"][t]["notes"]) + "</p>") if r["tlds"][t].get("notes") else ""}</td></tr>' for t in ('uk', 'eu', 'pt'))
    pr = ''.join(f'<tr><th scope="row">.{t}</th><td>{price_cell(r["prices"][t], t)}{B(r, "prices." + t)}</td></tr>' for t in ('com', 'uk', 'eu', 'pt'))
    pn = ''.join(f'<li>{esc(c["value"])} {links(c.get("source"))}</li>' for c in r['price_notes'])
    other = ''.join([row('Pricing model', r['pricing_model']), row('WHOIS privacy', r['whois_privacy']), row('DNSSEC', r['dnssec']), row('Account security', r['account_security']), row('Bulk and reseller', r['bulk_reseller']), row('Other notes', r['other_notes'])])
    if r.get('access_note'): other += row('Access note', r['access_note'])
    flags = ''.join(f'<li>{esc(f if isinstance(f, str) else json.dumps(f))}</li>' for f in r['unverified_flags'])
    srcs = ''.join(f'<li>{links(u, esc(x))}</li>' for u in r['sources'] for x in [u] if u)
    nm = r['name']['value']
    rqd = r.get('read_quality')
    rq = f'<p class="gap"><strong>{"Not read on the official page: from a search summary." if "*" in rqd["summary_only_fields"] else "Partly from a search summary."}</strong> {esc(rqd["note"])}</p>' if rqd else ''
    hp = r['homepage']['value']
    return f'''<p><a href="{base}/registrars/">All registrars</a></p>{h1(nm)}
{lead(f'Read from {esc(nm)}\'s own public pages on {CHECKED}. ' + (links(hp, esc(hp), 'hp') if hp else ''))}
{rq}<h2>API</h2><div class="scroll" tabindex="0" role="region" aria-label="API details"><table class="kv"><caption>API details for {esc(nm)}</caption><tbody>{a}</tbody></table></div>
<h2>Extensions</h2><div class="scroll" tabindex="0" role="region" aria-label="Extension support"><table class="kv"><caption>Extension support for {esc(nm)}</caption><tbody>{tl}</tbody></table></div>
<h2>Prices</h2><div class="scroll" tabindex="0" role="region" aria-label="Prices"><table class="kv"><caption>Prices for {esc(nm)}, as displayed on {CHECKED}</caption><tbody>{pr}</tbody></table></div>
{('<ul>' + pn + '</ul>') if pn else ''}
<h2>Privacy, security and the rest</h2><div class="scroll" tabindex="0" role="region" aria-label="Other details"><table class="kv"><caption>Other details for {esc(nm)}</caption><tbody>{other}</tbody></table></div>
{('<h2>Flags: conflicts or doubts</h2><ul>' + flags + '</ul>') if flags else ''}
<h2>Pages read</h2><ul class="srcs">{srcs}</ul>
'''
