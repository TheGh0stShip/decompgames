# Prism Foundry integration groundwork

Authored MIT animation/descriptor adapters and course-selection code for the Moon Child FE source-port experiment. **No game startup, playthrough or new catalog entry.** Interfaces and retained callers were inspected; this is not a clean-room certificate.

`animation.cpp` replaces `Classes/moonchild/anim.cpp`. It bounds forced frames against the actual frame count, handles null/empty sequences, rejects invalid sequence indices, and preserves ordinary forward/reverse stepping. `assets.cpp` replaces `Classes/moonchild/asset.cpp`: descriptor-validation failures leave the target lists empty, before newly parsed assets are committed. It retains actual native sprite construction and PCX decoding after checking the selected image profile.

This profile requires single-plane 8-bit RLE, zero origin, even width with no padded scanline, dimensions at most 2048×4096, a complete palette and no trailing bytes. Frame paths are limited to 80 characters because the retained `Cblitbuf` constructor uses a 100-byte diagnostic buffer. Descriptors are capped at 256 KiB, lines at 250 characters, frames per sequence at 100, concrete sequence slots at 21, total frames at 4096, sequence/animation definitions at 256 each and decoded sprite pixels at 16 MiB. This is a controlled authored-content profile, not a general PCX compatibility or arbitrary-input safety certificate.

`make-levels.py` generates CC0 course constants from the existing authored `campaign.json`. `FoundryConfigureLevels()` selects the three corresponding native `LEVEL_DESCR` entries and empties the other 17 runtime entries. `FoundryInitCourse()` and the checkpoint/gate callback compile against retained native actor APIs. **The initializer and gameplay callback have not executed**, and startup is not wired to them. Original source-side tables and unused campaign routines have not all been purged or reviewed merely because the runtime descriptor selector exists.

```text
python build-bounds.py --base-build ADAPTED_88_UNIT_BUILD --pack AUTHORED_PACK --output NEW_OUTPUT_DIRECTORY --emscripten EMSCRIPTEN_DIRECTORY --em-config EMSCRIPTEN_CONFIG --node NODE_EXECUTABLE
```

The recipe verifies the pinned base text/overlays, authored-pack hashes and **85 exact retained native object hashes** against the earlier committed receipt. It compiles four new/test units with strict warnings for their own code, treats retained headers as system headers, rejects unresolved symbols and enables assertions/SAFE_HEAP at final link. It runs a Node-only boundary/configuration harness and replays the committed native-content harness with the two animation/descriptor units changed. No game Host, loop, video or audio is initialized. SAFE_HEAP is not a complete memory-safety or leak-proof certificate.

Tests accept the 21-slot/100-frame boundaries and four 4-MiB sprites at the aggregate limit; reject a fifth such sprite, 22 slots, 101 frames, malformed/missing content and other invalid cases; and compare all 265 actual native-decoded image/palette SHA-256 values during full content replay. See the [measured checkpoint](../../docs/prism-foundry-bounds-levels-2026-10-15.md). The old source-only and content-only receipts remain separate historical results. No runtime or complete source archive is published here.
