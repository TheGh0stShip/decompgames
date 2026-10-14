# Eldritch authored native objective — October 14 UTC

Beacon Yard's complete authored courtyard objective now passes through the actual native game entry point. A muted headless Microsoft Edge run with SwiftShader walks through both wings and the passage, activates the three beacons, and completes the exit terminal. It also verifies that the gate rejects an early attempt and that activating a beacon twice does not increase the count. [Evidence](eldritch-native-objective-2026-10-14.json) records the tested module, resources and native observations. This advances the previous [startup/movement checkpoint](eldritch-native-startup-2026-10-14.md); restart, durable persistence and release readiness remain unverified.

This remains an original replacement-content challenge based on the original developer-released Eldritch source. It is not a retail campaign, decompilation or emulator, and no clean-room isolation is certified. The developer's previously audited zlib code grant, dependency/runtime grants and independent asset dedication are separate. No candidate code, asset pack or runtime was distributed or deployed. Catalog entries remain 85 and the matching-decompilation milestone remains four of five.

## Native challenge and content

A new MIT component receives the existing native `OnFrobbed` events. The upstream frobber selects targets by raycast and the upstream frobbable dispatches activation; the new component records the three beacon bits, rejects duplicates, denies the gate until all three are active, and publishes an original status message. Keyboard turning is implemented in that native component through the existing input system. Movement, gravity, camera and collision use the existing native player systems. The test sends ordinary browser keyboard events and reads native observations; it does not teleport the player or inject positions, activation events or objective state.

The four actors use the authored beacon mesh and pulse animation. The exit terminal has a blue surface, and activated beacons/the completed terminal turn green. Completion changes the terminal state and feedback; it does not open a moving door or load a retail level. New GLSL handles the single authored bone and the native HUD font. Native animation clocks advance and loop while the actors render; every possible animation pose and GPU deformation is not independently measured.

Seven new resource files and two configuration overrides extend the previous pack to 29 unique resources totaling 181,597 bytes. They include two procedural color surfaces, a newly generated HUD glyph atlas and metrics, three authored shaders, and native player/actor/objective/HUD definitions. Data is dedicated to CC0-1.0; authored shaders, generators, component, observer and test code are MIT. Font designs derive from the prior independently authored glyph design data, with new spacing and punctuation. No original retail graphics, font, model, animation, sound, map, localization/story text, package or ROM is an input. Per-file provenance and hashes are in the evidence.

The native HUD shows beacon progress, controls and the currently targeted actor. Bottom-origin font rows correct the native reader's expected TGA convention, and spaces have advance with a zero-width ink rectangle. The final HUD and green completed exit terminal were visually inspected. The pack still retains earlier fixture metadata and prototype help; the release must consolidate provenance and finalize controls/help before distribution.

## Gameplay acceptance

The final journey advances approximately 37.88 native simulation seconds. The player starts at (3.5, 3.5, 2.75), remains grounded with health 5, walks through the authored courtyard's passage to the eastern beacons, and returns to the exit terminal.

| Native interaction | Beacon mask | Complete | Result |
| --- | --- | --- | --- |
| Gate before beacons | 0 | False | Denied once |
| Beacon A | 1 | False | Activated |
| Beacon A again | 1 | False | Duplicate rejected |
| Beacon B | 3 | False | Activated |
| Beacon C | 7 | False | Activated; return-to-gate feedback |
| Gate after three beacons | 7 | True | `BEACONS 3/3 - YARD RESTORED` |

All six interactions report the intended native target, no self-ray obstruction and zero sampled GL errors. No browser/console errors, native assertions, missing HTTP resources, external requests or instrumented browser audio-context constructions occurred. SoLoud uses the explicit null driver. The native simulation/render loop was stopped, and the browser and local server closed. Audible audio remains unverified.

An earlier failed test supplied a useful native diagnostic: the authored camera was at Z=3.3 inside the player's collider, so the interaction ray hit the player at distance zero. Raising the authored stand/camera offset to 0.8 puts the eye at Z=3.55, just above the collider's Z=3.5 top. The final rays reach the intended targets through the existing native interaction path.

A longer diagnostic run also exposed a fixed-timestep assertion caused by repeated float subtraction leaving the last scheduled tick a few ulps short. The browser adapter checks a bounded 0.00001-timestep tolerance and clamps the subtraction residue to zero. The final journey contains no such assertion. Earlier failed runs and passing startup/resource fixtures are preserved separately.

## Build and remaining gates

The private build covers 424 game/library units, 12 zlib C units and two authored units. It recompiles five changed upstream units and reuses unchanged baseline objects after header equality checks; it is not a fresh extraction rebuild. Warnings remain. The authored component implements a versioned 14-byte native save record, but that record, full native save/restore and durable persistence have not been tested.

Next verify native save/restore, durable persistence, restart and full unload/resource/context cleanup; finalize controls/pause/help and one current provenance manifest; complete exact selected code/header/dependency/SDK/runtime/emitted-JavaScript notices; and produce reproducible source packaging with a fresh extraction rebuild. The private courtyard objective has gameplay acceptance, but these gates still block integration and release. Mario Party 2/3, Halo and prior private ROM research remain untouched.
