---
layout: ../layouts/Article.astro
title: Asset provenance and clean-room claims
description: How we distinguish replacement media, retained game content, source licensing, and evidence of independent implementation.
---
A project name containing “cleanroom” does not establish how its code or content was created. Each game page describes the evidence available for that particular build. Some older external projects regenerate selected media while retaining game code, geometry, animation, text or music sequences.

## Code and content are separate

A source licence must cover the code being distributed, including dependencies. A permissive licence for a browser wrapper or port layer does not establish permission for reconstructed game code, embedded SDK code or the game's content.

Content review includes graphics, models, animation, audio, text, maps and expressive data embedded in source files. Replacing textures and sound samples leaves the other categories to be checked. A free download or a public repository is not a complete redistribution licence.

## Independently authored replacements

For audited replacement packs, we record the authorship, licence, source inputs and file inventory. Licensed CC0 media can be used where its provenance is documented; separately licensed fonts and dependencies retain their own notices. Retained game content is disclosed rather than described as wholly original replacement content.

## What a comparison can establish

A byte comparison can find shared data in the files it examines. Passing it does not establish independent authorship, permission to redistribute, or separation between researchers and implementers. Colour grids, silhouettes, geometry and music sequences require their own provenance review even when generated output has different bytes.

## Browser builds and ROMs

Some external players load a ROM supplied by their hosting site. Playing without uploading your own ROM does not establish that the distribution is ROM-free. A decompilation-built ROM can still run through an emulator; that is different from compiling the game directly to WebAssembly.

## Verification limits

We do not certify formal clean-room isolation without evidence of the process and information boundaries. Gameplay testing, source licensing, asset provenance and runtime classification are separate checks. Startup is not a completed gameplay test, and a short gameplay test is not a full playthrough.

Each game page links its source and states its requirements, limitations and verification scope. Existing entries with unresolved provenance remain part of the broader classic collection; they are not counted as new audited permissive, ROM-free releases.
