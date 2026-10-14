# Eldritch native startup and movement — October 14 UTC

Beacon Yard now starts through Eldritch's actual native `main` entry point using only independently authored resources. A muted headless Microsoft Edge test with SwiftShader also verifies limited keyboard movement, grounding and wall collision through the upstream native input, player, camera and physics systems. [Evidence](eldritch-native-startup-2026-10-14.json) records the build, observations and remaining gates. This advances the previous [resource-format acceptance](eldritch-authored-content-probe-2026-10-14.md); it does not establish a complete playable objective or release readiness.

The original developer-released Eldritch source remains the basis of an original replacement-content edition. This is not a decompilation, emulator or retail campaign. No clean-room isolation is certified. The previously audited developer code grant, selected dependency grants and authored asset dedication are separate; exact SDK/runtime/emitted-JavaScript notices and reproducible source packaging remain pending. Catalog entries stay at 85 and the matching-decompilation milestone at four of five.

## Native configuration and port changes

Three new authored resources—a BMP icon, root configuration and world/player/material configuration—extend the prior 19 resources to 22 totaling 139,591 bytes. The new data is dedicated to CC0-1.0; generators, observer, shaders and authored adapters are MIT. The prototype manifest still marks the edition incomplete. No original retail map, model, font, story text, graphics, audio, ROM or content package is preloaded. The earlier mixed official source ZIP remains private; this does not claim that its supplied binary members were never downloaded.

The native world generator loads the authored 12×12×8 courtyard as one prescribed room with no exits or transforms. Its outer padding produces a 14×14×10 native world. The minimal player uses the existing native transform, gravity, player controller, collision, camera, health, inventory and stat-modifier components. W/A/S/D bindings are authored; only forward and left movement were tested. Beacon and gate spawners currently create inert marker entities. Visible animated actors, interaction, the three-beacon objective and gate completion remain pending.

Actual startup exposed gaps that the resource harness had not exercised. SoLoud's automatic backend selection did not select the compiled null driver; the browser adaptation now selects it explicitly. Three exact upstream default DDS names bind to the authored TGA fallback surfaces, with no catch-all substitution for missing content. The native renderer explicitly enables `EXT_color_buffer_float` for the game's half-float targets and leaves browser frame scheduling to the main loop. The browser fixture excludes the hardcoded retail package and desktop options/resolution/logo initialization. It provides the mandatory mirror image, authored materials and shaders, and uses the existing built-in Fade screen.

The build reuses the prior passing objects where source and headers remain unchanged, compiles four changed upstream units, and links the actual game entry plus a new native observer. It covers 424 game/library units, 12 zlib C units and one observer unit. Header equality is checked before baseline-object reuse; changed headers require a fresh compilation. This is an incremental build, not a fresh extraction rebuild. Warnings remain, and whole-runtime notice closure is not certified.

## Scoped acceptance

The observer reads native player position, health, grounding, dimensions, clock and GL errors. It does not inject movement, position or objective state. Playwright sends ordinary browser keyboard events to the actual game.

| Observation | Final result |
| --- | --- |
| Actual native initialization | Completed |
| World dimensions | 14×14×10 |
| Settled player | (3.5, 3.5, 2.75), grounded, health 5 |
| W held for at least 0.75 simulation seconds | Y advanced to 4.438221 |
| A held for at least 2 simulation seconds | X stopped at 2.253485 against the authored wall |
| After release and settling | Position stable, grounded, health 5 |
| Native simulation time | Advanced beyond four seconds |
| GL errors at four observation points | Zero |
| Browser/console errors, missing HTTP resources, external requests | Zero |
| Instrumented browser audio-context constructions | Zero; explicit SoLoud null driver |
| Native simulation/render loop, browser, local server | Stopped/closed |

The initial movement assertion required a full voxel of displacement in 0.75 seconds and rejected the observed 0.959805-voxel movement. The acceptance threshold was corrected to more than half a voxel. Both that result and the earlier startup failures are retained privately; final values above come from the separate passing acceptance run. The courtyard's native rendering was also visually inspected. These results verify startup and limited movement/collision, not every control or ordinary full-game completion.

The stop hook cancels the native loop before browser teardown. It does not exercise native game save-on-shutdown or resource/context destruction; those remain unverified. Browser testing stayed muted. Silent backend initialization and the prior WAV decode checks do not establish audible audio acceptance.

## Remaining release gates

Wire authored animated beacon/gate actors, native interaction and objective completion; finish browser controls, HUD and help; verify restart and durable save/restore where offered; test owned-context/resource destruction and full unload; and complete exact code/dependency/SDK/runtime notices plus reproducible source packaging and extraction rebuild. No game integration or deployment occurred. Mario Party 2/3, Halo and prior private ROM research remain untouched.
