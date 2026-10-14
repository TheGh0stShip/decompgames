# Rogue private browser compatibility probe

This is an unpublished developer-source-port lead, not a decompilation or a catalog addition. The pinned game grant names the original authors; the save/crypt notices are separate. No clean-room isolation is certified.

Source: `Davidslv/rogue` at `f4653c2a2ee6981a73abe9dfda055134285e1e79`. The private raw-text snapshot is under `D:/n64work/rogue-intake-2026-10-14`. No game archive, executable, PNG, ROM or audio was downloaded.

The historical first probe compiled 31 unchanged original C units with three independently authored units. `mdport.c` and `xcrypt.c` are excluded. `wizard.c` contains ordinary identification/teleport routines needed by the game; the `MASTER` cheat configuration is **not** enabled. The browser platform provides single-user filesystem access, terminal windows and asynchronous keyboard reads. Desktop process/signal/shell behavior is unavailable. No ncurses implementation or header was copied.

The Emscripten 6.0.10 probe uses `-fwrapv` for the old RNG's signed arithmetic and `EMULATE_FUNCTION_POINTER_CASTS` for old-C callbacks. The first movement originally trapped without the latter. Compiler warnings remain in unchanged old-C declarations; unresolved symbols are not allowed. Build logs are private. This build is not an exact linked-object/emitted-JavaScript license audit.

Reproduce the private text snapshot with `python -X utf8 experiments/rogue-browser/fetch-source.py`; it downloads only exact hash-checked text paths and refuses mismatched existing files. Run `python -X utf8 experiments/rogue-browser/build-probe.py`, then the bundled Node runtime with `experiments/rogue-browser/test-probe.cjs`. The test reads only native state; it uses keyboard movement, inventory and the native S/y save command. The historical first scoped pass used two normal moves, inventory, a 39,065-byte native save and a complete browser restart with equal position, health, depth, gold, experience, food, inventory and monster state. It blocked audio constructors and closed both browser contexts/server. It is not a full dungeon playthrough.

The probe retains licensed original strings and procedural content, and temporarily displays through a system monospace font. It is not the user's requested independent-content edition. There is no public runtime, source archive, catalog entry, upload or deployment.

Remaining gates: independent text/font/content provenance; an authored challenge with ordinary objectives, combat/death/retry and completion; inventory/message transitions during combat; full terminal overlay/subwindow semantics; strict validation of the legacy native save parser; persistence lifecycle (restore consumes the native file but this prototype retains its local-storage copy); focus/Stop/disposal; actual SDK archive members, emitted JS/header notices; reproducible portable source archive; site and production verification.

Earlier failed HTTP-path, memory-view, callback-signature and inventory assertions are preserved privately. The twelve-movement run's inventory assertion failed after enemy damage and remains a broader message/display follow-up; the passing two-movement result does not erase it. There is no audio code in this host; audible playback remains unavailable/unverified.


## Guarded v4 follow-up

The current default build output is `D:/n64work/rogue-intake-2026-10-14/guarded-v4`. It compiles **30 unchanged native C units, one derived BSD `state.c`, and three authored units**. Use `ROGUE_BUILD` for a different private output directory. `ROGUE_GUARDED=0` is a historical comparison configuration, not accepted for release.

The guarded native copy moves the daemon null-slot reset inside its bounds and serializes room/passage/null references explicitly. Original raw files remain unchanged. The platform input wait no longer implicitly redraws `stdscr`, which previously erased an inventory window when a combat message had just been cleared. Native movement, combat and save algorithms are retained; the read-only map observer lets the test select ordinary key routes without changing native state.

`validate-save.js` checks size, exact counts and markers, terminated strings, indices, coordinates, object subtypes, dice formats, daemon references, map-to-monster/room consistency, window data and exact end-of-file before native restore. It parses the native byte codec using pinned BSD algorithm constants generated into a private save spec. `REFERENCE-SOURCE-LICENSE.txt` retains those notices. Build-bound browser envelopes reject stale or malformed data and consume a checkpoint only after native restoration reaches its first input wait. This is bounded compatibility validation, not a security certification or proof for every possible valid native state.

Current tests demonstrate combat damage, a defeated native monster, inventory after combat, death and fresh retry; native S/y save and full-browser state restoration; consumed checkpoint; simulated blur/focus input gating; native Stop at input wait and during a held WASM download; malformed byte-level and browser checkpoint rejection. All tests block audio constructors and close contexts/servers. The v3 inventory failures remain historical evidence; v4's input-adapter fix closes the demonstrated case. See the guarded follow-up receipt in `docs` for counts, hashes and limits.

A separate 95-character CC0 font component is generated by `author-font.py` with `font-provenance.json`; it has **not** been integrated into the renderer. It does not clear game prose/names/maps. The full independent-content edition, complete dungeon objectives, exact SDK/link/emitted-JS notices, portable source replay and site/production acceptance remain open. No public integration or deployment exists.
