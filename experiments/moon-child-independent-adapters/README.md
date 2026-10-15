# Moon Child FE independent adapters

Experimental source-port groundwork, **not a playable release or catalog addition**. The first-party source grant and asset exclusion remain as recorded in the [earlier probe](../moon-child-source-probe/README.md). These authored adapters use the MIT license in this directory; referenced upstream components retain their own terms.

`build.py` verifies the earlier probe's 221 pinned text inputs before materializing a separate build directory. It replaces `fastfile.cpp`, `fastfile.h` and the backend factory; adds `NullAudio.h`; and removes `ffent.h`. The three legacy fast-file files carry Microsoft copyright/disclaimer text without a permission grant in those selected files. No original archive parser, compressed `.rz` reader or directory structs are reused by the replacement. Interface names and callers were inspected; this is **not a claim of clean-room isolation**.

The loose-file reader resolves functional names to lowercase basenames within the configured content directory, rejects traversal/absolute/invalid names, bounds reads/seeks, isolates simultaneous open files, caps individual files at 16 MiB and requires an exact `loose-content.marker` containing:

```text
DecompGames Moon FE independent content v1
```

The marker ends with LF. It is an implementation opt-in, **not provenance evidence**. Original `mc.art` cannot substitute for the marker. A future content generator and audited shipping allowlist must cover every file, including direct map/animation-description loads outside this reader. No campaign or marker is preloaded into this build.

`NullAudio` implements the native audio interface without opening files/devices, decoding samples or making host calls. Dummy sound handles preserve the interface; music/movie-stream requests return false. SDL2Audio, AudioEngine and MP3MusicTrack units are excluded. The selected SDK SDL2 library still contributes generic Web Audio helper code: do not describe the entire artifact as containing no audio implementation. Browser testing must remain muted. No browser/player or audible test was performed here.

```text
python build.py --source PINNED_TEXT_DIRECTORY --output NEW_OUTPUT_DIRECTORY --emscripten EMSCRIPTEN_DIRECTORY --em-config EMSCRIPTEN_CONFIG --node NODE_EXECUTABLE
```

Tested with Emscripten 6.0.10 and Node 24.19.0. The recipe selects 88 game/platform units, uses SDK SDL2, strict unresolved-symbol rejection, `-O0` and `INVOKE_RUN=0`. Zlib is no longer requested. It runs a separate Node/WASM **synthetic adapter test**, never the game. The test exercises marker rejection, independent cursors, file limits, invalid reads/seeks, closure, all null-audio methods and the unchanged upstream PCX decoder against newly generated 8×4 pixels/RLE/palette. It does not establish level startup, gameplay, save persistence or Stop.

`glad-generation.json` records 52 pinned generator/specification inputs and reproduction of the selected GLAD files: C/header match after CRLF normalization; Khronos header matches exactly. Generator MIT, generated-portion license options, registry Apache-2.0 and header permissions are separate. See the [adapter checkpoint](../../docs/moonchild-independent-adapters-2026-10-15.md) for evidence and remaining gates. No upstream game source archive, media, game runtime or player is published by this experiment.
