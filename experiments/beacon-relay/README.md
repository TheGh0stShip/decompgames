# Beacon Relay private source-port experiment

Three independently authored courses run on the unchanged developer-released Celeste Classic C# game class. This is a developer-source port with replacement presentation, not a decompilation, clean-room certificate, ROM emulator, original PICO-8 campaign or commercial Celeste (2018) port. It is not a catalog entry or cleared binary distribution.

`Classic.cs` is fetched only from `NoelFB/Celeste` at `1b0ce45c75e05649ae91b44a8bb6b196684e4352`, SHA-256 `657515f88328d0269fca3d5b83acbafb8bc61b24db7f5b6bff8a7d442fcb833d`. The author archive's MIT grant covers its included code. It excludes commercial game assets. The original `Emulator.cs`, XNA/FNA/Monocle binaries, cartridge, Lua payload, media and maps are excluded.

Own geometry value types and host adapters supply the compatibility surface. Own drawing commands, rover animation, font glyphs, palette, text substitutions and three maps supply the presentation. The prototype has no audio implementation and starts and remains silent. Sprite IDs are interface selectors, not copied sprite images. It does not implement every original object's rendering or certify original-machine timing/math accuracy.

The controller advances only after reading the native flag object's collision-driven `show` field. Upstream `PICO_COMPLETES` increments when a flag is instantiated and is explicitly not a win test. The controller then advances through its three courses using the public room-loading API. New relay starts through the original title/jump path; normal death/respawn stays inside the unchanged game class.

The JS adapter runs at 30 ticks/second with ordinary keyboard input, holds brief key presses through a tick, releases input on focus loss, and supplies Pause/Stop. Next course stores `{version:1,course:1..3}` in this origin/profile. Resume begins at that course's entrance or shows the completed relay. Position, collected lights, retries and elapsed time are not durable checkpoint fields. New relay keeps the prior durable checkpoint until the next successful checkpoint. Clearing site data removes it. No portable save import/export is exposed.

Rebuild with Python 3 and .NET SDK **9.0.318**:

```powershell
python experiments/beacon-relay/build.py --output C:/private-builds/beacon-relay
```

The script fetches the exact signed Microsoft `Microsoft.NETCore.App.Runtime.Mono.browser-wasm` **9.0.20** package, validates SHA-256, selects the recorded 23 managed-assembly reference closure, and writes SRI boot resources. Serve the generated `site` over local HTTP with JavaScript/WASM MIME types. The game assembly is managed IL interpreted by the Mono WebAssembly runtime; this is not a game AOT compilation. No WASM SDK workload is needed for this experimental manual boot route. The full package license and third-party notices are retained without asserting every notice applies to this selection.

Public binary/runtime upload remains gated on selected native/runtime/toolchain notice closure, browser loading-failure acceptance, packaging and production/site acceptance. The current receipt verifies all three private authored courses, collection, jump/dash/recharge, fall/respawn, completed and unfinished-course checkpoint retention across full browser shutdown and new process, short start tap buffering, Pause, release of held input on canvas focus loss, invalid/malformed storage rejection, persistent unavailable-save feedback and Stop. Storage fault injection is recorded separately from normal gameplay; it does not set native game state. Audio playback is unverified and deliberately absent.

Run the private acceptance helper from the repository with its existing Playwright dependency and Edge:

```powershell
node experiments/beacon-relay/test-browser.cjs C:/private-builds/beacon-relay
```

It starts a loopback-only server, blocks external requests, launches Edge headlessly with `--mute-audio`, observes read-only native state, writes its receipt/screenshots under the private build output, and closes the runtime/browser/server. Persistent test profiles remain under that output for evidence; do not publish them.

See `docs/celeste-author-source-intake-2026-10-14.md` and its linked receipts. Builds and browser profiles stay outside this source directory.
