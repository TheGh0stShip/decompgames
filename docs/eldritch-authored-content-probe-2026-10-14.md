# Eldritch authored content-format probe — October 14 UTC

An independently authored **Beacon Yard** resource prototype now loads through the ported game's native readers. Thirty-four muted acceptance checks passed in headless Microsoft Edge with SwiftShader, and the native room load/save roundtrip reproduced the authored file byte-for-byte. [Evidence](eldritch-authored-content-probe-2026-10-14.json) records the resources, build and scoped test results. This follows the [source/browser probe](eldritch-browser-probe-2026-10-13.md); it is resource and adapter acceptance, not actual game startup or gameplay. Catalog and distributed runtimes remain unchanged at 85; the matching-decompilation milestone stays at four of five.

## Original resource prototype

The private generator creates 19 resources totaling 133,488 bytes, with per-file hashes and provenance. Graphics, mesh/animation, glyph bitmap/metrics, mathematical sound cues, text, map and configuration data are dedicated to CC0-1.0. The generator, authored shaders and port adapters are MIT; upstream game code and dependencies retain their separate grants. No original retail graphics, model, animation, font, sound, map/room or localization/book text is an input. No clean-room isolation is certified.

The resources are an original sealed 12×12×8 voxel courtyard with one interior passage and five spawner records; a new 8×8 tile atlas, beacon surface and fallback textures; a 24-vertex/36-index beacon with one bone, a rest pose and 30 authored pulse frames; a new ASCII grid font in the native remaster format; three synthesized mono PCM cues; original instructions and objective plan; and prototype configuration/shaders. The proposed objective is to activate three beacons before using the gate. Actor, interaction, objective and complete game/UI configuration are still pending. The instructions describe planned controls, not verified gameplay.

An independent data/provenance check validates all 19 resource hashes and reaches all five authored spawner locations through 92 walkable plan cells, with two-cell headroom. This is a map-design check, not execution of the native world, collision controller or objective. The prototype's provenance manifest explicitly marks it unplayable. Ten provided developer-licensed program/configuration texts were inspected privately as interface references; no original room/map/media or retail package was extracted. They were not copied into this authored prototype.

## Native interoperability

The acceptance executable excludes the actual game entry point. It uses `ConfigManager`, `EldRoom`, `MeshFactory`, `BoneArray`, `Font`, the selected SoLoud WAV decoder and the ported GL renderer/shader classes, rather than JavaScript replacements.

All 34 checks passed: text-config parsing, explicit zero packages/volume and objective metadata; native room scalar/count/spawner/doorway/full-read fields; actual wasm mesh/animation structure sizes, counts, positions, bone identity/weights, authored keyframes and material name; native bone-array construction, one-second animation lookup and pose interpolation; decoding each of the three authored WAVs and verifying amplitude; video-only SDL/WebGL2 initialization; single-line/multiline font layout and vertical metrics; matrix identity/translation pixel readback; absence of GL errors; and resource cleanup with the borrowed GL context still alive.

The room's separate native serialization check returned exactly 1,285 bytes, SHA-256 `fe5d163aa33adb70209a7c3ca5d0a334b77b8935be7f706ab4ff78c22c82fc1c`, matching the authored input. Mesh ABI checks confirm the selected wasm layout, including 32-byte mesh headers, 88-byte padded animation records, 28-byte bones and 16-bit indices. These checks are scoped to this small asset set; malformed-resource handling and every legacy format are unverified.

The font fixture was corrected to account for a native space glyph and use eight-pixel line spacing. Final native layout is 11 glyph records/67×7 pixels for `BEACON YARD`, and 10 records/15-pixel height across two lines. This verifies native metrics/layout, not complete in-game UI rendering. Animation loading/interpolation is verified; animated character rendering remains unverified. WAV decode/amplitude checks are silent data checks, not audible playback or audio-device acceptance.

## Further port fixes

The previous WebGL adapter checks did not exercise camera/material matrix upload. The full renderer still passed `transpose=true` to `glUniformMatrix4fv`, which WebGL forbids. The new private adaptation transposes each matrix in CPU memory and uploads with `transpose=false`; tests exercise the actual native shader-program table and renderer setters. A nonidentity translation moves the rendered geometry outside the viewport, exposing the expected blue clear color; identity draws red. The result is checked by pixel readback with no GL errors.

Resource managers must also release their GL objects before the derived renderer destroys its context. Cleanup is now idempotent and called before context destruction; a renderer borrowing the test's context leaves it current. The native acceptance checks borrowed-context cleanup. Actual game-owned context creation/destruction and full restart/unload behavior remain pending. The earlier source/browser probe is preserved separately.

All 424 selected game/library units and 12 vendored zlib C units compile and link again after these changes. Warnings remain. The private game-entry module was linked but not executed; the separate resource-test executable preloads only authored prototype files and its manifest. Nothing was shipped or deployed. The native test context, browser and local server were closed; playback stayed muted, and audible audio is unverified.

## Next gate

Complete the independently authored game configuration, including a player and interactive beacon/gate actors, world/material/shader settings, input and UI. Wire the proposed objective through native game behavior and exercise the actual game entry point. Then verify ordinary movement/interaction, completion, restart and durable save/restore where offered; complete exact native/header/SDK/runtime/emitted-JavaScript notices and source packaging/rebuild checks before integration. This remains an original replacement-content edition based on the developer-released Eldritch source, not the retail campaign, a new decompilation or an emulator. Mario Party 2/3, Halo and prior private ROM research remain untouched.
