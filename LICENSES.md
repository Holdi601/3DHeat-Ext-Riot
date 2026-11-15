# Third-party licences

This tool is MIT licensed ([`LICENSE`](LICENSE)) and needs nothing but Python's
standard library. What it uses, and under which licence; each project's own
source is what counts, not this file.

| Software | Licence | How it is used |
|---|---|---|
| pytest | MIT | development only: the tests |
| roflxd.cs | MIT | consulted for facts only: the layout of a `.rofl` file's open header, metadata and chunk table; no code copied |
| vrfkit | Apache-2.0 | consulted for facts only: the container layout of a `.vrf` file; no code copied |
| ValorantReplayParser | MIT | consulted for facts only: the same layout; no code copied |

## What it reads, and what it does not

League of Legends and VALORANT belong to Riot Games. This repository holds no
replay and nothing read from one; the tool reads replay files on the user's
own machine, and what it writes stays there.

It reads **only what each file carries in the open**: a `.rofl`'s plain JSON
metadata (the end-of-game box score), its header and chunk table; a `.vrf`'s
info block, header facts and event chunks. It **breaks no encryption and
undoes no obfuscation**: the game data inside the replays is encrypted and
obfuscated against cheating, and getting through that would mean taking the
game client apart, which Riot's Terms of Service forbid (3.1, 7.1). Those parts
are named by their byte range and left unread. The tool talks to no server; the
match timeline from Riot's Match-V5 API, which the 3DHeat Watcher can fetch, is
fetched with the user's own Riot developer key and is not part of this tool.
See [Terms and licence](https://holdi601.github.io/3DHeat-Ext-Riot/terms.html).
