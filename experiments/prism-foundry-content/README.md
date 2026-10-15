# Prism Foundry authored-content experiment

Three independently authored course specifications and indexed art for the developer-source Moon Child FE port. **Content/parser groundwork only: no game integration, startup or gameplay result.** This is not a new decompilation or catalog entry.

The generator reads no original media, screenshots, fonts, maps, animation data or story text. Functional format/interface names were inspected in the pinned upstream source. All new graphics, animation poses, palette, block glyphs, maps, placement specifications and original text are dedicated under the scoped [CC0 declaration](CC0.txt). The full Creative Commons legal code is included separately and identified as a license document in the manifest. Generator/test code uses [MIT](LICENSE). None of this relicenses upstream game code or dependencies, or certifies clean-room isolation.

```text
python generate.py --output NEW_PACK_DIRECTORY
python verify-native.py --pack PACK_DIRECTORY --build ADAPTER_BUILD_DIRECTORY --output NEW_TEST_DIRECTORY --emscripten EMSCRIPTEN_DIRECTORY --em-config EMSCRIPTEN_CONFIG --node NODE_EXECUTABLE
python preview.py --output PREVIEW.png
```

First create the [88-unit adapted source build](../moon-child-independent-adapters/README.md). The verifier uses its actual compiled objects and retained upstream headers; it replaces only the application main with a Node-only test harness. It initializes no game Host, loop, video or audio. It checks the pack against its provenance hashes and compares actual native PCX pixels/palettes, native animation slots, map-file reads and collision-grid sampling. The optional preview uses Pillow and is clearly labeled as an art/geometry preview.

The generated pack has 276 listed files, 469,902 bytes, plus `provenance.json`. It contains 265 PCX images, native animation descriptors, three tile maps and three collision grids, course/placement/goal text, and notices. No music, effects or movies are present; null audio is required. A second generation matched all 277 files including the manifest. [Pinned generated manifest](provenance.json); [measured checkpoint](../../docs/prism-foundry-content-2026-10-15.md).

The intended three-prism gate objectives and all course routes remain **untested gameplay specifications**. Safe game initialization, source-side level/placement/trigger selection, remaining expressive UI/story/font/animation tables, runtime objective/save/retry/Stop behavior, full notice/source packaging and muted live verification remain before release. Twelve animation names needed for this initial content path are supplied; other native animation IDs are absent. Do not load unrelated original levels or present this pack as the complete original campaign.
