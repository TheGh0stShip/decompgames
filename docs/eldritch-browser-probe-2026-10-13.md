# Eldritch source-only browser-port probe — October 13

The 2019 developer source now compiles and links privately to WebAssembly. Seventeen muted native GPU adapter checks passed in headless Microsoft Edge with SwiftShader enabled. This establishes a useful browser-port basis, not game startup or completed gameplay. No catalog/runtime distribution changed; the catalog remains at 85 and the decompilation milestone at four of five. Eldritch is original released source, not decompilation or clean-room-certified work.

This follows the [source intake](eldritch-raptor-ken-source-intake-2026-10-13.md). [Probe evidence](eldritch-browser-probe-2026-10-13.json) records source/output hashes, selected source counts, test cases and remaining gates. Port edits, full source inventories, compiler logs, linked maps, executables and the test harness remain private; nothing was deployed.

## Source selection and dependencies

The official `Eldritch-Source-2019-04-16.zip` was downloaded privately in full: 7,625,114 bytes, SHA-256 `7bee255de9943e805bbd591ae7fb6ca1d9ac6609b5ba84374ab694eb7edb6774`. Its 2,339 directory entries agree with the earlier range-read metadata. The full archive includes supplied binary members; only **1,091 selected textual source/build/notice files** were extracted, totaling 8,162,199 bytes. No supplied executable/library binary, configuration, room, map, media or retail package member was extracted or run. No original retail files or ROM were preloaded or shipped.

The developer's [zlib release notice](https://eldritchgame.com/bin/license.txt) covers game source with separately licensed libraries; the [release readme](https://eldritchgame.com/bin/readme.txt) expressly excludes missing retail content. The earlier review established the developer publication route and selected library notices. This probe does not extend that grant to retail assets.

Actual vendored `zlib.h` declares **1.2.3**, copyright 1995–2005; the root notice describes 1.2.8. The actual source retains its zlib-style grant. Dependency identification and an eventual release notice must use the selected version's real header, not copy the root version description. The private probe compiles its 12 supplied C files; strict C99 compilation requires the POSIX feature declaration for `fdopen`. No implicit-declaration errors were suppressed.

The build selects SoLoud's null backend and excludes its SDL2-static audio backend. The framework's SDL initialization flags already omit `SDL_INIT_AUDIO`. Desktop GLEW source is excluded in favor of toolchain GLES3 headers; Steam stays disabled. The old project files are treated as source-list references, with an authored browser recipe instead of their desktop library link lists. TinyXML, SoLoud, its Vorbis decoder, selected SDL/toolchain headers, actual linked SDK libraries, compiler/runtime exceptions and emitted JavaScript still require a complete distribution-level closure/notice inventory. No blanket whole-dependency approval or release eligibility is claimed.

## Compile and link result

Emscripten **6.0.10**, revision `d6c521a7f05449857c76bd99e396895583cf2083`, produced the probe. Five unmodified syntax checks initially found unsupported platform selection in the clock, GL context/framework and main entry point. After the SDL/platform adaptation, 422 of 424 selected translation units compiled; the remaining two shared the date/time platform branch. After the date and WebGL changes, **all 424 selected game/library translation units compiled**, followed by 12 vendored zlib C units. All 436 object inputs linked successfully without supplied prebuilt binaries or preloaded content.

The private game-entry build produced:

| Output | Bytes | SHA-256 |
| --- | ---: | --- |
| JavaScript | 419,227 | `457955b4632f45310b55b3a082fc4406a3cf9dd0997d34ab82e6019157051aa6` |
| WebAssembly | 2,825,066 | `6de8b55c2bf8d316ea610e82df024a63c014f3c90abb6caaa16864828f817044` |

The original game entry point was **not executed**. A content-free link result is not a playable edition. Compiler warnings remain in private logs; warning-free compilation, all legacy paths, a reproducible source distribution and production SDK closure have not been established.

## Authored port adaptations and GPU acceptance

The private adaptations explicitly select Emscripten/SDL without pretending to be Linux; use the toolchain SDL headers; extend the POSIX directory/date branches; request an ES3 context; and replace the blocking framework loop with an Emscripten callback. They use core GLES3 framebuffer calls, typed texture allocation, BGRA-to-RGBA upload conversion, four-component packed-color attributes and float depth calls. Dynamic vertex writes retain CPU storage and upload it explicitly rather than attempting desktop GPU memory mapping. Anisotropic filtering is disabled and border sampling uses the port's edge-clamp policy. Unsupported normalized 16-bit targets are not silently converted into a different format. Future authored shaders must account for packed vertex-color channel order.

The acceptance harness excludes the game entry point. It supplies independently authored test shaders and a flat 2×2 TGA test tile dedicated to CC0; it uses the ported game's actual `GL2VertexBuffer`, `GL2Texture` and `GL2RenderTarget` classes. It does not replace them with JavaScript mocks. Expected pixel colors were checked through GPU readback.

All 17 checks passed: video-only SDL initialization; WebGL2 context; authored vertex/fragment shaders and program link; initial red geometry; native buffer lock; upload moving geometry outside the view and exposing blue; another upload restoring green geometry; CPU buffer-storage release; native TGA framebuffer completeness and correct RGBA pixel values; float render-target extension availability; native RGBA8, RGBA16F and R32F framebuffer completeness; and absence of GL errors.

This is scoped to headless Microsoft Edge with SwiftShader enabled. It does not verify the complete renderer, camera/input loop, world generation, native UI, authored campaign shaders, MRT effects, cubemaps, compressed textures, animation, persistence, mobile or other browsers. Float framebuffer completeness is not a complete test of float rendering or shader precision. Audio was omitted from the harness, all browser playback was muted, and audible audio remains unverified. The native GL context, browser and local server were closed after the test.

## Remaining integration gates

Create a complete independently authored content pack: graphics, animation, font/glyphs, audio or an explicit silent edition, text, maps/rooms and resource/config data, with a provenance manifest. Supplied licensed configuration/room files are useful interface references but were not imported as the replacement campaign. The native config loader accepts its compiled format or falls back to text parsing, so an authored content pipeline can use the existing loose-file route. Format parsing and resource names still need verification against the chosen pack.

Then exercise ordinary gameplay through the actual game entry point, including movement, world/entity behavior, objectives, restart and durable save/restore where offered. Test the complete renderer/material/shader and input/event-loop paths with those assets, record the exact native/header/library/emitted-JavaScript dependency closure, package a reproducible source archive with correct notices and validate that archive's build. Only then is a ROM-free integrated entry reviewable. Do not count the adapter tests or successful link as gameplay, or this original-source port toward the matching-decompilation milestone. Mario Party 2/3, Halo and prior private ROM research remain untouched.
