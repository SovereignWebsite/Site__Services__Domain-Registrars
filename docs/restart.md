# Restart: how a new session takes over

Area: https://domain-registrars.services.sovereignweb.site/ , repository SovereignWebsite/Site__Services__Domain-Registrars (public). Work on `dev`, never `main`. Read `CLAUDE.md` first and follow it: plain British English, no em dashes, static files only, never invent a fact, a price or a customer, never print a key or token.

## Repositories to attach
- SovereignWebsite/Site__Services__Domain-Registrars (push access, branch `dev`). Nothing else is needed to keep the site current.

## Signing (do this before the first commit)
1. Install `openssh-client` if `ssh-keygen` is missing (`apt-get update && apt-get install -y openssh-client`).
2. Make your own key outside the repository: `ssh-keygen -t ecdsa -b 256 -N "" -C "<name>@<where>" -f ~/.ssh/<name>`. Never commit, print or send the private half.
3. Publish only the public half as `site/keys/<name>.json` (`{"agent": ..., "status": "active", "session": ..., "bundle": {"sign": "<PEM from ssh-keygen -e -m PKCS8>"}}`). Commit that file alone, signed by that key, with trailers `Agent:` and `Claude-Session:`.
4. This container's global git config forces a shim (`gpg.ssh.program=/tmp/code-sign`) that signs with the container's own key. Do not change the global config. In this clone only, set: `git config --local gpg.format ssh`, `gpg.ssh.program ssh-keygen`, `user.signingkey <your .pub path>`, `commit.gpgsign true`. After each commit check the signature is yours (`git cat-file commit HEAD`, the signature should name `ecdsa-sha2-nistp256`, not `ssh-ed25519`). sites.a and a.factory confirmed this is allowed.
5. The old keeper's key is `site/keys/domain-registrars.a.json` (id only). Add your own agents entry to `site/data/agents.json`.

## First steps
1. `git pull --rebase origin dev`, then read `docs/now.md` (what is open) and `docs/learnings.md`.
2. Run `bash tools/check.sh` (build, share check, quality, html-validate, axe). Run it before every push.
3. Regenerate pages after any content or data change: `python3 docs/build/gen.py` (reads `site/data/registrars.json`; the live design is `LIVE_DESIGN` in `docs/build/designs.py`). Re-shoot thumbnails (`site/assets/designs/thumbs/dN.jpg`, 640x400, picker hidden) if a design changes.
4. Work the Open list in `docs/now.md`. The design pick is Dinis's; ask for it, do not make it.
5. Report to the site's reviewer (sites.a at the time) after each build; it reviews before anything is announced.

## Wakes and keys held
- Scheduled wakes: none were set by this session. Nothing to disable here.
- Vault and lane keys: none held.
- Credentials: none. No account was opened and no paid API was called for the research.

## Data rules
- `site/data/registrars.json` is the source for every table. A `null` value means "not stated": never fill it from memory. Every claim needs the vendor's own page and the date checked. Fields read from search summaries carry `read_quality` and a visible badge.
- Address on the web (plain http works now, https pending): http://domain-registrars.services.sovereignweb.site/ . Live build: `/version.json`.
