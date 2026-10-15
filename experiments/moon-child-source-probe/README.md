# Moon Child FE source-only build probe

This experiment records source feasibility for an original-developer source port. It is **not a playable release, a new catalog entry, a decompilation or a clean-room certificate**.

Game/FE code: MIT declarations from the original programmer and selected FE repository. Original media is excluded. The original author currently declares CC BY-NC-SA for non-code assets, while FE lists CC BY-NC; neither declaration is treated as CC0 or permission to ship a replacement campaign's missing content. See the [source intake](../../docs/moonchild-gnukem-chromium-source-intake-2026-10-14.md).

`source-inputs.json` contains 221 pinned text-file paths, URLs, hashes and lengths: selected FE code/build text and the exact pl_mpeg header from FE's gitlink. It contains no game data. Populate a source directory with those exact listed text files, retaining paths; do not copy the original `Data` directory. The recipe checks every recorded input before compiling, uses the installed SDK's SDL2/zlib ports, and does not fetch dependencies or run a player.

```text
python build.py --source SOURCE_DIRECTORY --output NEW_OUTPUT_DIRECTORY --emscripten EMSCRIPTEN_DIRECTORY --em-config EMSCRIPTEN_CONFIG
```

The exact SDK used was Emscripten 6.0.10. The selected upstream CMake source lists supply 91 translation units for the SDL2/GLES2 choice. The probe changes no source files, omits original-data/controller-database preloads, uses `-O0` and strict unresolved-symbol rejection, and sets `INVOKE_RUN=0`. It is a custom direct compiler selection, not a claim that the unmodified upstream CMake package built without data or vendored dependencies. Audio code remains compiled; **do not run this artifact** before a null-audio adaptation and content review.

Two separate output directories produced identical 91 objects and identical JS/WASM bytes. WASM validation passed without instantiation or a call to main. The installed SDK libraries were used, not independently rebuilt/audited here. This is not yet a portable corresponding-source release or a package license-closure certificate.

Release gates remain: independent graphics, animation, text, maps and other expressive content with a provenance manifest; a null-audio selection; exact GLAD/generated-header and selected SDK/runtime notices; retained source-content audit; ordinary gameplay, objectives, damage/death/retry, saves and Stop; then source packaging and production verification. No runtime or source archive is published by this experiment.
