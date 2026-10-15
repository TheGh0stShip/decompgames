# Prism Foundry: original campaign roots removed and runtime inputs traced

The private candidate now omits original level/trigger placement roots from the selected build. The resulting **1,925,933-byte WASM** is **250,925 bytes smaller** than the preceding save candidate. Its full muted playthrough, earned checkpoint/browser restart, checkpoint fall/respawn, earned final-save restoration and native shutdown checks pass. Catalog remains **90**; this developer-source port is still private and adds no decompilation.

## Source-side removal

The optional `--strip-campaign-tables` path in the [player recipe](../experiments/prism-foundry-integration/build-player.py) generates a derivative of the pinned globals source. It removes **14 original trigger arrays**, **14 original map descriptors** and their level-init pointers. The 20-slot level matrix starts empty and receives only the three authored descriptors. The original **16-row** scroll-trigger schedule becomes one terminal sentinel.

The selected link excludes the original `globals.cpp`, `levinits.cpp` and `trigger.cpp` objects. A generated globals unit retains needed engine state, while an authored empty trigger dispatcher fits the campaign's object-callback progression. Authored checkpoint/gate callbacks remain active. Unexpected native exit flags retry the current authored course; shutdown frees selected campaign resources without entering original movie/puzzle/menu cleanup paths. The immutable original text inputs, earlier artifacts and boundary-test source remain preserved.

This is **79 exact retained native objects and ten changed/new units**, with strict linking, assertions and final-link SAFE_HEAP. It does not establish complete memory safety. Remaining expressive source tables, unused UI/story code and original-world special cases still need review/removal before a complete shipping-content claim. Original source-code permission and separately excluded media remain distinct scopes; no clean-room certificate is made.

## Actual link-input inventory

The [audit recipe](../experiments/prism-foundry-integration/audit-runtime.py) validates the candidate artifacts, adds an input trace and linker map, and records archive hashes and selected member names. It hashes **99 persistent input files**: 89 project/generated objects and ten SDK archives, with **380 extracted archive-member records**. One additional temporary `embedded_files.o` input is traced but disappears during linker cleanup and is explicitly recorded without an object-file hash. Its authored inputs remain covered by the unchanged pack manifest; the audit also compares the resulting data section bytes.

| Archive | Traced member records |
| --- | ---: |
| libSDL2.a | 84 |
| libGL-getprocaddr.a | 3 |
| libhtml5.a | 1 |
| libstubs-debug.a | 2 |
| libnoexit.a | 1 |
| libc-debug.a | 244 |
| libdlmalloc-debug.a | 2 |
| libclang_rt.builtins.a | 18 |
| libc++-debug-noexcept.a | 16 |
| libc++abi-debug-noexcept.a | 9 |

The trace relink is two bytes smaller because its output filename changes the WASM debug module name from `foundry.wasm` to `audit.wasm`. The parser compares every other section and name subsection byte, which matches exactly. Raw WASM hashes are recorded separately. This is a structural byte comparison, not execution of the trace artifact; gameplay tests use the actual candidate.

## Separate component notices

[Eight copied primary notices](../experiments/prism-foundry-integration/notices/README.md), totaling **67,540 bytes**, match corresponding installed or previously pinned inputs after newline normalization. Their [per-file record](../experiments/prism-foundry-integration/notice-inputs.json) keeps full text, primary URLs and hashes. They cover Moon Child FE's code/media statement, Emscripten, SDL2, musl, libc++, libc++abi, compiler-rt and GLAD scopes.

The official [SDL2 notice](https://raw.githubusercontent.com/libsdl-org/SDL/release-2.32.10/LICENSE.txt), [Emscripten notice](https://raw.githubusercontent.com/emscripten-core/emscripten/6.0.10/LICENSE), [musl copyright record](https://raw.githubusercontent.com/emscripten-core/emscripten/6.0.10/system/lib/libc/musl/COPYRIGHT) and [LLVM library notice](https://raw.githubusercontent.com/emscripten-core/emscripten/6.0.10/system/lib/libcxx/LICENSE.TXT) retain their distinct conditions and exceptions. An SDK root notice alone does not replace component or selected per-file notices. The copied FE notice retains its original-media terms; no such original media is imported or relicensed by this experiment.

Final reconciliation remains for selected musl math/SDL per-file notices, dlmalloc and remaining generated/header notices, exact selected SDK source/build capture and distribution packaging. The pinned pl_mpeg header's MIT SPDX declaration and prior GLAD reproduction remain recorded separately; guessed standalone pl_mpeg `LICENSE`/`LICENSE.txt` URLs returned 404 and are not presented as fetched notices. This checkpoint does not certify complete dependency clearance.

## Verification and remaining work

The initial replay overshot the second ledge, fell before checkpoint activation and timed out waiting for that checkpoint. It reported no JavaScript exception, and native shutdown passed. The test now releases jump steering against observed position instead of relying on a fixed tick estimate. Game physics, geometry, pickups and gate rules are unchanged by that driver correction.

The final ordinary-input run earns all nine pickups and three gates, restores an earned two-pickup checkpoint after a full browser restart, verifies an actual fall/respawn at that checkpoint, earns victory, and restores the earned terminal state after a second full browser restart. The trimmed build's separate smoke test passes delayed loading cancellation, movement/jump, pause/resume, editor-skip rejection, R retry, New game and native shutdown. The retained WebGL `INVALID_ENUM` warning remains. Browsers and local servers were closed; sound stayed off and audible audio remains unverified.

Broader save/hazard/shooting cases, remaining source-content review, complete selected dependency notices/source packaging, shipping allowlists, renderer warning and muted production acceptance remain open. No runtime or complete source archive was uploaded; no website deployment occurred. Mario Party 2/3, Halo and private ROM research were untouched.

[Machine-readable checkpoint](prism-foundry-roots-runtime-2026-10-15.json).
