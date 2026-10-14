# Rogue guarded private browser follow-up

Catalog **89**; strict additional-decompilation milestone **4/5**. Rogue remains an unpublished developer-source-port lead. This follow-up advances the [initial private source audit](rogue-source-intake-2026-10-14.md); its earlier receipts remain historical.

The pinned raw source snapshot is unchanged. The current build selects **30 unchanged game C units, one derived BSD save implementation, and three authored units**. The derived `state.c` fixes an array overrun in the daemon loader and explicitly serializes/restores room, passage and null references. The independent platform input wait preserves the last explicitly refreshed window: its previous implicit main-screen redraw erased an inventory display after a combat message. The v3 failure and v4 correction were both retained privately. No actor, HP, object or RNG state was injected by gameplay tests.

## Measured native behavior

Normal keyboard routes passed native movement, enemy damage, a defeated enemy, inventory after combat, death and fresh retry. Native S/y produced a **39,236-byte** save; a full browser restart restored position, HP/max HP, depth, gold, experience, food, inventory and observed monsters. The browser removes its checkpoint only after successful native restoration reaches input wait, so the old retained-copy behavior is closed for the tested path. Stop exits the native runtime and freezes display/input, both at normal input wait and when requested while the WASM download is held. Simulated window blur/focus checks confirm ignored input while unfocused and resumed native turns after focus; physical app switching is not certified.

The bounded independent format reader checks sizes, exact marker/count fields, terminated text, object and dice formats, coordinates, array indices, daemon function IDs, map/monster/room references, window data and exact end-of-file before native restore. It rejected **894 malformed native cases** against the latest accepted sample. Five malformed browser envelopes were rejected with zero native display frames and no restore file written. These are tested format/bounds controls, not an exhaustive valid-state or security certificate.

All browser tests blocked audio constructors and used muted Edge contexts. Audio-constructor calls were zero. Every test context and server closed. Audible playback remains unavailable/unverified. The ordinary original game remains much larger than the measured path; no dungeon playthrough is claimed.

## Independent content and release gates

A separate **95-character CC0** glyph component now covers printable ASCII using the project's own block-font family plus independently authored punctuation/game symbols. [Font provenance](../experiments/rogue-browser/font-provenance.json) and the content dedication cover only that component. It is not integrated or visually accepted. Original licensed prose, names and procedural dungeon content remain in the private probe; the full independently authored edition and its objectives are not complete.

Exact linked SDK members, emitted JavaScript and header notices, portable source replay, broader authored-course saves/objectives, loading/site and production acceptance remain open. No runtime/source upload, new catalog entry or deployment occurred. Mario Party 2/3, Halo and private ROM history remain untouched.

[Checkpoint and payload hashes](rogue-guarded-checkpoint-2026-10-14.json), [save/restart](rogue-guarded-save-2026-10-14.json), [combat/death/retry](rogue-guarded-combat-2026-10-14.json), [malformed native cases](rogue-guarded-validation-2026-10-14.json), [browser rejection](rogue-guarded-invalidCheckpoints-2026-10-14.json), [focus and Stop](rogue-guarded-controls-2026-10-14.json).
