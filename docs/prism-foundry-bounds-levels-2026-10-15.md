# Prism Foundry: animation bounds and authored level selection

The private integration groundwork now passes animation/descriptor boundary tests, selects three authored native level descriptors, and passes the full native content replay. **The course initializer and gate/checkpoint callbacks are compiled, not executed. No game startup, gameplay or release is claimed.** Catalog remains **90**, with no new decompilation count.

## Concrete fixes and checks

The retained animation code allowed a forced frame to equal the frame count, which is outside the frame array. The retained descriptor parser could populate more slots than the 21-element animation array, and maintained a 100-element temporary frame list without rejecting excess entries. The new [MIT adapters](../experiments/prism-foundry-integration/README.md) bound these operations, reject null/zero-count/invalid sequence states, and validate descriptors before committing newly loaded lists.

Frame-file validation precedes the retained native sprite constructor and PCX decoder. The authored profile checks dimensions, RLE packet counts, palette completeness and exact end-of-file. It restricts frame paths to 80 characters because the native blit-buffer constructor formats a diagnostic into a 100-byte array. Size/count/pixel-budget limits bound this selected content path; the legacy constructor and general PCX API were not globally rewritten or certified for arbitrary inputs.

The final Node harness passes:

- Forced-frame lower/upper/count bounds, null and zero-count handling, invalid sequence rejection, valid forward/reverse wrap and recovery from an invalid current index.
- Positive 21-slot and 100-frame cases. Four independently generated 4-MiB sprites are accepted at the 16-MiB aggregate sprite-pixel limit; a fifth is rejected.
- **21 rejected descriptor/image cases**, including slot/frame overflow, empty or unknown definitions, malformed quotes, oversized text, missing terminator/files, trailing descriptor content, invalid image profile/RLE, incomplete palette, trailing image bytes, long frame path and excess decoded pixels. Target lists stay empty after these rejections.
- Acceptance of the actual authored **258-frame, 32-sequence, 12-animation** pack.

The recipe verifies base text/overlay hashes and reuses **85 exact native objects** from the prior [content checkpoint](prism-foundry-content-2026-10-15.md), replacing the animation/descriptor objects and application main. Four new/test units compile; strict link and both harness runs pass. Assertions and SAFE_HEAP are enabled at final link. Retained native objects were reused, not independently rebuilt here; this is not a complete memory-safety/leak certificate.

The first harness compile used a linker-only assertions setting during compilation; moving it to the link fixed that driver error. Strict warnings then exposed preexisting header diagnostics, including Microsoft-only pragmas and class/struct tag mismatches. The final recipe treats the hash-verified retained headers as system headers and keeps strict warnings for the authored code. Those header diagnostics were not fixed or converted into a blanket warning-free upstream-source claim.

## Full content replay preserved

The committed native-content harness was compiled with the new adapters. **All 265 native-decoded image and palette SHA-256 comparisons still pass**, over 1,413,900 pixel indices and 203,520 palette bytes. Native selection/stepping across 252 animation slots, three map-file fingerprint checks, three collision-grid checks, 22,016 cell samples and six out-of-bounds samples also pass. The authored pack and its provenance manifest are unchanged.

## Authored level selection, not gameplay

The course-data generator reads only the existing CC0 authored `campaign.json`. The native selector is tested against Assembly Floor, Cooling Loop and Night Shift dimensions, map/description/background/tile paths and initializer pointers. The other **17 `LEVEL_DESCR` entries** are empty after selection. Out-of-range course lookup returns no course.

The compiled initializer uses retained native actor APIs for the courier and three pickups, and an authored gate/checkpoint callback. Neither is executed by these tests. No pickup was earned, checkpoint reached or gate passed. Startup flow, objective progression, death/retry, save restoration, Stop and ordinary full gameplay still need integration and muted verification. Unused original source-side tables, special effects and UI/story content still need review/removal or replacement before a shipping-content claim. Selecting runtime descriptors does not itself purge original source constants.

The original-programmer source grant, the [separate Microsoft loader replacement](moonchild-independent-adapters-2026-10-15.md), authored CC0 media, and final selected SDK/runtime notices remain separate scopes. Source packaging and production verification remain open. No browser/player, audible test, runtime upload or website deployment occurred. Mario Party 2/3, Halo and private ROM research were untouched; no test players or servers were left running.

[Machine-readable checkpoint](prism-foundry-bounds-levels-2026-10-15.json).
