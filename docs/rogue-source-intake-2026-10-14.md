# Rogue 5.4.4 — private source-port compatibility

Catalog **89**. Rogue is a nonduplicate developer-source-port lead, **not a new decompilation**, emulator or clean-room certification. The strict additional-decompilation milestone remains **4/5**. Vector Duel's released receipt remains [current](vector-duel-release.json); the older catalog-88 reconciliation is a historical snapshot.

Reviewed [Davidslv/rogue](https://github.com/Davidslv/rogue/tree/f4653c2a2ee6981a73abe9dfda055134285e1e79) at `f4653c2a2ee6981a73abe9dfda055134285e1e79`, 548 stars at this audit. Its [BSD-style notices](https://github.com/Davidslv/rogue/blob/f4653c2a2ee6981a73abe9dfda055134285e1e79/LICENSE.TXT) name original authors Michael Toy, Ken Arnold and Glenn Wichman, with separate Nicholas Kisseberth save/platform and David Burren crypt notices. This is stronger provenance than a contributor-only reconstruction label, although this mirror does not itself prove the author's release history. The selected source retains the original game grant and separate save implementation notice; no independent release-history certificate is claimed. Its archive-maintenance README does not make the maintainer an original author.

The text-only snapshot inventories 48 raw files, 520,760 bytes, with unchanged SHA-256 hashes. Media and executable entries were excluded. No retail resource, ROM or original game binary was fetched. The desktop recipe uses terminal curses; its own code contains gameplay prose, names and procedural dungeon generation, so absence of separate data files does not imply absence of expressive content.

## Private engineering result

An independently authored terminal/single-user browser adapter links 31 unchanged game C units plus three authored units to WASM. The selected configuration excludes original desktop `mdport.c`, crypt `xcrypt.c`, ncurses and `MASTER` cheat mode. Ordinary identification/teleport functions in `wizard.c` are required, so that file remains selected. Emscripten's function-pointer compatibility option resolves old-C callbacks; `-fwrapv` preserves signed RNG arithmetic. Original prototype warnings remain. There is no unresolved-symbol allowance or gameplay stub. Exact extracted SDK members, emitted JavaScript and header-notice closure are still unaudited; SDK linker search arguments alone do not establish selected dependencies.

The muted private pass demonstrates two normal keyboard moves and native food consumption, inventory display, the native S/y save and full browser restart. Position, HP, maximum HP, depth, gold, experience, food, inventory and all observed monsters match the checkpoint. The save contains **39,065 bytes**. The observer reads game state; it does not set actors, health, objects or RNG. Audio-constructor calls were zero and both players/server closed. This is scoped browser compatibility, not dungeon completion or release acceptance.

## Precise release gates

The private probe still contains licensed original prose/procedural content and uses a system monospace font. An independently authored content edition with a provenance manifest is not complete. Broader combat/death/retry/finish, message and inventory transitions, terminal overlays, strict legacy-save validation, persistence lifecycle, focus and Stop/disposal remain open. The twelve-movement inventory assertion failed after enemy damage; its receipt is retained, and the passing shorter run does not clear that wider case. The prototype also keeps a local-storage copy after native restore consumes the filesystem save, so its final persistence policy is not ready.

Complete dependency notices, a portable source-only replay package, loading-failure tests, catalog integration and production tests remain required. No runtime/source upload, new catalog entry or deployment occurred. No audible test occurred. Mario Party 2/3, Halo and private ROM history remain untouched.

[Raw snapshot hashes](rogue-source-snapshot-2026-10-14.json), [private browser receipt](rogue-private-browser-2026-10-14.json), [checkpoint](rogue-intake-checkpoint-2026-10-14.json), [adapter notes](../experiments/rogue-browser/README.md).
