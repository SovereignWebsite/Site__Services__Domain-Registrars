"""Shared helpers for the site generator. Static output only: no script, no cookies, no tracking."""
import html, re, json

LIVE = 'https://domain-registrars.services.sovereignweb.site'
CARD = LIVE + '/assets/share/card-1200x630.jpg'
CHECKED = '25 Nov 2026'
SITE_NAME = 'Domain registrars: how buying a domain works, and the good options'

def clean(s):
    """House style: no em or en dashes in visible text."""
    if s is None: return s
    s = str(s)
    s = re.sub(r'(?<=\d)\s*[–]\s*(?=\d)', ' to ', s)
    s = s.replace('—', ', ').replace('–', '-')
    return s

BAD = set(json.load(open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'badlinks.json'))))
_URL = re.compile(r'https?://[^\s<>"]+')
def links(text, label='source', cls='srclink'):
    """Anchors for each good web address in text; an address that answered 404 on the check date is shown as text, not linked."""
    out = []
    for u in _URL.findall(text or ''):
        u = u.rstrip('.,;)')
        if u in BAD: out.append(f'<span class="{cls}">{label} (address no longer resolves, 404 on {CHECKED}; check by hand)</span>')
        else: out.append(f'<a class="{cls}" href="{html.escape(u, quote=True)}">{label}</a>')
    return ' '.join(out)

def esc(s): return html.escape(clean(s) if s is not None else '', quote=True)

SOURCES = {}   # key -> dict(url,title,how)
USED = set()
def src(key, url, title, how='read'): SOURCES[key] = dict(url=url, title=title, how=how)

def cite(*keys):
    out = []
    for k in keys:
        USED.add(k); s = SOURCES[k]
        tag = ' <span class="flag badge">Not read on the official page: from a search summary</span>' if s['how'] == 'summary' else ''
        out.append((f'<a href="{esc(s["url"])}">{esc(s["title"])}</a>' if s['url'] not in BAD else f'{esc(s["title"])} (address no longer resolves, 404 on {CHECKED})') + tag)
    return f'<span class="src">Source: {"; ".join(out)}. Checked {CHECKED}.</span>'

def P(text, *keys): return f'<p>{text} {cite(*keys) if keys else ""}</p>'

def short(text, n=110):
    t = clean(text or '')
    if len(t) <= n: return esc(t), None
    cut = t[:n]
    m = max(cut.rfind('. '), cut.rfind('; '), cut.rfind(', '), cut.rfind(' ('))
    if m > 40: cut = cut[:m]
    else: cut = cut[:cut.rfind(' ')] if ' ' in cut else cut
    return esc(cut.rstrip(' ,;.(')) + '…', esc(t)

def cell_claim(c, n=110, link=True):
    """A table cell for one claim: short text, full text in a details element, source link, or 'not stated'."""
    if not c or c.get('value') is None:
        note = (c or {}).get('note') or 'not stated'
        return f'<span class="ns">not stated</span>' + ('' if note == 'not stated' else f'<details><summary>why</summary>{esc(note)}</details>')
    s, full = short(c['value'], n)
    srcl = (' ' + links(c['source'])) if c.get('source') and link else ''
    if full:
        return f'<details><summary>{s}</summary><p>{full}</p>{srcl}</details>'
    return f'{s}{srcl}'

def head(title, desc, path, base, theme, noindex=False):
    full = f'{title}: {SITE_NAME}' if path != '/' else title
    url = LIVE + path
    robots = '<meta name="robots" content="noindex">\n' if noindex else ''
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
{robots}<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:locale" content="en_GB">
<meta property="og:url" content="{esc(url)}">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{CARD}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(SITE_NAME)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(full)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{CARD}">
<link rel="canonical" href="{esc(url)}">
<link rel="stylesheet" href="/assets/base.css">
<link rel="stylesheet" href="/assets/themes/{theme}.css">
</head>
'''

FAMILY = '''<details class="family-credit">
  <summary>Sovereign Website</summary>
  <ul>
    <li><a href="/start/">Start here</a></li>
    <li><a href="/agents/">Use with your AI</a></li>
    <li class="family-gap"><a href="/admin/">How this site was made</a></li>
    <li><a href="https://sovereignwebsite.ai/">Sovereign Website</a></li>
    <li><a href="https://sovereignwebsite.org/">Principles</a></li>
    <li><a href="https://sovereignwebsite.site/">Hosted</a></li>
    <li><a href="https://hub.sovereignweb.site/">Hub</a></li>
    <li><a href="https://agents.sovereignweb.site/">Agents</a></li>
    <li><a href="https://vault.sovereignwebsite.site/">Vault</a></li>
    <li><a href="https://agenticcells.ai/">AgentiCCells</a></li>
    <li><a href="https://riskmandate.ai/">RiskMandate</a></li>
    <li><a href="https://newsroom.sgit.ai/">Newsroom</a></li>
  </ul>
</details>
'''

NAV = [('how-it-works', 'How it works'), ('buy-direct', 'Buy direct?'), ('aftermarket', 'Brokers and aftermarket'),
       ('transfers', 'Transfers and renewals'), ('registrars', 'Registrars with APIs'), ('choosing', 'Choosing for customers'),
       ('sources', 'Sources'), ('designs', 'Designs')]

def page(title, desc, path, body, base='', theme='d1', banner='', noindex=False, active=None):
    """path: the live path, e.g. '/how-it-works/'. base: '' live, '/designs/d2' for a preview."""
    nav = ''.join(f'<li><a href="{base}/{k}/"{" aria-current=\"page\"" if active == k else ""}>{esc(t)}</a></li>'
                  if k != 'designs' else f'<li><a href="/designs/"{" aria-current=\"page\"" if active == "designs" else ""}>{esc(t)}</a></li>'
                  for k, t in NAV)
    return head(title, desc, path, base, theme, noindex or bool(base)) + f'''<body class="theme-{theme}">
<a class="skip" href="#main">Skip to content</a>
{FAMILY}<div class="wrap">
<header class="top">
  <a class="name" href="{base or ''}/">{esc(SITE_NAME)}</a>
  <nav class="main-nav" aria-label="Sections"><ul>{nav}</ul></nav>
</header>
<main id="main">
{banner}{body}
</main>
<footer class="foot">
<nav class="site-links" aria-label="About this site">
  <a href="/start/">Start here</a>
  <a href="/agents/">Use with your AI</a>
  <a href="/admin/">How this site was made</a>
  <a href="/policy/">How this site is governed</a>
  <a href="/data/">Data and schema</a>
</nav>
<p>Everything here is sourced and dated, and prices change: check the vendor before you buy. No accounts were opened and nothing was bought to make this site. No cookies, no tracking, no affiliate links. A sovereign website, made with the <a href="https://sovereignwebsite.org/">open pattern</a>. Source: <a href="https://github.com/SovereignWebsite/Site__Services__Domain-Registrars">github.com/SovereignWebsite/Site__Services__Domain-Registrars</a>.</p>
</footer>
</div>
</body>
</html>
'''
