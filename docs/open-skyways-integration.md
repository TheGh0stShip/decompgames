# Open Skyways integration and test record

Open Skyways pairs [skyroads-32x at `df219e03b854153291b32224593013b60d861d40`](https://github.com/haroldo-ok/skyroads-32x/tree/df219e03b854153291b32224593013b60d861d40) with 25 independently authored replacement files. Upstream describes its C engine as reconstructed from the game's disassembly; its [license](https://github.com/haroldo-ok/skyroads-32x/blob/df219e03b854153291b32224593013b60d861d40/LICENSE) grants MIT rights to that source, except the bundled Nuked OPL3 code under LGPL-2.1. Bluemoon's original executable, game data, artwork, and audio are not included. The replacement roads, menus, font, interface, HUD, objects, animation, and inert demo were authored by the Decomp Games generators and dedicated CC0-1.0. The one-byte intro-sample placeholder cannot be played; `MUZAX.LZS` and `SFX.SND` are absent. The compiled browser shell initializes SDL video only and does not open an audio device. Audible playback has not been tested or enabled.

Package ID `df219e03b854-59b1a2a61bd4` uses the upstream revision above, generator/recipe commit `0da835dd6bb284edf8fcaa652f02cf7954d944a3`, Python 3.13, Pillow 12.3.0, and Emscripten 6.0.1. Run the three `scripts/build-open-skyroads-{roads,visuals,support}.py` generators, then `scripts/build-open-skyroads-browser.py` with the pinned upstream checkout and their output directories. The private [CI build 36293441485](https://github.com/andrewnakas/decompgames/actions/runs/36293441485) compiled the package; the exact [recipe](../scripts/build-open-skyroads-browser.py) rejects any input besides those 25 named replacements. The reproducible [staged source/data archive](/sources/open-skyways-df219e03b854-59b1a2a61bd4.tar.gz) includes upstream source, its license, the null-audio and browser-save patches, all 25 replacements, and `build-record.json` with each input's byte size and SHA-256. The generators and [packaging script](../scripts/package-open-skyroads-source.py) remain in the repository.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `skyroads.js` | 180,656 | `260f9afe0edfc87ad0b25333956b6b2c8e94f25340852e3858cba98e5c1bd6e3` |
| `skyroads.wasm` | 685,541 | `d28ac44c6abf4188a575a119917a5d31909efe330c9f4d6bf190c79b83cc7cd3` |
| `skyroads.data` | 1,402,541 | `59b1a2a61bd46d813f5f7f8d5763c4c6ada53137ee865bf89cb08ccd0e5b3f37` |
| staged source/data archive | 68,279 | `0276af350558edc7e89b008fde9ce7f382ccc55dbfbefcb1ced544683e95cf85` |

In the local site player, press Enter through the intro, Play menu, and road chooser. Up accelerates, Down brakes, Left and Right steer, Space jumps, P pauses, and Escape returns to the chooser. A completed course saves a completion marker automatically to browser storage. The toolbar's Export saves, Delete saves, and Import saves controls offer a portable JSON backup. Browser storage can be cleared by the browser or user, so exported backups matter.

## Silent browser verification

The pinned private build in headless Microsoft Edge on Windows, with `--mute-audio` and all off-origin requests blocked, rendered title, menu, road chooser, Road 01 and HUD. Held Up reached the **Road Completed** screen. Separate Right and Space probes visibly changed the ship's horizontal position and height. IndexedDB contained a 66-byte config with Road 01 completion count 1; the completion marker remained after reload.

The exact local site player package was then tested in headless Edge with the same muted/off-origin restrictions. It launched Road 01, reached **Road Completed**, exported a JSON backup containing `/save/skyroads.cfg` with completion count 1, deleted the save and showed no marker, imported the backup, restarted, and showed the marker again. Screenshots are under ignored `test-results/open-skyroads-site/`. The test browser and development server were closed.

## Production release gate, September 27

The repository passed `pnpm check`, 23 `pnpm test` cases, `pnpm build`, and 2,084 local-link checks. The three runtime files and source archive were uploaded to the existing Cloudflare R2 bucket, and the site was deployed to [Decomp Games](https://decompgames.com/games/skyways/) and [the player](https://play.decompgames.com/play/skyways/). All four files fetched back through the production asset endpoint matched the byte sizes and SHA-256 values above; the WebAssembly response had `application/wasm`, byte ranges, and an immutable cache policy.

The exact uninstrumented production package passed the same silent Road 01 completion and save export/delete/import flow in a fresh headless Edge profile. The exported 66-byte config recorded one completion, the chooser marker disappeared after deletion, and it returned after importing and restarting. Off-origin Cloudflare analytics requests were blocked during the test; their failed fetches had no game effect. The test player was closed. This is verified addition **4 of 5**; it does not imply a full thirty-road playthrough.

Only Road 01 has a completed-course observation. The other 29 authored courses, full campaign progression, long-term balance, touch/gamepad support, and audible audio remain unverified. Replacement art is minimalist, with sparse perspective cues; the project does not claim to reproduce the original game's presentation.


## October 14 authored-campaign follow-up

The earlier one-road checkpoint above is historical. Muted normal-control production play now completed all thirty authored roads, reached The End and retained the exact native config after a complete browser close/relaunch. All 25 loaded replacements and four published runtime/source hashes matched. See [campaign evidence](open-skyways-campaign-production-test-2026-10-14.json). Original retail courses, exhaustive off-center collision/death cases, long-term balance, other devices/browsers and audible playback remain unverified. Runtime/license/classification and the 4/5 milestone are unchanged. Both players stopped with save synchronization and closed.
