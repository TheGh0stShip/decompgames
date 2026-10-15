# Open Cadet native launch-skill bonus

The unchanged live game produced a **7,500-point launch-skill bonus during unpaused keyboard play**. The [direct canvas screenshot](open-cadet-skill-shot-unpaused-2026-10-14.png) visibly shows LAUNCH SKILL BONUS and score 7500. A separate read-only debugger run paired the native award call with a **0 → 30,000** score change and its corresponding message. [Machine-readable receipt](open-cadet-skill-shot-production-test-2026-10-14.json).

These are two different runs and amounts. The unpaused case confirms an ordinary-play bonus; the debugger case establishes the native score transition within debugger timing limits. Neither establishes a reliably repeatable plunger hold, calibrated physics, a completed mission or a full table playthrough. This verifies the existing entry; catalog **90** and the additional-decompilation milestone **4/5** remain unchanged.

## Unpaused production case

A fresh isolated headless Edge context opened the canonical player with `--mute-audio` and confirmed Sound: off. Ordinary F2, a 1,700 ms wait, Space held for 900 ms and release were followed by read-only scanning for the runtime-formatted bonus message. The observer rejects the static `%ld` format and only accepts a positive numeric message; it neither invokes game functions nor modifies game memory, saves, RNG, actors or physics.

The formatted message `Launch skill bonus` with amount 7500 was observed about 5.8 seconds after release. The immediate native-canvas screenshot was visually inspected and confirms the message and score. Stop game acknowledged save synchronization, then the context and browser closed. There were no page errors or missing game resources. Site analytics were deliberately blocked and recorded separately. This is one accepted unpaused case, not deterministic timing advice.

An earlier 650 ms unpaused attempt showed only ready/zero-score frames. A subsequent portable-harness candidate did not observe a bonus at 900, 1100 or 1300 ms and then encountered a navigation timeout. Those reports and screenshots remain private; they are not claimed as a stable regression pass or as evidence that the bonus is absent. No flaky automated acceptance test was added to the repository's test suite.

## Native score pairing

The published source archive, SHA-256 `33d4502ff6f3d8023b0248b9fff68c2a1f709a12cee9584625618be658f04a42`, was freshly extracted. All 68 selected C++ units and resources were rebuilt unchanged with the published recipe and Emscripten 6.0.10, adding only `--emit-symbol-map`. The resulting WASM and the live debugger's original module both hash to the published `06edc08c83025f2de2d7024111186a2ebf8059081f929c17eb4ca554e243d891`.

The exact map identifies `TPinballTable::AddScore(int)` as function 1654 and the launch-skill controller `DeploymentChuteToEscapeChuteOneWayControl` as 268. At the AddScore entry, the debugger read its table pointer, requested 30000 points and current score 0. Stepping out returned to that controller with score 30000. The later native text-box call carried the matching launch-skill message. Incoming collision stack frames identify ordinary ball/one-way geometry contact. The receipt preserves all offsets and stack/state pairs.

The score-field offset 84 came from a separate LLVM-only query compiled with the same headers/toolchain. That query was never linked into the game. CDP's wrapped WebAssembly scalar values were unwrapped before reading parameters; earlier observer attempts that omitted this step are not negative gameplay evidence. A first harness also opened the guide rather than the player and produced no gameplay evidence. All corrected and failed attempts closed their browser contexts.

This run used ordinary F2 and Space inputs; the accepted award occurred during the 650 ms attempt after the native ball-feed wait. Debugger pauses affect scheduling and plunger timing. It must not be conflated with the unpaused 900 ms / 7500 case, or used to claim timing equivalence.

## Preserved limits

All missions, remaining objectives, every collision state/device, full playthrough, rapid-close save durability and audible audio remain unverified. No new code-license, asset-provenance or clean-room certification follows from gameplay. Runtime/source bytes and all other game entries remain unchanged. Mario Party 2/3, Halo and prior private ROM research were untouched. Backlog/test-log records were byte-appended; unrelated local history was not staged.
