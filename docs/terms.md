---
title: Terms and licence
nav_order: 8
---

# Terms and licence

## Riot's games and replays

3DHeat Riot is not affiliated with or endorsed by Riot Games. League of Legends,
VALORANT and related names and trademarks belong to their owners. This tool
ships no Riot assets - no game file, art, model, map, sound, logo or data of
either game - and talks to no server: it reads the replay files the games wrote
on your computer, outside the game, and changes nothing in it. What it writes
stays on your machine.

## What is read, and what never is

Both games protect what is inside their replays: the moment-to-moment game data
is encrypted and obfuscated, and differently with every patch, to keep it from
being used to cheat. This tool:

- reads **only what each file carries in the open** - a `.rofl`'s plain JSON
  metadata (the end-of-game box score), its header and chunk table; a `.vrf`'s
  info block, the map, match id and agents in its header, and the server's
  event chunks;
- **breaks no encryption and undoes no obfuscation**, and contains no key, no
  decryption and no code taken from the games;
- names the protected parts by their place in the file and leaves them unread.

A key the file itself stores in the open (a ROFL1 replay's chunk key) is
copied into the reading as it is stored, as part of the header; nothing is
decrypted with it.

## The Riot API key

The tool needs no account and no key. Positions of a League match come from
Riot's Match-V5 API, not from the file: the 3DHeat Watcher can fetch a match's
timeline with **your own** Riot developer key (a personal key is meant for
"showing (self) player stats"). That fetch is the Watcher's, it is off without
a key, and nothing is sent anywhere by this tool.

## Its own project

Each game reader is its own small project with its own licence file, releases
and issue tracker, so it can be installed, updated, maintained - or withdrawn on
a rights holder's request - on its own, without affecting the viewer or the
other tools.

Rights holders: open an issue at
[3DHeat-Ext-Riot/issues](https://github.com/Holdi601/3DHeat-Ext-Riot/issues) -
we respond quickly and remove anything on request.

## Licence and sources

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/LICENSE)).
Needs only Python's standard library; the tests need pytest (MIT). Written for
this project, first as part of the 3DHeat Watcher. The file layouts were taken
as facts from roflxd.cs (MIT), vrfkit (Apache-2.0) and ValorantReplayParser
(MIT), and from a Riot engineer's description of ROFL2 (ReplayBook issue 299);
no code was copied. See
[`LICENSES.md`](https://github.com/Holdi601/3DHeat-Ext-Riot/blob/main/LICENSES.md).
