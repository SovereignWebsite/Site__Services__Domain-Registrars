"""The five design directions, their review rounds, and the picker page."""
from lib import esc

LIVE_DESIGN = 'd5'

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
ROUNDS = [
 ('Round 2 (25 Nov 2026): recommendation d5 Dashboard, with d4\'s margin sources', [
  'The review of round 1 came from a.design, account A\'s design reviewer. It recommended d5, because the comparison is what readers come back for, with d4\'s margin sources on wide screens. After the changes below, the keeper agrees, and the live pages now use d5. d1 was the keeper\'s provisional pick in round 1.',
  'Changed for every design: on a phone the long title becomes a short name and eight links become one Sections button; the web address kicker is gone; the first column of every table stays in view and a cue says the table scrolls sideways; the notes about reading prices are folded under one line instead of standing before the table.',
  'Changed per design: d1 and d4 are no longer twins on a phone (d4 sources become boxed notes, d1 keeps quiet italic lines); d3 gets a bar of sections fixed to the bottom of a phone; d5 now truly leads with the comparison and gains d4\'s margin sources on wide screens; d2 is kept as the developer option and is the hardest for newcomers.',
  'Still open: design.b was also asked for a review through a.maestro and has not answered yet. Dinis Cruz picks.']),
 ('Round 1 (25 Nov 2026): five directions', [
  'd1 Ledger, d2 Terminal, d3 Atlas, d4 Field Notes and d5 Dashboard, built from the same pages and sources. The keeper\'s provisional pick was d1. a.design found, worst first: the five were one layout on a phone; the comparison table hid .uk, .eu and .pt off screen with no cue; three notes stood before the table; d1 and d4 were near twins on a phone; d3\'s sidebar existed only on desktop; d2 is hardest for newcomers.']),
]

def picker_body(live):
    items = ''.join(f'<li><a href="/designs/{k}/"><img src="/assets/designs/thumbs/{k}.jpg" width="320" height="200" alt="Thumbnail of design {k}, {esc(d["name"])}: the home page">'
                    f'<span class="dt">{k}: {esc(d["name"])}{"<span class=rec>live, recommended</span>" if k == live else ""}</span><span class="dd">{esc(d["line"])} {esc(d["who"])}</span></a></li>' for k, d in DESIGNS.items())
    rounds = ''.join(f'<h3>{esc(h)}</h3>' + ''.join(f'<p>{p}</p>' for p in ps) for h, ps in ROUNDS)
    return f'''<div class="mark">Design</div><h1>Choose a design</h1>
<p class="lead">Five directions for this research and comparison site. Open each one, look at the comparison table, and tell Dinis Cruz which number to keep. The live pages stay on {esc(live)} until the pick is made.</p>
<ul class="design-grid">{items}</ul>
<h2>How to choose</h2>
<p>Each preview is the whole site in that design, with its links kept inside the preview. Check three things: can you read the explanation pages comfortably, can you compare registrars without losing the column headings, and does it work at phone width and in light and dark. Then say "keep d2", for example. Nothing on this page records a choice, and it uses no cookies or scripts.</p>
<h2>Design rounds</h2>
{rounds or '<p>Round 1 is out for review. Notes appear here after each round.</p>'}'''
