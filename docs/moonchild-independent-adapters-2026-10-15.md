# Moon Child FE: silent and independent-content adapters

Moon Child FE now passes an **88-unit adapted WASM link and synthetic adapter tests**. This is continued source-port work, not a decompilation, a playable release or a new catalog entry. Catalog remains **90**. The [previous unchanged-source probe](moonchild-gnukem-chromium-source-intake-2026-10-14.md) remains a separate historical build result.

## Separate component scopes

The original programmer's MIT grant remains useful first-party code evidence. Review of selected `Classes/framewrk/fastfile.cpp`, `fastfile.h` and `ffent.h` found Microsoft 1995–1996 notices and warranty disclaimers without a permission grant in those files. The root MIT declaration is not treated as clearing that third-party component. This is a missing selected-file grant, not a determination that no historical SDK license could exist.

The [new MIT adapters](../experiments/moon-child-independent-adapters/README.md) replace the two fast-file implementation/interface files and remove the directory-struct header from the materialized tree. The new reader uses ordinary loose files, not the original packed/compressed format. It implements only functions used by the retained PCX caller. Source interfaces and callers were inspected; no clean-room certification is made.

The reader requires an explicit content marker, constrained names, bounded independent cursors and files no larger than 16 MiB. The marker proves neither authorship nor licensing. Direct map and animation-script file loads bypass this reader, so a complete authored-content manifest and final shipping allowlist remain required.

The selected factory now constructs `NullAudio`. SDL2Audio, AudioEngine and MP3MusicTrack translation units are excluded, with no MP3 decoder needed by that selection. Generic SDK SDL2 Web Audio helpers remain in emitted JavaScript. No game main, browser or player was run, and no audible verification occurred. Future browser runs must still be muted. Removing the compressed-archive reader also allowed removal of the SDK zlib selection; the final strict link succeeded without it.

## Measured verification

The recipe checks all **221** pinned original text inputs, copies them to a new private output tree, applies four explicit overlays and removes one header. The pinned source directory remains unchanged. All **88** selected game/platform units compiled and linked with unresolved symbols rejected. Emscripten **6.0.10**, `-O0`, SDK SDL2 **2.32.10**, WebGL 1 and `INVOKE_RUN=0` were selected. Final build/test elapsed time: **15.988 seconds**.

The separate synthetic Node/WASM harness passed marker rejection, path rejection, read/seek boundaries, negative/overflow offsets, independent simultaneous handles, capacity, closure/reinitialization, an empty file, the 16 MiB cap and all null-audio methods. More substantially, the **unchanged native PCX decoder** read a newly authored 8×4 RLE fixture through the replacement interface and returned the expected 32 pixel indices and all 768 palette bytes. The fixture was generated in the test filesystem; no original image or media was fetched.

The first harness compile failed for a missing `<initializer_list>` include; that was corrected before the passing runs. The first two adapted game links retained the previous zlib flag; the final build removed it. WASM bytes are identical across these three adapted links. JavaScript differs in two generated comments naming the pre-JS source location; after replacing only those location comments it matches. This is not a claim of universal byte-identical JavaScript builds.

Final WASM is **1,073,019 bytes**, SHA-256 `a66b81da6288e32374186d499d749d7b84f841a15bbcf149ff843f53b7352a6d`. JavaScript is **386,769 bytes**, SHA-256 `55519808750d16343c716092a0e74e10b9c85e6e1eec34966d0d6bd2a96e69b6`. WASM validation and module parsing passed: 243 imports, 21 exports. The game module was not instantiated or run. These are private build outputs, not published runtimes or completed corresponding-source distributions.

## GLAD provenance narrowed

The selected source identifies generated GLAD **0.1.36**. Generator/specification text was retrieved from `Dav1dde/glad` tag `v0.1.36`, resolved commit **`1ecd45775d96f35170458e6b148eb0708967e402`**: 52 text files, 3,331,404 bytes. Running that unmodified generator with its packaged GL registry and `--reproducible`, GL 2.1/GLES2 2.0, compatibility profile, no extensions and local files reproduced the selected C/header after line-ending normalization, and `khrplatform.h` byte for byte. [Pinned inputs and comparisons](../experiments/moon-child-independent-adapters/glad-generation.json).

The generator's [pinned license](https://github.com/Dav1dde/glad/blob/1ecd45775d96f35170458e6b148eb0708967e402/LICENSE) distinguishes MIT generator code, Apache-2.0 GL registry material and permissive Khronos header material. Its [generated-code explanation](https://github.com/Dav1dde/glad/blob/1ecd45775d96f35170458e6b148eb0708967e402/README.md#whats-the-license-of-glad-generated-code) offers public-domain/WTFPL/CC0 choices for the generator-authored output portion while retaining separate registry/header scopes. The packaged `gl.xml` explicitly declares Apache-2.0. This reproduction closes the earlier unidentified-generated-file provenance question; final notice packaging and the complete selected SDK/runtime closure are still open.

## Concrete remaining work

The next content boundary includes indexed PCX graphics/palettes, animation descriptors consumed by `asset.cpp`, native 32-pixel tile maps, 16-pixel collision grids, and source-side level definitions, placements, triggers and expressive UI/story text. Existing `globals.cpp` level tables select files and initialization functions; `mc.cpp` loads maps/collision grids directly and calls those level initializers. Merely replacing an image archive would leave this content work unfinished. The PCX test establishes one valid format path, not a full content pack or robust validation of arbitrary PCX input.

An independently authored campaign, animation/graphics/text provenance, no original media, selected dependency/runtime notices, safe initialization/content validation, ordinary movement/objectives/combat or hazards/death/retry, save restoration and Stop must precede integration. Source packaging, catalog deduplication at release and muted production verification follow. No original campaign, root-license blanket clearance, clean-room isolation or full gameplay result is claimed. Mario Party 2/3, Halo and private ROM research were untouched. No players or test servers remain from this work.

[Machine-readable checkpoint](moonchild-independent-adapters-2026-10-15.json).
