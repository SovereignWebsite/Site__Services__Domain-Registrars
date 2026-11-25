# Learnings

- **Research agents give a thin first pass.** The first fetch of the registrar pages left most .uk, .eu, .pt, DNSSEC and security fields empty. A second, targeted pass filled many. Plan two passes and mark what stays empty.
- **A summarising fetch tool paraphrases.** Keep quotes short and mark anything that came only from a search summary ("Not read on the official page: from a search summary"). Several vendor pages (Namecheap, Nominet) returned 403 or 404; do not retry them, say "not stated".
- **Check cited links.** Seven source URLs returned 404 on the pipeline's link check. Keep them as plain text in `docs/build/badlinks.json`, never as links.
- **Never check a page over file://.** Root-relative stylesheets do not load, so the check is meaningless. Serve `site/` with `python3 -m http.server` and use a browser (Playwright).
- **CSS selectors: id versus class.** d5's "comparison first" order silently failed because the id was on the heading, not the section. Screenshot every layout you claim.
- **Cache.** Every stylesheet link carries `?v=<content hash>` (generated in `docs/build/lib.py`; `build.mjs` also adds hashes). Give every `<img>` width and height so it stays small with CSS blocked.
- **Picker while designs are open.** Standing rule from Dinis: the "Choose a design" picker with thumbnails goes at the top of every page. Thumbnails must be shot with the picker hidden, or they contain pickers.
- **Phones first.** One Sections button, a short name, sticky first table column and a swipe hint made the comparison readable at 390 px. Test overflow on every page at 390 px.
- **Do not commit compiled Python.** `docs/build/.gitignore` covers `__pycache__/`.
- **Run `bash tools/check.sh` before every push.** It matches the deploy. New pages need all 14 Open Graph and Twitter tags (copied by `lib.head`).
- **The share card.** Made with Playwright from a screenshot of our own comparison; no external script is needed.
