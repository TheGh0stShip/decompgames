# Open Paths authored campaign — October 14, 2026

The unchanged live package passed all six independently authored navigation levels using normal menu clicks and 356 arrow-key moves. The engine wrote six Completed states and its all-levels-completed flag. Those same values survived a full browser close and a new browser process using the isolated test profile.

The [receipt](open-paths-campaign-production-test-2026-10-14.json) records per-level progress, restart results, package hashes, diagnostics and private evidence hashes. This covers the complete six-level CC0 replacement campaign. It does not cover the original retail campaign or its excluded collectibles, hazards, enemies, music and sound effects.

| Level | Keyboard moves | Native completion states after exit | All-levels flag |
|---|---:|---|---:|
| 1 | 2 | 1, 0, 0, 0, 0, 0 | 0 |
| 2 | 82 | 1, 1, 0, 0, 0, 0 | 0 |
| 3 | 50 | 1, 1, 1, 0, 0, 0 | 0 |
| 4 | 70 | 1, 1, 1, 1, 0, 0 | 0 |
| 5 | 70 | 1, 1, 1, 1, 1, 0 | 0 |
| 6 | 82 | 1, 1, 1, 1, 1, 1 | 1 |

The test read the engine-written PLAYER.LST without modifying game memory, save data, scores or random state. The published source defines Completed as 1 and Skipped as 2; all six recorded states are Completed. Although its struct comment retains uncertainty about the last byte, `updateHallOfFameEntries()` sets `completedAllLevels` to 1 only after counting all six Completed states. The synthetic player started with six zero states. The loaded LEVELS.DAT matched the published hash, and each planned route matched its authored level chunk. Selected campaign, level-six and restart canvases were visually reviewed; actual native completion values support the completion claim.

The package remains `bad56a4e174e-026301f2dd`, from source revision `bad56a4e174e628643995284ea55d4c49af3137c`. Fresh HTTP downloads of both runtime files, all 14 allowlisted replacement assets and the corresponding-source archive matched all 17 recorded byte lengths and SHA-256 hashes. Runtime WASM remains `8bde797a8c381d8436d4cdada2703734bbc4c691a325c21290d68fac2ef4eaa5`; LEVELS.DAT remains `42129a281b05dd82f4fd1d1fe489e42d30a1f9e986a248b0b869affdba609e38`. No runtime or source upload is needed.

Both accepted sessions used headless Microsoft Edge on Windows with `--mute-audio` and Sound: off. The existing build uses the null audio backend. There were no page errors, game console errors or missing resources. Three deliberately blocked site-analytics requests and their expected diagnostics per session are separate from game failures. Each session used the actual Stop game button, waited for local-save synchronization and closed its browser.

An initial harness trial missed Go after the canvas resized and stayed on the menu. Its failed receipt and screenshots were retained privately and excluded from accepted gameplay evidence. A fresh test profile and normalized menu coordinates corrected the harness. This was not a product gameplay failure.

September 22 backup export/delete/import restoration remains separate historical evidence; this pass did not repeat that cycle. Other browsers, touch devices, rapid-close durability and audible playback remain unverified. The existing GPL/MIT engine record and CC0 replacement-content scope are unchanged; this pass makes no new license or clean-room certification. Catalog 87 and the decompilation milestone 4/5 remain unchanged.
