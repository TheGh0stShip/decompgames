# Open Cadet native flipper contacts — October 14, 2026

A private instrumented build of the published Open Cadet source recorded 25 native ball/flipper contacts during ordinary keyboard play. Four contacts applied a positive native boost across both flipper components, and all 25 changed the observed velocity vector. This expands source-build physics coverage. It does not certify contact behavior in the exact production binary; the public manifest's production-contact limitation remains unchanged.

The [receipt](open-cadet-native-contact-probe-2026-10-14.json) contains build hashes, the observer source and insertion locations, per-component counts and all four positive-boost observations. The base is the currently published [corresponding source archive](https://decompgames.com/sources/cadet-0bc12d3ca97a-authored-c51f8473a6.tar.gz), SHA-256 `33d4502ff6f3d8023b0248b9fff68c2a1f709a12cee9584625618be658f04a42`, 1,489,466 bytes and 242 package files. Extraction paths were checked to remain within the private test directory; archive files were hashed before changes.

Only `SpaceCadetPinball/TFlipperEdge.cpp` received observer insertions. The observer copies incoming ball state on entry, records the existing computed boost and reads outgoing state after the original collision code returns. Its writes affect only its own local record and a separate browser event list. It never changes the ball, score, random seed, saves, collision geometry or simulation settings. Removing the three observer insertions restores the original file byte for byte; all other archive input files are unchanged. The original collision file SHA-256 is `2bc2b966b11da254c3202ff6a9faace016d2fa7abf53ebaebd8b8abc61ccf9cf`.

The unmodified published build flags compiled all 68 selected game units using installed Emscripten 6.0.10 (`d6c521a7f05449857c76bd99e396895583cf2083`). The native `TFlipperEdge::EdgeCollision` and `maths::basic_collision` implementations retain their original control flow and physics calculations. The probe's 1,431,942-byte asset data is byte-identical to the current public manifest. JavaScript and WASM differ because they contain the private observer; neither was uploaded or substituted in a playable release.

The fresh isolated Edge session used `--mute-audio` and the site's AudioNode master-gain gate fixed at zero before engine startup. A local-only host served the probe. An initial pre-launch Z/slash press recorded no contacts. Normal F2/Space launch followed by 95 Z/slash press/release pulses produced the observations below, without invoking an engine state setter or editing game memory.

| Native component | Contacts | Positive boosts | Representative speed before → after |
|---|---:|---:|---|
| `a_flip1` | 21 | 3 | 7.069548 → 18.560257 |
| `a_flip2` | 4 | 1 | 5.193358 → 12.811914 |

All four positive-boost events occurred with native motion flag 1 and collision flags 1/0. The other two `a_flip1` events changed speed from 0.815452 to 9.032930 and 0.875300 to 8.730570. Every logged position, direction, speed and boost value was finite. These are internal engine units; no calibrated real-world force or exact timing equivalence with production is claimed. The final canvas was visually inspected, but event records—not a static image—support the collision claim.

The passing run has no page errors, console errors, missing requests or external requests. Keys were released and the browser/player and local server closed in the harness's final cleanup. Audio quality, full objectives, collision behavior across other browsers and an uninstrumented-production contact trace remain unverified. Earlier live visual-control and earned-score/persistence evidence is preserved separately and was not retested here.

The first observer attempted 17 JavaScript callback fields; its final field was undefined and the first collision stopped that private simulation. Its report, build hashes and screenshots are preserved privately, and it is excluded from accepted gameplay evidence. The corrected observer uses 15 fields, verified in generated JavaScript before rerunning. An initial Windows compiler-launch path also failed before compilation and was corrected to invoke the installed Python compiler entry point. These were test-harness failures; the public runtime was unchanged throughout.

No catalog entry, public runtime/source archive, manifest, protected game or private ROM record changed. Catalog 87 and the actual-decompilation milestone 4/5 remain unchanged. This publication is a documentation-only source-build checkpoint.

A later same-day [production contact test](open-cadet-contacts-production-test-2026-10-14.md) observes the unchanged live WASM with read-only debugger stepping. It supersedes the production-contact gap stated at this earlier checkpoint, within its separate timing limits.
