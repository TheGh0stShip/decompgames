# Prism Foundry: selected SDK sources and additional notices

All **380 traced SDK archive-member records** now map to **380 distinct local translation-unit files**, totaling **3,677,571 bytes**. Each file matches its primary upstream Emscripten **6.0.10** or SDL **release-2.32.10** counterpart after CRLF/LF normalization. No fetch errors or byte mismatches remain. This advances the private developer-source port's dependency record; it adds no catalog entry or decompilation.

## Source mapping and capture

The [source audit recipe](../experiments/prism-foundry-integration/audit-sdk-sources.py) starts from the preceding actual link trace, resolves source names within their component roots, and explicitly selects the browser/single-threaded SDL backends and Emscripten libc overrides recorded in the installed build recipes. It preserves dotted translation-unit names: `ios.instantiations.o` maps to `ios.instantiations.cpp`, separately from `ios.o`/`ios.cpp`. A uniqueness assertion caught an initial filename-resolution error before any primary-version match claim was recorded; the corrected run resolves all 380 distinct sources.

The two installed recipes, [system_libs.py](https://raw.githubusercontent.com/emscripten-core/emscripten/6.0.10/tools/system_libs.py) and [sdl2.py](https://raw.githubusercontent.com/emscripten-core/emscripten/6.0.10/tools/ports/sdl2.py), also match their pinned primary versions. The cached **9,111,739-byte SDL source ZIP** matches the SHA-512 specified by that port recipe. A private **887,272-byte ZIP** preserves the 380 source files plus both recipes; its SHA-256 is recorded in the [machine receipt](prism-foundry-sdk-sources-2026-10-15.json). This source bundle has not been uploaded.

This mapping follows installed build recipes and names. It does **not** rebuild the existing SDK archives or prove that every instruction in them was compiled from these files. Included/transitive headers, compiler-generated/runtime JavaScript inputs and full build configuration/source packaging still need capture and review.

## Notice scope

The [notice collection recipe](../experiments/prism-foundry-integration/collect-sdk-notices.py) preserves **62 distinct byte-exact comment blocks across 190 occurrences** in a **93,174-byte supplementary inventory**. It retains entire matching C/contiguous line-comment blocks with source paths, offsets, line numbers and hashes. Its keyword scan is a review aid, not an exhaustive permission detector. Sources with no matching comments still require the applicable component notice and source context.

The [copied comment inventory](../experiments/prism-foundry-integration/notices/selected-sdk-notice-comments.txt) supplements the eight previously preserved component documents. It retains selected Sun permission statements, Arm MIT SPDX/copyright declarations, Lynn Ochs' MIT-style smoothsort notice, LLVM Apache-2.0-with-exception declarations, Emscripten notices, SDL/Valve/Gareth McCaughan/Andreas Schiffler attributions, public-domain statements, and SDL's ARDI permission comment. Conditional source blocks are retained conservatively; an archive member trace alone does not prove that each such source branch survives linking.

The selected [`yuv_rgb_std.c`](https://raw.githubusercontent.com/libsdl-org/SDL/release-2.32.10/src/video/yuv2rgb/yuv_rgb_std.c) explicitly points to BSD-3-Clause terms. Its separate [upstream license](https://raw.githubusercontent.com/libsdl-org/SDL/release-2.32.10/src/video/yuv2rgb/LICENSE), copied as [SDL2-yuv2rgb-LICENSE.txt](../experiments/prism-foundry-integration/notices/SDL2-yuv2rgb-LICENSE.txt), requires retaining the notice/conditions/disclaimer for source distributions and reproducing them in binary-distribution materials. This **1,480-byte** primary copy matches the installed source after newline normalization. It is distinct from the SDL root zlib-style notice.

The selected [musl sine source](https://raw.githubusercontent.com/emscripten-core/emscripten/6.0.10/system/lib/libc/musl/src/math/sin.c) retains Sun's notice-preservation condition; [dlmalloc](https://raw.githubusercontent.com/emscripten-core/emscripten/6.0.10/system/lib/dlmalloc.c) records Doug Lea's public-domain/CC0 statement alongside Emscripten's adaptation. These facts do not replace the remaining header/runtime/source review. No original game media was acquired, imported or relicensed by this audit.

## Verification and remaining gates

The completed read-only audit verifies all 380 local/primary comparisons, both recipe comparisons, exact preserved source and notice hashes, source uniqueness and the SDL archive SHA-512. The private ZIP is checked against all 382 member hashes. No game or browser was started, no runtime changed and no audible test occurred. The prior muted campaign/save evidence remains attached to the unchanged candidate.

Remaining work includes transitive SDK/game headers and generated/runtime inputs, remaining game-source expressive tables/special cases, complete corresponding-source and distribution notice packaging, shipping allowlists, broader hazard/shooting/save cases, the retained WebGL warning and muted production acceptance. The catalog remains **90**. Mario Party 2/3, Halo and private ROM research remain untouched.

The historical [campaign-root/runtime checkpoint](prism-foundry-roots-runtime-2026-10-15.md) retains its original eight-notice and 99-persistent-input scope; this follow-up records the additional source and notice evidence without claiming complete dependency clearance.
