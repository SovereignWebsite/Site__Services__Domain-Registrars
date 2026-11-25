"""The five design directions, their review rounds, and the picker page."""
from lib import esc

LIVE_DESIGN = 'd1'

DESIGNS = {
 'd1': dict(key='d1', name='Ledger', line='An editorial reference book: serif type, paper colours, ruled tables, one calm column.',
            who='Best for reading the explanations end to end and for printing.'),
 'd2': dict(key='d2', name='Terminal', line='Monospace, hard borders and prompt-style headings, for people who live in a shell.',
            who='Best for developers; the densest text, the least friendly to newcomers.'),
 'd3': dict(key='d3', name='Atlas', line='A guide with a map: a fixed sidebar of sections, coloured headings and rounded cards.',
            who='Best for finding your way around; the most app-like.'),
 'd4': dict(key='d4', name='Field Notes', line='A researcher\'s notebook: warm paper, with each source set in the margin beside its claim on wide screens.',
            who='Best for showing the evidence; sources are visible without clutter.'),
 'd5': dict(key='d5', name='Dashboard', line='Comparison first: full width, compact tables with sticky headers, status chips.',
            who='Best for the registrar comparison itself; the explanations are secondary.'),
}

# Review rounds: edited as the rounds happen. Each entry: (heading, paragraphs).
ROUNDS = []

def picker_body(live):
    items = ''.join(f'<li><a href="/designs/{k}/"><img src="/assets/designs/thumbs/{k}.jpg" width="640" height="400" alt="Thumbnail of design {k}, {esc(d["name"])}: the home page">'
                    f'<span class="dt">{k}: {esc(d["name"])}{"<span class=rec>live, recommended</span>" if k == live else ""}</span><span class="dd">{esc(d["line"])} {esc(d["who"])}</span></a></li>' for k, d in DESIGNS.items())
    rounds = ''.join(f'<h3>{esc(h)}</h3>' + ''.join(f'<p>{p}</p>' for p in ps) for h, ps in ROUNDS)
    return f'''<div class="mark">Design</div><h1>Choose a design</h1>
<p class="lead">Five directions for this research and comparison site. Open each one, look at the comparison table, and tell Dinis Cruz which number to keep. The live pages stay on {esc(live)} until the pick is made.</p>
<ul class="design-grid">{items}</ul>
<h2>How to choose</h2>
<p>Each preview is the whole site in that design, with its links kept inside the preview. Check three things: can you read the explanation pages comfortably, can you compare registrars without losing the column headings, and does it work at phone width and in light and dark. Then say "keep d2", for example. Nothing on this page records a choice, and it uses no cookies or scripts.</p>
<h2>Design rounds</h2>
{rounds or '<p>Round 1 is out for review. Notes appear here after each round.</p>'}'''
