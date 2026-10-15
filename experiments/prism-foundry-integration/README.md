# Prism Foundry integration groundwork

Authored MIT animation/descriptor adapters and course-selection code for the Moon Child FE source-port experiment. A later private player now passes a muted three-course playthrough with all nine pickups, three gates and final victory, plus separate startup/control/retry/fall/Stop checks. **No new catalog entry or production release.** Save support and final source/dependency/distribution gates remain open. Interfaces and retained callers were inspected; this is not a clean-room certificate.

`animation.cpp` replaces `Classes/moonchild/anim.cpp`. It bounds forced frames against the actual frame count, handles null/empty sequences, rejects invalid sequence indices, and preserves ordinary forward/reverse stepping. `assets.cpp` replaces `Classes/moonchild/asset.cpp`: descriptor-validation failures leave the target lists empty, before newly parsed assets are committed. It retains actual native sprite construction and PCX decoding after checking the selected image profile.

This profile requires single-plane 8-bit RLE, zero origin, even width with no padded scanline, dimensions at most 2048×4096, a complete palette and no trailing bytes. Frame paths are limited to 80 characters because the retained `Cblitbuf` constructor uses a 100-byte diagnostic buffer. Descriptors are capped at 256 KiB, lines at 250 characters, frames per sequence at 100, concrete sequence slots at 21, total frames at 4096, sequence/animation definitions at 256 each and decoded sprite pixels at 16 MiB. This is a controlled authored-content profile, not a general PCX compatibility or arbitrary-input safety certificate.

`make-levels.py` generates CC0 course constants from the existing authored `campaign.json`. `FoundryConfigureLevels()` selects the three corresponding native `LEVEL_DESCR` entries and empties the other 17 runtime entries. The original boundary harness only checks descriptor selection; the later private player executes all three course initializers and the authored callbacks. All three checkpoint positions activate, each gate advances normally, and final victory is earned. Respawn at an activated checkpoint remains unverified. Original source-side tables and unused campaign routines have not all been purged or reviewed merely because the runtime descriptor selector exists.

```text
python build-bounds.py --base-build ADAPTED_88_UNIT_BUILD --pack AUTHORED_PACK --output NEW_OUTPUT_DIRECTORY --emscripten EMSCRIPTEN_DIRECTORY --em-config EMSCRIPTEN_CONFIG --node NODE_EXECUTABLE
```

The recipe verifies the pinned base text/overlays, authored-pack hashes and **85 exact retained native object hashes** against the earlier committed receipt. It compiles four new/test units with strict warnings for their own code, treats retained headers as system headers, rejects unresolved symbols and enables assertions/SAFE_HEAP at final link. It runs a Node-only boundary/configuration harness and replays the committed native-content harness with the two animation/descriptor units changed. No game Host, loop, video or audio is initialized. SAFE_HEAP is not a complete memory-safety or leak-proof certificate.

Tests accept the 21-slot/100-frame boundaries and four 4-MiB sprites at the aggregate limit; reject a fifth such sprite, 22 slots, 101 frames, malformed/missing content and other invalid cases; and compare all 265 actual native-decoded image/palette SHA-256 values during full content replay. See the [measured checkpoint](../../docs/prism-foundry-bounds-levels-2026-10-15.md). The old source-only and content-only receipts remain separate historical results. No runtime or complete source archive is published here.

## Private player recipe

```text
python build-player.py --base-build ADAPTED_88_UNIT_BUILD --pack AUTHORED_PACK --output NEW_OUTPUT_DIRECTORY --emscripten EMSCRIPTEN_DIRECTORY --em-config EMSCRIPTEN_CONFIG
node test-player.mjs PRIVATE_PLAYER_DIRECTORY
node test-player.mjs PRIVATE_PLAYER_DIRECTORY --route
```

The player recipe verifies the pinned source/overlays, exact pack allowlist and 83 retained native objects. Six changed/new units provide patched MC/Host/main, the two bounded adapters and authored level selection. It bypasses original movie/menu/progress flows, disables editor access, selects null audio and omits original palette/world presentation updates. It maps pickup bursts to authored content, uses fixed normal controls, and adds a campaign fall/respawn path through native `hoi_init`; the original collapse/rise animation is not exercised. Normal native actor movement, collision and pickup callbacks remain. Read-only state exports support test evidence; they do not move actors, grant pickups or advance courses.

The wrapper supplies Start/Stop. Stop asks the Host to end its loop and destroy native resources; the test observes `Ready` becoming false before removing the iframe, twice. The test launches headless Edge with `--mute-audio`, uses ordinary keyboard input and closes the browser/server in `finally`. The `--route` check is partial: two pickups and one gap fall in Assembly Floor, with both pickups retained after respawn. It is not a three-course playthrough. Save support is not implemented in this candidate.

The [private-player checkpoint](../../docs/prism-foundry-player-2026-10-15.md) records a removed original-water-animation crash and the remaining WebGL warning, dependency, source-content and release gates. A [later progression check](../../docs/prism-foundry-progression-2026-10-15.md) tests the readiness guard, cancellation during loading and earned three-course completion. Assertions/SAFE_HEAP at final link do not establish complete memory safety. No runtime is placed in the public game catalog by these recipes.

`test-player.mjs PRIVATE_PLAYER_DIRECTORY --loading-stop` delays the first WASM request, observes the pre-initialization state return `null`, cancels that player without calling native exports, then performs normal startup/control/retry and two native shutdown checks. `test-campaign.mjs PRIVATE_PLAYER_DIRECTORY` attempts all courses using ordinary keyboard input and read-only observations. The report distinguishes completed courses from an unsuccessful full attempt; `--first-only` limits it to the first gate. Both wrappers are guarded by actual runtime initialization, not merely the existence of Emscripten export stubs. Cancellation during loading is labeled as context removal, never native shutdown.
