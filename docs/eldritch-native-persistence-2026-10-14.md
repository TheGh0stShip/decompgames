# Beacon Yard native persistence and cleanup — October 14 UTC

Beacon Yard now passes native partial save/restore, a native world restart, durable completed-game restoration after closing and relaunching the browser, and native GL resource/context cleanup. [Evidence](eldritch-native-persistence-2026-10-14.json) records the exact build and observations. This extends the [native objective checkpoint](eldritch-native-objective-2026-10-14.md). The candidate remains private; product controls, save validation, notice closure and a reproducible release build still block integration. The catalog remains 85 and the matching-decompilation milestone four of five.

This is an original replacement-content challenge using the developer-released Eldritch source, not a decompilation, retail campaign or emulator. No clean-room isolation is certified. The existing developer code grant, dependency/runtime notices and independently authored asset dedication are separate. This checkpoint distributes documentation only.

## Native save and restart acceptance

The keyboard journey activates beacon A after an early gate denial. A thin adapter calls the existing native `EldSaveLoad::SaveMaster`, producing a 589-byte compressed full-world checkpoint. Native `ReturnToHub` with restart and flush flags creates a new yard: player position returns to the spawn, beacon/actor state resets to zero and the gate-denial count resets.

Native `TryLoadMaster`, preceded by the framework's load preparation, restores the checkpoint. Player position and orientation, beacon A's activation, player mask 1, health and the earlier gate denial return. Activating A again is rejected, demonstrating restored actor state separately from the player count. Ordinary keyboard gameplay then activates B and C and completes the gate. The custom component's versioned 14-byte records participate in the upstream world serialization; the test does not inject positions or objective values.

The completed native master is 567 bytes. Emscripten IDBFS mounts `/beacon-save` before native initialization and hydrates it through an asynchronous startup dependency. The test waits for each `syncfs` callback, closes the first persistent Edge context, and relaunches Edge with the same isolated profile at the same local origin. The second native main automatically loads the stored master. It restores the same position/orientation, health 5, player mask 7, all three beacons plus the completed gate, prior gate denial and `YARD RESTORED` status. The restored HUD and green exit terminal were visually inspected.

These are tests of native operations through private adapters. Save/restore/restart buttons, pause controls and storage-error feedback are not yet part of a product interface. Native world restart and fresh browser/module restoration are verified; reinitializing a shut-down framework within the same WASM module is not.

## Shutdown acceptance

The test queues `SDL_QUIT`. The native frame loop stops and calls virtual Eldritch/framework shutdown, including the game's native save and renderer destruction. Instrumented WebGL2 API calls report:

| Object | Created | Deleted | Live after native shutdown |
| --- | ---: | ---: | ---: |
| Buffers | 352 | 352 | 0 |
| Textures | 14 | 14 | 0 |
| Framebuffers | 5 | 5 | 0 |
| Renderbuffers | 3 | 3 | 0 |
| Shaders | 5 | 5 | 0 |
| Programs | 5 | 5 | 0 |

The Emscripten GL registry has zero context entries and no current context before browser closure. An initial test required literal `null` and incorrectly classified the cleared `undefined` value as a present context. The final observation checks nullish absence, the context registry and object counts; no native context workaround was added. That failed diagnostic receipt is retained privately.

This verifies the owned renderer objects and context in this tested path. It does not prove destruction of the framework allocation, every singleton/event-manager allocation or the entire WASM heap. The second run also completes native shutdown, and both browser runs and the local server close.

Both runs use muted headless Edge with SwiftShader and the explicit SoLoud null driver. There are no browser/console errors, native assertions, missing HTTP resources, external requests or instrumented audio-context constructions. Sampled native GL errors are zero. Audible audio remains unverified.

## Remaining release gates

The build still reuses unchanged baseline objects after header equality checks, with five changed upstream units and two authored units. It is not a fresh extraction rebuild. The same 29 authored resources are preloaded; no original retail package, asset or ROM is required.

Before integration, finalize product controls/pause/help and storage-error feedback; validate malformed/unsupported native saves and recovery; clear the stale target label observed after restart; consolidate the current asset provenance and remove prototype metadata; complete exact selected source/header/dependency/SDL2/SDK/runtime/IDBFS/emitted-JavaScript notices; and package reproducible sources with a fresh extraction build. Mario Party 2/3, Halo and prior private ROM research remain untouched.
