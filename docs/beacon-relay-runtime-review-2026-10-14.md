# Beacon Relay selected runtime review — October 14, 2026

The selected source/native dependency review now supports packaging the independently authored three-course source port with separate, retained permissive grants. This is an intake review of explicit inputs and build selections, not a legal opinion, all-MIT certificate, whole-.NET audit, clean-room certificate or native object-to-source rebuild. The [source snapshot](beacon-relay-runtime-source-review-2026-10-14.json) records exact pins, text hashes, packaged compiler properties and retained notice files. Gameplay/site/production acceptance remains separate.

## Framework and game are separate

NoelFB's included Classic.cs and our geometry/host/controller code have separate MIT grants. The release replaces six UI/content literals, including an unused expressive message, before compilation and source packaging; gameplay algorithms remain unchanged. Our maps, graphics/animation designs, font glyphs, palette and authored presentation text have a scoped CC0 dedication. Native gameplay/procedural effect algorithms remain author MIT code. No commercial Celeste engine, original Emulator.cs, XNA/FNA/Monocle binary, cartridge, Lua payload or retail media is selected.

The signed Microsoft.NETCore.App.Runtime.Mono.browser-wasm 9.0.20 package is hash-pinned independently. Its full MIT and broad third-party notice documents are retained. Its 23-assembly recursive metadata selection omits unused BCL libraries; source/build evidence is used to resolve native selections rather than assuming that this omission excludes all third-party native code.

## Compiler stamp and system libraries

Runtime recipe commit `3879076d9a06ce098d37c3882fb1845a6627335b` pins dotnet/emsdk `b2bf6cec0cb4ce281802ac3951bdd14287aad112`. That pins dotnet/emscripten `b9e76c96569596d11f72543f41985eb93b8fe45e`. The fork version file says `3.1.56-git`; the signed runtime's wasm-props.json reports version 3.1.56 and revision `57b21b8fdcbe3ebb523178b79465254668eab408`.

The latter revision is a fixed **base stamp**, not the exact fork commit: the fork's Transport.props copies `eng/emscripten-*.txt` into the SDK, `eng/emscripten-revision.txt` contains that older base revision, and emcc.py uses it when the Git checkout is omitted. The older upstream source identifies itself as 3.1.34-git. This resolves the apparent version/hash disagreement without treating the base stamp as a complete source identity. Exact fork provenance comes from the dependency recipe chain; the native runtime was reused from the signed package rather than rebuilt here.

Emscripten's MIT/NCSA grant, Node-derived path-code notice, musl's complete copyright/third-party notice, LLVM libc++/libc++abi/compiler-rt/libunwind Apache-2.0-with-LLVM-exceptions/legacy grants, Mono's runtime-wide notices and conservative native unwind notices are retained. dlmalloc's original public-domain/CC0 attribution and Emscripten modifications are identified separately. The selected packaged link response does not override the default allocator; source settings use dlmalloc. No SDK/compiler executables are shipped with the player. Build-tool licenses are retained conservatively without claiming that the entire tool is part of the runtime.

## ICU, compression, timezone and excluded XML data

The recipe pins dotnet/icu `9adc45770f79d8d0161ac8972a0036e36bd48ded`, with vendored ICU **68.2**. Its complete Unicode/ICU grant and included third-party terms are retained. No external ICU locale-data file is shipped. Invariant boot does not remove the already compiled native ICU code; no such absence claim is made.

Browser System.IO.Compression.Native selects zlib-ng under its zlib grant. Its Brotli source branch is excluded for browser/WASI by the pinned CMake conditions, while the package-wide .NET notices remain a conservative superset. No Brotli-permission inference is made from a directory merely being present.

System.Runtime.TimeZoneData comes from runtime-assets `12466630283f5e0fe1869b52184aece70d3967a4`; its project selects IANA **2026c**. The IANA public-domain data grant is retained separately. The date.c/newstrftime.3/strftime.c exceptions apply to named source files, which are not player files or the selected timezone-data bundle. Runtime-assets test collections, including its unrelated CC-BY-SA test material, are not selected or downloaded as runtime content.

The broad .NET notice file's ISO SGML-specific notice is reproduced exactly in System.Private.Xml's XHTML entity data. That project embeds those resources in System.Private.Xml.dll. Neither that DLL/resources nor an XML library is in this player's 23-assembly closure or selected native/browser link recipes. This supports exclusion for this selection; it does not relicense the XML material. Other broad notices, including the Apple-header acknowledgment, remain retained conservatively, and the product's credits include the Berkeley acknowledgment.

## Remaining limits

This selection retains full framework/ICU/system-library notices rather than relabeling dependencies MIT or CC0. No full native linker-map certificate, native framework/SDK rebuild or universal platform behavior is claimed. The framework package remains an implementation input reused byte-for-byte. The source rebuild covers the selected game assembly and packaged files. Only independently authored gameplay content is eligible for integration; ordinary private acceptance, loader-failure handling, source/archive reproduction and site/production checks must accompany any release.
