"""Page bodies. Every factual sentence carries its source; what is our reading says so."""
import json
from lib import *
import sources  # noqa

DATA = json.load(open('/home/user/Site__Services__Domain-Registrars/site/data/registrars.json'))
REGS = DATA['registrars']

def lead(t): return f'<p class="lead">{t}</p>'
def h1(t, kicker=''): return f'<div class="mark">{esc(kicker)}</div><h1>{esc(t)}</h1>' if kicker else f'<h1>{esc(t)}</h1>'
def note(t): return f'<p class="ours"><strong>Our reading, not a sourced fact.</strong> {t}</p>'
def gap(t): return f'<p class="gap"><strong>Not stated.</strong> {t}</p>'
def table(cap, head_, rows, label=None):
    th = ''.join(f'<th scope="col">{h}</th>' for h in head_)
    tr = ''.join('<tr>' + ''.join(c for c in r) + '</tr>' for r in rows)
    return (f'<div class="scroll" tabindex="0" role="region" aria-label="{esc(label or cap)}">'
            f'<table><caption>{esc(cap)}</caption><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>')
def td(x, rowh=False): return f'<th scope="row">{x}</th>' if rowh else f'<td>{x}</td>'

# ---------- stats from data ----------
def stats():
    cells = 0; filled = 0
    for r in REGS:
        for t in ('com', 'uk', 'eu', 'pt'):
            cells += 1; filled += 1 if r['prices'][t]['first_year'] or r['prices'][t]['renewal'] else 0
    return dict(n=len(REGS), core=sum(1 for r in REGS if r['tier'] == 'core'), cells=cells, filled=filled)

# ---------- HOME ----------
def home(base):
    s = stats()
    b = base
    cards = [
     ('how-it-works', 'How it works', 'ICANN, registries, registrars, resellers and you; WHOIS, RDAP and EPP; what each layer charges.'),
     ('buy-direct', 'Can you buy direct?', 'What the registries say, and what it takes to become an accredited registrar or a Nominet member.'),
     ('aftermarket', 'Brokers and the aftermarket', 'When a name is taken: contacting the holder, escrow, expired names, premium names. No broker is recommended.'),
     ('transfers', 'Transfers and renewals', 'Auth codes, the 60-day rules, grace periods, DNSSEC, privacy, and the .uk change due in February 2027.'),
     ('registrars', 'Registrars with APIs', f'{s["n"]} registrars compared from their own pages, with every field sourced or marked not stated.'),
     ('choosing', 'Choosing for customers', 'Why the customer should be the registrant, and a checklist for registering on someone\'s behalf.'),
    ]
    cs = ''.join(f'<li><a class="card" href="{b}/{k}/"><span class="ct">{esc(t)}</span><span class="cd">{esc(d)}</span></a></li>' for k, t, d in cards)
    matrix = matrix_table(core_only=True, base=b)
    return f'''{h1('Registering domains: how it works, and who has an API', 'domain-registrars.services.sovereignweb.site')}
{lead('A researched guide for anyone registering domains on behalf of customers: how the system fits together, whether you can buy direct, what to do when a name is taken, and which registrars offer an API. Every claim has its source and the date it was checked.')}
<ul class="cards">{cs}</ul>
<section aria-labelledby="short"><h2 id="short">Short answers</h2>
<dl class="short">
<dt>Can you buy a domain straight from the registry?</dt>
<dd>The sources show registries working through accredited registrars: ICANN describes one registry in charge of each top-level domain, with registrars paying it a per-domain fee and free to charge what they wish. Verisign says it manages relationships with about 3,000 accredited registrars. For .uk, Nominet requires every registrar to be a member. Whether a registry also sells to the public is <strong>not stated</strong> on the pages we could read for Nominet, EURid and .PT. {cite('icann_what','verisign_registry','nominet_faq')}</dd>
<dt>Do you need a broker?</dt>
<dd>Only when the name you want is already registered and the holder will not sell through a normal route. For a free name, no: you register it through a registrar. See <a href="{b}/aftermarket/">brokers and the aftermarket</a>.</dd>
<dt>What does a .com cost at the bottom of the chain?</dt>
<dd>Verisign's wholesale fee rose from $10.26 to $10.97 per domain-year on 1 November 2026, and ICANN's transaction fee is $0.20 per domain-year. Registrar margin sits on top and is set by each registrar. {cite('verisign_10q','icann_fy27')}</dd>
</dl></section>
<section aria-labelledby="cmp"><h2 id="cmp">The comparison at a glance</h2>
<p>The eleven registrars first named in the brief. The full table, with prices, security and reseller options, is on the <a href="{b}/registrars/">registrars page</a>. A dash in a cell means the vendor's own pages did not say.</p>
{matrix}
<p class="small">{s["n"]} registrars in the data ({s["core"]} core, {s["n"]-s["core"]} extra). Of {s["cells"]} price cells (registrar by .com, .uk, .eu, .pt), {s["filled"]} have a price we could source; the rest are empty on purpose, because we do not guess a price. Machine-readable: <a href="/data/registrars.json">registrars.json</a>.</p></section>
'''

def lead_word(c):
    v = (c or {}).get('value')
    if v is None: return '<span class="chip na">not stated</span>'
    w = clean(v).strip().lower()
    if w.startswith('yes'): return '<span class="chip yes">yes</span>'
    if w == 'no' or w.startswith(('no:', 'no (', 'no,')): return '<span class="chip no">no</span>'
    if w.startswith('limited'): return '<span class="chip part">limited</span>'
    if w.startswith('not listed'): return '<span class="chip na">not listed</span>'
    if w.startswith('not '): return '<span class="chip na">not stated</span>'
    return '<span class="chip part">see note</span>'

def matrix_table(core_only=False, base=''):
    rows = []
    for r in REGS:
        if core_only and r['tier'] != 'core': continue
        rows.append([td(f'<a href="{base}/registrars/{r["id"]}/">{esc(r["name"]["value"])}</a>', True),
                     td(lead_word(r['api']['exists'])), td(lead_word(r['api']['sandbox'])),
                     td(lead_word(r['tlds']['uk'])), td(lead_word(r['tlds']['eu'])), td(lead_word(r['tlds']['pt']))])
    return table('API, sandbox and .uk, .eu, .pt support, from each vendor\'s own pages', ['Registrar', 'API', 'Sandbox', '.uk', '.eu', '.pt'], rows, 'Comparison at a glance')

# ---------- HOW IT WORKS ----------
def how():
    layers = '''<ol class="layers">
<li><strong>ICANN</strong>: coordinates the naming system and contracts with gTLD registries and accredited registrars. It does not control content.</li>
<li><strong>The registry</strong>: one organisation in charge of every name under a top-level domain (Verisign for .com, Nominet for .uk, EURid for .eu, the .PT registry for .pt).</li>
<li><strong>The accredited registrar</strong>: has direct access to the registry and sells names to the public. Registrars set their own prices.</li>
<li><strong>The reseller</strong>: sells on behalf of a registrar. The ICANN pages we fetched do not describe resellers, so we say no more here.</li>
<li><strong>The registrant</strong>: the holder of the name. The party the registry data and the transfer rules treat as the owner.</li>
</ol>'''
    fees = table('What each layer charges for a .com, and for the three country domains we checked',
      ['Layer', '.com', '.uk', '.eu', '.pt'],
      [[td('Registry fee', True), td(f'$10.97 per domain-year from 1 Nov 2026 (was $10.26). {cite("verisign_10q")}'),
        td(f'£3.90 a year for members, ex VAT; £80.00 listed for non-members (2-year period). Schedule marked effective 13 Jan 2020, page updated 9 Apr 2026. {cite("nominet_fees")}'),
        td(f'€4.60 for registration and for each renewal year. {cite("eurid_price")}'),
        td(f'€9.60 plus VAT per domain-year, billed to registrars. {cite("pt_prices")}')],
       [td('ICANN fee', True), td(f'$0.20 per domain-year (transaction fee, FY26 and FY27 letters). {cite("icann_fy26","icann_fy27")}'),
        td('Not applicable as ICANN policy: .uk is a country domain with its own rules (our reading; no single sentence found).'), td('As .uk.'), td('As .uk.')],
       [td('Registrar margin', True), td(f'Not stated by any primary source. ICANN says registrars are "free to charge whatever they wish". {cite("icann_what")}'),
        td('Same: set by each registrar.'), td('Same.'), td('Same.')]])
    return f'''{h1('How it works')}
{lead('Five layers sit between you and a working domain. Knowing which one you are dealing with explains most of the prices, the rules and the delays.')}
<h2>The layers</h2>
{layers}
{P('ICANN: "dedicated to keeping the Internet secure, stable and interoperable". For each top-level domain "one company ... is in charge of all domains ending with" it, called the registry, and ICANN contracts with it. An accredited registrar "offers domain name registration services" with "direct access to the gTLD registries". Verisign operates the .com registry and manages relationships with approximately 3,000 accredited registrars.', 'icann_what','icann_raa','verisign_registry')}
{P('The .PT registry now lives at pt.pt (the old dns.pt address redirects there).', 'pt_prices')}
{note('The .com registry agreement is an ICANN contract, so the ICANN rules and fees below apply to .com and other gTLDs. Country domains such as .uk, .eu and .pt run on their own registry rules. We found no single page stating this, so treat it as a working assumption and check each registry.')}
<h2>WHOIS, RDAP and EPP</h2>
{P('WHOIS is the old way to look up who holds a name. RDAP is its replacement, developed by the IETF: ICANN says it was created "as the replacement for the WHOIS protocol" and gives "WHOIS-like registration data". Since 28 January 2025 gTLD registries and registrars are no longer required to provide WHOIS, with exceptions for .com, .name and .post, and all must provide RDAP.', 'icann_rdap')}
{P('RDAP is defined in RFC 7480 to 7484 (HTTP usage, security, query format, JSON responses and bootstrapping). We opened RFC 7480 only.', 'rfc7480')}
{P('EPP, the Extensible Provisioning Protocol, is how registrars talk to registries: an XML application-layer protocol defined in RFC 5730 (August 2009). The .PT registry requires registrars to integrate through EPP. This is why a registrar API usually wraps EPP rather than replacing it.', 'rfc5730','pt_become')}
<h2>What each layer charges</h2>
{fees}
{P('ICANN states that its transaction fee "can be billed by the registrar separately on its invoice to the registrant", so some registrars show it as a separate line.', 'icann_fin')}
{P('The .com price is capped: Verisign may raise it by up to 7 per cent in each of the final four years of each six-year period, and the current period began 26 October 2024. The 2020 amendment announcement said the price was $7.85 then and could not exceed $10.26 until October 2026. We could not read the cap clause in the registry agreement itself, so the figure above is from Verisign\'s own filing.', 'verisign_10q','icann_com2020','icann_comra')}
{gap('EURid\'s wholesale figure comes from a search result, not an opened page, and is marked so. Nominet and EURid pages for the public side of pricing returned errors to our fetcher.')}
'''

# ---------- BUY DIRECT ----------
def buy():
    rows = [
     [td('ICANN (gTLDs such as .com)', True),
      td(f'The registry (Verisign for .com) lists "Become a Registrar" and "Find a Registrar" and serves about 3,000 accredited registrars. An explicit "we do not sell to the public" statement: not stated. {cite("verisign_registry")}'),
      td(f'Application fee $3,500, non-refundable. Accreditation fee $4,000 a year. Transaction fee $0.20 per domain-year, billed quarterly, plus a variable fee shared among registrars. "Adequate working capital": $70,000 or more in liquid capital is deemed adequate for initial accreditation. Insurance: not stated on that page. Then a registry contract and technical tests: per a Verisign page seen only in a search summary, the Operational Test and Evaluation environment. {cite("icann_fin","icann_regs_old","verisign_become")}')],
     [td('Nominet (.uk)', True),
      td(f'Nominet\'s consumer pages returned errors to us, so its own statement on direct sales is <strong>not stated</strong>. Its fee schedule is registrar-facing, with member and non-member rates. {cite("nominet_fees")}'),
      td(f'Membership is required: "all .UK Registrars must be members of Nominet" (with a small exception for .sch.uk-only managers). Joining fee £400, annual subscription £100. Tag types (Accredited Channel Partner, Channel Partner, Self-Managed) are described only in a search summary. {cite("nominet_faq","nominet_fees","nominet_tags")}')],
     [td('EURid (.eu)', True),
      td(f'The become-a-registrar page does not say whether EURid sells direct; its fee schedule applies only to accredited registrars. <strong>Not stated.</strong> {cite("eurid_become")}'),
      td(f'Proof of business and good financial standing; a website in an EU official language with pricing and an availability check; customer support in an EU language; technical competence. Advance payment of at least €2,500, balance kept at or above €2,500, and at least €500 of payable transactions a year. {cite("eurid_become")}')],
     [td('.PT (.pt)', True),
      td(f'The prices page says registrations are made through registrars, who pay .PT. It does not say whether the public may register directly. <strong>Not stated.</strong> {cite("pt_prices")}'),
      td(f'€1,200 joining fee on signing the registry-registrar agreement; €1,000 a year after the first year, plus VAT; at least 200 domains under management from the third year; integration through EPP and technical compliance tests; ISO/IEC 27001 or equivalent from 1 January 2029. {cite("pt_become")}')],
    ]
    t = table('Does each registry sell to the public, and what does it take to become a registrar?', ['Registry', 'Sells to the public directly?', 'To become a registrar or member'], rows)
    return f'''{h1('Can you buy direct?')}
{lead('Short version from the sources: names are sold to the public by registrars, and registries describe themselves as serving registrars. Becoming one yourself is a business with fixed costs, not a way to buy a few domains cheaply.')}
{t}
{note('Adding the ICANN and Verisign figures, an accredited registrar pays $3,500 to apply and $4,000 a year before registering a single name, and must show working capital. Nominet membership is £400 to join and £100 a year, but the wholesale rate is £3.90 against £80.00 listed for non-members, which is why members are the ones who sell. For a handful of customer domains these fixed costs dominate, so using an existing registrar with an API is the practical route. This is arithmetic and judgement on the sourced figures, not a quoted conclusion.')}
<h2>What about the registry's own site?</h2>
{P('Some registries have a "Register" or "Find a registrar" link. On the pages we could read, those links lead to the list of accredited registrars. Where a registry page was blocked to our fetcher (Nominet\'s public pages answered 403), we say so rather than guess.', 'eurid_become','pt_prices')}
<h2>Gaps in this section</h2>
<ul><li>No registry page we read states outright whether it sells to the public.</li>
<li>.eu transfer notes and .pt transfer notes: not stated.</li>
<li>ICANN insurance requirement: not stated on the financials page.</li>
<li>The .com agreement text itself (the cap clause) could not be read.</li></ul>
'''

# ---------- AFTERMARKET ----------
def after():
    return f'''{h1('Brokers and the aftermarket')}
{lead('If the name you want is free, register it. If it is taken, you have three routes: ask the holder, use a marketplace, or pay a broker. This page explains how each works. It does not recommend any broker, because none has been sourced as one.')}
<h2>When a name is already registered</h2>
{P('ICANN says to use ICANN Lookup to find the registrar; the registrar should offer a web form or other method to contact a registrant whose details are not public. Registrant fields in RDAP are often shown as redacted, and the registrar contact must be an email address or web form that does not reveal the registrant\'s address.', 'lookup_icann','icann_rdrp','icann_webforms')}
{P('A May 2026 ICANN advisory notes the Registration Data Policy took effect on 21 August 2025 and requires registrars to publish a registrant email, often pseudonymised or a web form. At least one registrar\'s form only allows a message to the registrant or technical contact.', 'icann_webforms')}
{P('The aftermarket is the resale market for names already registered; a buyer bids or negotiates to move the registration from the current holder. One registrar\'s guide describes it that way; we found no formal regulation of it in the sources.', 'ns_aftermarket')}
{gap('Whether a holder must reply: not stated by ICANN. A broker\'s service page notes a sale can fail if the registrant is unreachable or refuses.')}
<h2>What a broker does</h2>
{P('A broker contacts the current registrant, may analyse the name, negotiates a price and helps complete the transaction; some keep the buyer\'s identity private. This description is from one cloud provider\'s own service page.', 'alibaba_broker')}
{gap('Broker fees, and any ICANN or registry page describing brokers: not found. We name no broker.')}
<h2>How escrow works</h2>
{P('Escrow.com\'s own steps: buyer and seller agree the domain and price; the buyer pays Escrow.com; the seller is told to transfer the domain and confirms; the buyer confirms possession and an inspection period runs; funds go to the seller when the transfer is verified or inspection ends. The buyer should verify the seller\'s ownership before sending funds.', 'escrow_how','escrow_learn')}
{gap('Escrow fee amounts and who pays: neither Escrow.com page states them ("low transparent fees" and a calculator).')}
{P('The transfer step itself follows ICANN\'s Transfer Policy: the registrar must give the registrant an auth code (or remove the lock) within five calendar days of a request, and a change of registrant name, organisation or email triggers a confirmation process and a 60-day transfer lock unless opted out beforehand. See <a href="/transfers/">transfers and renewals</a>.', 'icann_transfer16','icann_transfer')}
<h2>Expired names, auctions and drop-catching</h2>
{P('ICANN: reminders go out about a month and a week before expiry. A registrar may offer an Auto-Renew Grace Period of 1 to 45 days, during which the name may be auctioned by the registrar depending on its terms. After deletion registries must offer a 30-day Redemption Grace Period; then five days of pending delete; then the name is released first come, first served.', 'icann_errp_reg','icann_renewal_faq','icann_errp')}
{P('Nominet (.uk): 0 to 30 days Expiry Grace (the name works and can be renewed); 30 to 90 days Redemption Grace (does not resolve, renewable); 90 to 95 days Pending Delete (not renewable). Names no longer drop at random: each drops at a published UTC time, and a daily drop list is published. Drop catchers are told to use drop lists and EPP availability checks.', 'nominet_expiry')}
{P('Verisign (.com): 45 days Auto-Renew Grace and 30 days Redemption, per a registry agreement exhibit seen only in a search summary.', 'verisign_exhibit')}
{P('One registrar\'s explainer (for .com): auction houses list expired names between expiry and registry release; backorder services try to register a name the moment it is available, and several backorders on one name usually lead to an auction among them. The same registrar is reported to have stopped taking new backorders on 8 August 2025 (not confirmed on an opened page).', 'godaddy_expired','godaddy_backorder')}
<h2>Premium names</h2>
{P('One registrar explains two kinds: names owned by an existing holder (usually a one-time fee, renewal and transfer at standard rates) and registry premiums, which can carry special pricing for acquisition, renewal and transfer, and may be registered or renewed for one year at a time.', 'nc_premium')}
{gap('ICANN\'s own page on registry premium pricing: not found.')}
<h2>Risks</h2>
{P('Attackers may try to hijack a domain: the UK NCSC advises using an organisation-controlled registrar account and securing it as it advises for accounts. The NCSC page does not mention scams or fake renewal notices.', 'ncsc_protect')}
{P('The Swiss national cyber security centre describes fake messages of the form "someone wants your domain, register it now" and criminals catching lapsed domains, from search snippets only.', 'ncsc_ch')}
<h2>Disputes</h2>
{P('If someone holds a name that matches your trademark, the UDRP is the ICANN route: the complainant must show the name is identical or confusingly similar to a mark, that the holder has no rights or legitimate interests, and bad-faith registration and use. The only remedies are cancellation or transfer.', 'icann_udrp')}
{P('For .uk the equivalent is Nominet\'s Dispute Resolution Service (a complainant needs rights in a similar name and must show an abusive registration), from a search summary because Nominet\'s pages returned 403. Fees: not stated.', 'nominet_drs')}
'''

# ---------- TRANSFERS ----------
def transfers():
    life = table('Expiry lifecycle: ICANN gTLDs and Nominet .uk', ['Stage', 'gTLD (ICANN policy)', '.uk (Nominet)'],
     [[td('After expiry, name still works', True), td(f'Optional Auto-Renew Grace Period of 1 to 45 days, set by the registrar. {cite("icann_errp_reg")}'), td(f'Expiry Grace: 0 to 30 days, renewable. {cite("nominet_expiry")}')],
      [td('Name stops resolving, can be restored', True), td(f'Redemption Grace Period: 30 days; the registry disables DNS and prohibits transfers. {cite("icann_errp")}'), td(f'Redemption Grace: 30 to 90 days, does not resolve, renewable. {cite("nominet_expiry")}')],
      [td('Final hold', True), td(f'Pending Delete: 5 days, then released. {cite("icann_renewal_faq")}'), td(f'Pending Delete: 90 to 95 days, not renewable, fixed drop time. {cite("nominet_expiry")}')],
      [td('Released', True), td('First come, first served.'), td('At a published drop time; a daily drop list is published.')]])
    return f'''{h1('Transfers, locks, renewals, DNSSEC and privacy')}
{lead('The rules that decide whether you can move a domain, and what happens if you forget to renew it.')}
<h2>Transfers, auth codes and the 60-day rules</h2>
{P('ICANN\'s Transfer Policy (updated 21 February 2024; implementation required by 21 August 2025) applies to gTLDs.', 'icann_transfer')}
<ul>
<li>After a change of registrant, the registrar "must impose a 60-day inter-registrar transfer lock", though the holder may be allowed to opt out before the change request. {cite('icann_transfer')}</li>
<li>After first registration there is no mandatory lock, but a registrar of record may deny a transfer requested within 60 days of the creation date. A separate 60-day denial ground applies after an inter-registrar transfer. {cite('icann_transfer')}</li>
<li>The auth code is unique per domain and only identifies the holder; the transfer still needs the process authorisation. If there is no self-service, the registrar must provide the code or remove the transfer lock within five calendar days of the request. {cite('icann_transfer')}</li>
<li>A registrar must not use transfer processes "as a mechanism to secure payment", with exceptions for non-payment after expiry or for the current period. {cite('icann_transfer')}</li>
</ul>
<h2>The .uk change on 9 February 2027</h2>
{P('Nominet says the move from the IPS tag change process to Transfer Authorisation Codes will take place on Tuesday 9 February 2027, that a TAC is valid for 14 days, and that "accreditation" replaces "TAGs". Until then the tag-change process is current.', 'nominet_faq')}
{gap('.eu and .pt transfer rules, auth code validity and fees: not stated by any registry page we read. A registrar page (Gandi) gives some notes, shown on <a href="/registrars/gandi/">its entry</a>.')}
<h2>Renewals, grace periods and redemption</h2>
{life}
{P('Renewal notices: ICANN requires a reminder about a month before expiry and another about a week before, and a further notice if the name is not renewed or deleted within five days after expiry. DNS must be interrupted for at least the last eight days a name is renewable. Fees for renewal and redemption must be made reasonably available.', 'icann_errp','icann_errp_reg')}
<h2>DNSSEC</h2>
{P('"DNSSEC strengthens DNS authentication using digital signatures based on public key cryptography." The key material goes to the parent zone, and "in most cases, that communication happens through the zone owner\'s registrar." Whether a registrar supports it, and automates it, is a column on the <a href="/registrars/">comparison</a>.', 'icann_dnssec')}
<h2>Privacy and WHOIS</h2>
{P('Since the 2018 Temporary Specification, personal data in public registration data has been redacted; the Registration Data Policy published 21 February 2024 lets a registrar redact where a registrant does not consent to publication. Third-party "privacy services" are a separate, registrar-specific product, compared on the registrars page.', 'icann_regdata')}
'''

# ---------- CHOOSING ----------
def choosing():
    return f'''{h1('Choosing for customers')}
{lead('When you register a domain for someone else, the main decision is who the registrant is. The rest follows from it.')}
{note('This page is our advice for agencies and developers. It is not a quoted source, except where a source is cited.')}
<h2>Who should own the domain</h2>
<p>Make the <strong>customer the registrant</strong>, with their own name or organisation and a contact address they control. You act as the technical or administrative contact, or hold a delegated login. The reasons are in the sources:</p>
<ul>
<li>The registrant is the party the transfer rules treat as holder. A change of registrant triggers a confirmation process and, by default, a 60-day transfer lock, so putting the right name on the registration at the start avoids the lock later. {cite('icann_transfer')}</li>
<li>The auth code identifies the holder, and the registrar must provide it within five calendar days or remove the transfer lock. A customer who is the registrant can move away from you. {cite('icann_transfer')}</li>
<li>The UK NCSC advises an organisation-controlled registrar account secured with good account practice, because attackers may try to hijack a domain. {cite('ncsc_protect')}</li>
</ul>
<h2>Access</h2>
<ul>
<li>Prefer a registrar that lets the customer keep an account and grant you access, or an API key scoped to your work. Compare the "account security" and "bulk and reseller" columns on the <a href="/registrars/">registrars page</a>.</li>
<li>Where you hold the account yourself, keep one account per customer or a clear record of which names belong to whom, and make sure the customer can obtain an auth code within the five-day rule.</li>
<li>Use two-factor authentication on every registrar account and turn the registrar lock on. Which registrars offer these is on the comparison, each with its source.</li>
</ul>
<h2>Records to keep</h2>
<ul>
<li>Domain, registrar, account used, registration and expiry dates, and where the auth code is stored (never in plain email).</li>
<li>Registrant name, organisation and the email on the registration. ICANN says registrars must publish a registrant email, often a web form or pseudonymised address, so check which is shown. {cite('icann_webforms')}</li>
<li>Nameservers, DNSSEC state and DS records if you enable it. {cite('icann_dnssec')}</li>
<li>Renewal arrangements: who pays, whether auto-renew is on, and which email receives reminders. ICANN requires reminders about a month and a week before expiry. {cite('icann_errp')}</li>
<li>The customer's written agreement that they are the owner.</li>
</ul>
<h2>Checklist: registering a domain on someone's behalf</h2>
<ol class="check">
<li>Check the name is free (registrar search or RDAP lookup); if it is taken, see <a href="/aftermarket/">the aftermarket</a>.</li>
<li>Confirm the registrar supports the extension you need (.uk, .eu and .pt vary: .eu eligibility conditions are noted at several registrars; read the notes on each entry).</li>
<li>Read the first-year price against the renewal price and the transfer price, in the vendor's currency, and note whether tax is included.</li>
<li>Enter the customer as registrant, with a role mailbox they control.</li>
<li>Turn on two-factor authentication and the registrar lock.</li>
<li>Turn on DNSSEC if your DNS provider and registrar support it together.</li>
<li>Switch on auto-renew, or diarise the expiry and reminder emails.</li>
<li>Record the details above and give the customer a copy.</li>
<li>Note the transfer rules: 60 days after a change of registrant, and for .uk the tag change until 9 February 2027, then TACs. {cite('icann_transfer','nominet_faq')}</li>
</ol>
'''
