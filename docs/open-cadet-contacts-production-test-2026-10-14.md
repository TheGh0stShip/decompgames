# Open Cadet live native contacts — October 14, 2026

The unchanged production WASM recorded eight paired native flipper-contact observations during muted keyboard play. All eight changed the ball's velocity vector; five increased speed by more than one internal unit, covering both flipper components. This closes the production-contact observation gap within read-only debugger stepping. It does not verify unpaused timing equivalence, calibrated forces, every contact case or a full playthrough.

The [receipt](open-cadet-contacts-production-test-2026-10-14.json) records source/build identity, ABI offsets, native function locations, all eight incoming/outgoing state pairs and cleanup. The earlier [private instrumented probe](open-cadet-native-contact-probe-2026-10-14.md) remains separate historical evidence; its modified module was not used here.

The published 1,489,466-byte source archive, SHA-256 `33d4502ff6f3d8023b0248b9fff68c2a1f709a12cee9584625618be658f04a42`, was freshly extracted without source changes. Its original recipe compiled all 68 game units with Emscripten 6.0.10, adding only `--emit-symbol-map`. The resulting WASM hash is exactly the published `06edc08c83025f2de2d7024111186a2ebf8059081f929c17eb4ca554e243d891`. The live debugger's original module bytecode independently has that same hash. No replacement, observer, code patch or modified asset package was served to the live player.

That exact symbol map identifies native function 1562 as `TFlipperEdge::EdgeCollision(TBall*, float)`, with executable entry at byte offset 736509. The debugger paused at its entry, read its original `this` and ball pointers, stepped out of the function and read the resulting ball state before resuming. Read-only memory expressions obtain the component name, position, normalized direction, speed and motion/collision flags. Field offsets were computed with the same compiler and published headers in a separate LLVM-only ABI query; that query was not linked or run in the game. No score, ball, save, random seed, physics setting or other game-state setter was used. Debugger pauses affect wall-clock timing, so these observations must not be described as ordinary uninterrupted real-time physics testing.

| Native component | Paired contacts | Speed increases over one unit | Representative speed before → after |
|---|---:|---:|---|
| `a_flip2` | 7 | 4 | 1.423592 → 9.469979 |
| `a_flip1` | 1 | 1 | 6.248901 → 13.149797 |

The three other `a_flip2` contacts reduced speed, consistent with observing multiple contact states rather than counting only gains. All logged state values were finite. Each speed-increase event occurred with native motion flag 1 and collision flags 1/0. These are internal engine units; no calibrated real-world force or exact coefficient validation is claimed.

The fresh isolated Edge session launched the canonical shared player with `--mute-audio`, confirmed Sound: off and used ordinary F2, Space, Z and slash keyboard input. A separate initial discovery run reached the same exact native entry, then resumed and closed its player; it is not counted among the eight paired observations. The accepted run has no page errors, game console errors or missing resources. Deliberately blocked Google/Cloudflare site analytics and their expected diagnostics are recorded separately. The final canvas was visually inspected, but native state pairs support the contact claim.

After collecting both components' speed increases, the test removed its breakpoint and disabled debugging, released all keys and used the actual Stop game button. The player acknowledged local-save synchronization before the browser closed. No audible audio test or new persistence, objective-completion or rapid-close durability test was performed. Earlier high-score, restart and visual-control records remain separate.

Only verification metadata and documentation are updated for publication. Public runtime/source bytes, all other game objects, protected entries and prior private ROM records are unchanged. Catalog 87 and the actual-decompilation milestone 4/5 remain unchanged.
