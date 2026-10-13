# Abuse, OpenLoco and Fallout source intake — October 13

These three titles are absent from the 83-entry catalog. Abuse offers a documented permissive original-source route, but no reviewed ready browser distribution meets all intake requirements. OpenLoco remains a lower-priority engine recreation under the September 20 pause. Fallout Community Edition's code license is outside the current permissive route. No game or asset package was integrated.

[Snapshot](abuse-loco-fallout-source-snapshot-2026-10-13.json) records 33 selected decoded UTF-8 source/build/notice texts across five pinned repositories. Source inspection remains private; no graphics, level, music, sound, executable, prebuilt library, installer or release archive was downloaded. This is not a complete dependency or content audit.

## Abuse: an original released-source port, not a decompilation

[Archived developer source](https://github.com/videogamepreservation/abuse/tree/01cce80eaf2ae82bafb9981162e205e42d0fae2f), pin `01cce80eaf2ae82bafb9981162e205e42d0fae2f`, had 95 stars. Its [README](https://github.com/videogamepreservation/abuse/blob/01cce80eaf2ae82bafb9981162e205e42d0fae2f/README) contains an explicit Crack dot Com public-domain source release, attributed to founders Jonathan Clark and Dave Taylor. This is materially stronger provenance than a reconstruction contributor's root badge. It permits new games and ports using the released source. No clean-room certificate is asserted or needed to describe the developer release.

That same notice retains trademarks and the retail/registered data set: levels, graphics, audio and other content not common to shareware. It allows shareware data reuse except Bobby Prince's WAV files. It does not release every retail file. No shareware file inventory, exact provenance manifest or complete independent pack has been established here.

[Xenoveritas/abuse](https://github.com/Xenoveritas/abuse/tree/9d1f66f57377859bae10e28eabebea0b9c750490), pin `9d1f66f57377859bae10e28eabebea0b9c750490`, had 170 stars. Its [COPYING](https://github.com/Xenoveritas/abuse/blob/9d1f66f57377859bae10e28eabebea0b9c750490/COPYING) identifies public-domain original source, WTFPL helper/tool code and **GPL-2.0-or-later `src/sdlport/*`**. CMake actually compiles and links that adapter; this is not merely an optional build tool. The ready modern port therefore does not satisfy the current whole-runtime permissive criterion. SDL2 and SDL2_mixer are separate dependencies whose exact selected codec/library closure has not been audited.

The modern COPYING calls its broader data tree public domain, whereas the archived developer release explicitly excludes retail-only content. Its install list includes 22 numbered levels, Mac levels and multiplayer/add-on files without a reviewed per-file mapping to the shareware release or later author grants. Do not resolve that discrepancy by assuming all data is cleared. COPYING records audio redistribution permission specifically given to Debian; README omits audio and fRaBs because of unclear/conflicting permission. Those statements are not a general CC0 audio grant.

The permissive engineering route would retain only the verified developer-released source, independently implement a browser platform adapter, and either inventory permitted shareware content precisely or supply a complete authored replacement pack. Reviewed original interfaces expose palette/image updates and keyboard/mouse event handling, while the old platform implementation uses X11/shared-memory APIs. Browser scheduling, input, filesystem/save handling, silent audio and modern compiler compatibility remain unimplemented and untested. The existing GPL adapter was not copied into a new permissive runtime.

**Disposition:** original source permission established for the documented release; no eligible complete runtime/content/build yet. This is a conditional source-port candidate, not a rejected original-code grant, new decompilation or completed game. No component compile or gameplay proof is claimed.

## OpenLoco: MIT reimplementation with a concrete content gate

[OpenLoco](https://github.com/OpenLoco/OpenLoco/tree/e71abfb3c3dd29a6db5da58c5b4be0a476d8733c), pin `e71abfb3c3dd29a6db5da58c5b4be0a476d8733c`, had 1,935 stars. Root MIT copyright OpenLoco developers 2018 was verified. README calls this a C++ reimplementation of Chris Sawyer's Locomotion and reports completion of reimplementation in December 2025. That upstream report is not our gameplay, matching-binary or clean-room verification. Classify it as an engine reimplementation; broad expansion remains paused.

Original game files remain required. Reviewed `Environment.cpp` explicitly validates `Data/g1.DAT`, requests an original installation and maps CSS sound files/scenarios. The existence of freely usable object graphics is therefore not a ROM-free standalone game proof.

[OpenGraphics](https://github.com/OpenLoco/OpenGraphics/tree/019943c5aa9654ea15a401e48ab25d48217004a6), pin `019943c5aa9654ea15a401e48ab25d48217004a6`, has a separate MIT notice, copyright OpenLoco 2024. README describes ongoing replacement of 545 vanilla assets with region-based packs; it does not certify a complete independent base game. Only root texts were reviewed. No object/model provenance, completeness or coverage of required g1/UI/fonts/maps/audio was certified. OpenLoco CMake fetches the different `v0.1.12` objects release; that archive was not downloaded or cleared by the current-HEAD notice.

Current code uses C++20/SDL3, PNG/zlib, OpenAL and fetched yaml-cpp/fmt/sfl; tests, Windows breakpad and libstdc++ TBB have conditional paths. System-selected dependencies need exact notices, not presumed MIT from the game root. Source inspection records tags and vcpkg pin but does not close those grants. Reviewed entry point has a blocking message loop, and native platform builds are documented; no verified browser scheduler, storage, renderer/audio backend or gameplay exists in this audit.

**Disposition:** preserve as a content/dependency/browser engineering lead below actual decomps and released-source ports. No new entry, original media or generic substitute scenario.

## Fallout Community Edition: Sustainable Use restriction

[fallout1-ce](https://github.com/alexbatalov/fallout1-ce/tree/0609bcfd0ec40ff0571d0f57fab2821eb461dc8b), pin `0609bcfd0ec40ff0571d0f57fab2821eb461dc8b`, had 2,944 stars. Actual [LICENSE.md](https://github.com/alexbatalov/fallout1-ce/blob/0609bcfd0ec40ff0571d0f57fab2821eb461dc8b/LICENSE.md) is Sustainable Use License 1.0, limiting distribution to free, noncommercial purposes. It is not MIT or an accepted permissive whole-code route. Replacing graphics would not change that restriction.

README describes a reimplementation based on Reference Edition and requires owned Fallout data, including `master.dat`, `critter.dat` and the data folder. This audit does not certify independent clean-room development or a matching decompilation. CMake selects SDL2, adecode and fpattern separately; no complete dependency audit or reviewed browser target/gameplay is established. Native/mobile releases are not WebAssembly evidence.

**Disposition:** current code-license gate fails; original content, exact dependencies and browser build remain separate unresolved gates. No data or binary fetched, build/player launched, catalog count changed or deployment made. Mario Party 2/3 and Halo remain untouched.
