# Beacon Relay source port

Three independently authored courses run on developer-released Celeste Classic C# gameplay algorithms. Six display/content literals are independently replaced, including an unused message, before compilation and source packaging. This is a developer-source port with replacement presentation, not a decompilation, clean-room certificate, ROM emulator, original PICO-8 campaign or commercial Celeste (2018) port. Selected runtime grants and distribution status are recorded separately in the dated runtime review and release receipt.

`Classic.cs` is fetched only from `NoelFB/Celeste` at `1b0ce45c75e05649ae91b44a8bb6b196684e4352`, SHA-256 `657515f88328d0269fca3d5b83acbafb8bc61b24db7f5b6bff8a7d442fcb833d`, and then `content_patch.py` replaces the six pinned UI literals without embedding the original expressive message in the patch. The compiled source hash is recorded separately. The corresponding-source archive contains the patched class, not the original message-bearing input. The author archive's MIT grant covers its included code. It excludes commercial game assets. The original `Emulator.cs`, XNA/FNA/Monocle binaries, cartridge, Lua payload, media and maps are excluded.

Own geometry value types and host adapters supply the compatibility surface. Own drawing commands, rover animation, font glyphs, palette, text substitutions and three maps supply the presentation. The prototype has no audio implementation and starts and remains silent. Sprite IDs are interface selectors, not copied sprite images. It does not implement every original object's rendering or certify original-machine timing/math accuracy.

The controller advances only after reading the native flag object's collision-driven `show` field. Upstream `PICO_COMPLETES` increments when a flag is instantiated and is explicitly not a win test. The controller then advances through its three courses using the public room-loading API. New relay starts through the original title/jump path; normal death/respawn stays inside the unchanged game class.

The JS adapter runs at 30 ticks/second with ordinary keyboard input, holds brief key presses through a tick, releases input on focus loss, and supplies Pause/Stop. Next course stores `{version:1,course:1..3}` in this origin/profile. Resume begins at that course's entrance or shows the completed relay. Position, collected lights, retries and elapsed time are not durable checkpoint fields. New relay keeps the prior durable checkpoint until the next successful checkpoint. Clearing site data removes it. No portable save import/export is exposed.

Rebuild with Python 3 and .NET SDK **9.0.318**:

```powershell
python experiments/beacon-relay/build.py --output C:/private-builds/beacon-relay
```

The script fetches the exact signed Microsoft `Microsoft.NETCore.App.Runtime.Mono.browser-wasm` **9.0.20** package, validates SHA-256, selects the recorded 23 managed-assembly reference closure, and writes SRI boot resources. Serve the generated `site` over HTTP with JavaScript/WASM MIME types. The game assembly is managed IL interpreted by the Mono WebAssembly runtime; this is not a game AOT compilation. No WASM SDK workload is needed for this manual boot route. The full package license/third-party notices and selected ICU/Emscripten/system-library notices are retained without asserting every broad notice applies to this selection. The prebuilt native framework and SDK objects have not been independently rebuilt.

The private receipt verifies all three authored courses, collection, jump/dash/recharge, fall/respawn, completed and unfinished-course checkpoint retention across full browser shutdown and new process, short start tap buffering, Pause, release of held input on canvas focus loss, invalid/malformed storage rejection, persistent unavailable-save feedback and Stop. Storage fault injection is recorded separately from normal gameplay; it does not set native game state. Missing loader assets and a stalled manifest fail before gameplay with controls disabled. The player preflights required asset availability and uses a 30-second loading deadline; unusually slow connections may require a retry. Production/site acceptance is recorded separately. Audio playback is unverified and deliberately absent.

Run the private acceptance helper from the repository with its existing Playwright dependency and Edge:

```powershell
node experiments/beacon-relay/test-browser.cjs C:/private-builds/beacon-relay
```

It starts a loopback-only server, blocks external requests, launches Edge headlessly with `--mute-audio`, observes read-only native state, writes its receipt/screenshots under the private build output, and closes the runtime/browser/server. Persistent test profiles remain under that output for evidence; do not publish them.

See `docs/celeste-author-source-intake-2026-10-14.md` and its linked receipts. Builds and browser profiles stay outside this source directory.
