# Rogue private browser compatibility probe

This is an unpublished developer-source-port lead, not a decompilation or a catalog addition. The pinned game grant names the original authors; the save/crypt notices are separate. No clean-room isolation is certified.

Source: `Davidslv/rogue` at `f4653c2a2ee6981a73abe9dfda055134285e1e79`. The private raw-text snapshot is under `D:/n64work/rogue-intake-2026-10-14`. No game archive, executable, PNG, ROM or audio was downloaded.

`build-probe.py` compiles 31 unchanged original C units with three independently authored units. `mdport.c` and `xcrypt.c` are excluded. `wizard.c` contains ordinary identification/teleport routines needed by the game; the `MASTER` cheat configuration is **not** enabled. The browser platform provides single-user filesystem access, terminal windows and asynchronous keyboard reads. Desktop process/signal/shell behavior is unavailable. No ncurses implementation or header was copied.

The Emscripten 6.0.10 probe uses `-fwrapv` for the old RNG's signed arithmetic and `EMULATE_FUNCTION_POINTER_CASTS` for old-C callbacks. The first movement originally trapped without the latter. Compiler warnings remain in unchanged old-C declarations; unresolved symbols are not allowed. Build logs are private. This build is not an exact linked-object/emitted-JavaScript license audit.

Reproduce the private text snapshot with `python -X utf8 experiments/rogue-browser/fetch-source.py`; it downloads only exact hash-checked text paths and refuses mismatched existing files. Run `python -X utf8 experiments/rogue-browser/build-probe.py`, then the bundled Node runtime with `experiments/rogue-browser/test-probe.cjs`. The test reads only native state; it uses keyboard movement, inventory and the native S/y save command. The latest scoped pass used two normal moves, inventory, a 39,065-byte native save and a complete browser restart with equal position, health, depth, gold, experience, food, inventory and monster state. It blocked audio constructors and closed both browser contexts/server. It is not a full dungeon playthrough.

The probe retains licensed original strings and procedural content, and temporarily displays through a system monospace font. It is not the user's requested independent-content edition. There is no public runtime, source archive, catalog entry, upload or deployment.

Remaining gates: independent text/font/content provenance; an authored challenge with ordinary objectives, combat/death/retry and completion; inventory/message transitions during combat; full terminal overlay/subwindow semantics; strict validation of the legacy native save parser; persistence lifecycle (restore consumes the native file but this prototype retains its local-storage copy); focus/Stop/disposal; actual SDK archive members, emitted JS/header notices; reproducible portable source archive; site and production verification.

Earlier failed HTTP-path, memory-view, callback-signature and inventory assertions are preserved privately. The twelve-movement run's inventory assertion failed after enemy damage and remains a broader message/display follow-up; the passing two-movement result does not erase it. There is no audio code in this host; audible playback remains unavailable/unverified.
