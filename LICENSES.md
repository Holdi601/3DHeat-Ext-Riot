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

3DHeat Riot is not affiliated with or endorsed by Riot Games. League of Legends,
VALORANT and related names and trademarks belong to their owners. This
repository holds **no Riot assets** - no game file, art, model, map, sound, logo
or data of the games - and no replay or anything read from one. The tool reads
the user's own `.rofl` and `.vrf` replay files, on the user's own machine, and
what it writes stays there.

It reads **only the unencrypted parts of each file**: a `.rofl`'s plain JSON
metadata (the end-of-game box score), its header and chunk table; a `.vrf`'s
info block, header facts and event chunks. It **breaks no encryption and does no
deobfuscation**: it contains no key, no decryption and no code taken from the
games. The encrypted parts are named by their byte range and left unread. The
tool talks to no server; the match timeline from Riot's Match-V5 API, which the
3DHeat Watcher can fetch, is fetched with the user's own Riot developer key and
is not part of this tool. Rights holders: open an issue at
[3DHeat-Ext-Riot/issues](https://github.com/Holdi601/3DHeat-Ext-Riot/issues) -
we respond quickly and remove anything on request. See [Terms and
licence](https://holdi601.github.io/3DHeat-Ext-Riot/terms.html).
