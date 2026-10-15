---
layout: ../../layouts/Article.astro
title: What’s new
description: Release notes and compatibility changes for Decomp Games.
---
## October 14, 2026 — Open Cadet: native launch-skill bonus verified

Unpaused muted keyboard play displayed Open Cadet's launch-skill bonus and a 7,500-point score. A separate read-only debugger run paired a native award with a 30,000-point score increase. The game package is unchanged, both players stopped with save synchronization, and exact plunger timing, all missions and full playthrough remain unverified. [Skill-shot evidence](https://github.com/andrewnakas/decompgames/blob/main/docs/open-cadet-skill-shot-production-test-2026-10-14.json). [Play Open Cadet](/games/open-cadet/).

## October 14, 2026 — Signal Survey: three stations in Rogue code

Retrieve a survey lens, then carry it back through three stations to the surface. Signal Survey runs native Rogue source with independently authored CC0 layouts, encounters, glyphs, names and messages. It requires no ROM or original media and is silent. Save and exit, Continue saved, New expedition and Stop are included. This is a source port with an original replacement campaign and does not advance the decompilation milestone. [Play Signal Survey](/games/signal-survey/).

## October 14, 2026 — Vector Duel: robot rounds in GLFighters code

Spar with a gold robot on the original Foundry Deck arena, then switch to an attacking opponent. Vector Duel runs permission-backed GLFighters source through SDL/WebAssembly with independently authored CC0 meshes, motion, pixels, glyphs and arena content. It needs no ROM or original game media and is intentionally silent. Completed-round journals persist between browser sessions; unfinished matches restart. This is a source port and does not count toward the decompilation milestone. [Play Vector Duel](/games/vector-duel/).

## October 14, 2026 — Beacon Relay: three original courses in Celeste Classic code

Guide a service rover through three original courses, collect lights and reach the beacons. Beacon Relay runs developer-released Celeste Classic C# code in the Mono WebAssembly runtime with independently authored CC0 graphics, animation, glyphs, text and maps. It needs no original game files and is intentionally silent. Course checkpoints, Pause, New relay and Stop are included. This source port does not count toward the decompilation milestone. [Play Beacon Relay](/games/beacon-relay/).

## October 14, 2026 — Open Skyways: all thirty authored roads verified

Muted production keyboard play completed the thirty-road CC0 campaign and reached The End. All native completion markers survived a full browser close and relaunch. The game package is unchanged, and both players stopped with save synchronization and closed. All off-center collision/death cases, long-term balance and other browsers/devices remain unverified. [Campaign evidence](https://github.com/andrewnakas/decompgames/blob/main/docs/open-skyways-campaign-production-test-2026-10-14.json). [Play Open Skyways](/games/skyways/).

## October 14, 2026 — Open Paths: all six authored levels verified

Muted production testing completed the full six-level CC0 navigation campaign through ordinary keyboard input. Native completion states and the all-levels-completed flag survived a full browser close and relaunch. The runtime is unchanged, and both test players stopped with save synchronization and closed. This covers the authored replacement campaign; other browsers and rapid-close save durability remain unverified. [Campaign evidence](https://github.com/andrewnakas/decompgames/blob/main/docs/open-paths-campaign-production-test-2026-10-14.json). [Play Open Paths](/games/supaplex/).

## October 14, 2026 — Open Cadet: live native flipper contacts observed

Read-only debugger stepping in Open Cadet's unchanged live WASM recorded eight ball/flipper contacts, with velocity changes and speed increases on both native flipper components. Tests stayed muted and the player stopped with save synchronization. Debugger pauses affect timing; calibrated forces, every contact case and a full playthrough remain unverified. [Contact evidence](https://github.com/andrewnakas/decompgames/blob/main/docs/open-cadet-contacts-production-test-2026-10-14.json). [Play Open Cadet](/games/open-cadet/).

## October 14, 2026 — Open Cadet: live flipper controls verified

Open Cadet’s live player now has verified Z and / flipper response, individually and together, with exact return on release. Tests stayed muted and used ordinary keyboard input before launch. The runtime is unchanged; earlier earned-score and browser-restart save verification remains valid. Later same-day native contact evidence appears above; all missions and a full playthrough remain unverified. [Play Open Cadet](/games/open-cadet/).

## October 14, 2026 — Paper Rooms: five original flights in Glider 4 code

Guide a folded flyer through five original rooms, follow the air columns and collect sun tokens. Paper Rooms runs developer-released Glider 4 flight code translated to JavaScript, with independently authored CC0 rooms, procedural graphics, animation and text. It needs no original game files and starts silent. Room checkpoints, Pause, New flight and Stop are included. This is a source port with original content and does not count toward the decompilation milestone. [Play Paper Rooms](/games/paper-rooms/).

## October 14, 2026 — Beacon Yard: a courtyard in the Eldritch engine

Activate three beacons and return to the exit terminal in an original courtyard built on developer-released Eldritch code. Beacon Yard uses independently authored replacement art, glyphs, animation, text and map, with no original game files required. This silent source port includes Pause, Save, Restore, New yard and Stop. Muted tests completed the challenge and restored native progress after a browser restart. It is an original challenge, not the retail campaign or a matching decompilation. [Play Beacon Yard](/games/beacon-yard/).

## October 13, 2026 — Cinder: an authored challenge in the Abuse engine

Cinder ports the developer-released Abuse engine to WebAssembly with independently authored CC0 graphics, glyphs, animation, text, rules and two heat courses. It is a silent source port with new content, not retail Abuse or a matching decompilation. Muted local tests covered both exits, death/retry, jump avoidance, and a damaged native save restored after a full browser restart. Broader save failure cases and other devices remain unverified. [Play Cinder](/games/cinder-abuse/).

## October 10, 2026 — Skate 3: online rooms, community maps, regenerated geometry

The Skate 3 clean-room build now has multiplayer: open a private room and send the invite link, or a public room that anyone can join from the Multiplayer menu, for up to ten skaters on the same map. The map picker lists community maps published on skatemods.com and opens `.skate` files from your own disk. The visual geometry of every park and the skater is now regenerated like the textures and sounds, and a ninth park, built from Kenney's CC0 Mini Skate kit, has been added. Multiplayer has only been checked between two test browsers so far. [Play Skate 3](/games/skate-3/).

## October 1, 2026 — Clean-room builds and a new design

The catalogue now leads with 17 clean-room builds: 16 Nintendo 64 games and Skate 3. Each runs decompiled or rewritten game code with regenerated assets and plays in place on its game page, with gamepad support. The site has been redesigned around the game grid, and link-only directory entries have been removed. [How the clean room works](/clean-room/).

## September 27, 2026 — Open Junction is playable

Open Junction pairs the documented reSL decompilation with independently authored CC0 art, interface, and six-station scenario data. The pinned WebAssembly build excludes original game resources and uses a null audio backend. Muted private tests covered player-built rails, switch routing, natural train deliveries, Save/Archive, and six-station cases. The deployed package passed a natural completed-train delivery and a save export/delete/import/restore cycle in an isolated, silent browser test. Uninterrupted 1800–2000 progression and the repeat-level campaign remain unverified. [Play Open Junction](/games/shortline/).

## September 22, 2026 — Open Paths is playable

Open Paths combines the documented OpenSupaplex decompilation with six original CC0 navigation mazes and independently generated graphics, screens, fonts, palettes, and panel data. The null-audio WebAssembly build passed muted local and production tests for launch, menu input, player creation, movement, first-level completion, fresh-start progress, and backup export/delete/import restoration. At this September checkpoint, the full six-level playthrough remained unverified; the October 14 record above verifies the authored campaign.

## September 22, 2026 — Open Digger is playable

Open Digger combines the documented Digger Remastered decompilation with eight new levels and independently generated CC0 graphics, font, title, and icon data. The no-audio browser build passed muted launch, input, collection, scoring, first-level completion, second-level enemy and death/restart checks, origin-local storage reload, and the live Decomp Games player flow. The game page states the exact tested scope.

## September 18, 2026 — Building the first collection

The first catalog brings decompilations, engine recreations, and released-source ports into one searchable collection. Game pages separate asset requirements from engine licenses and publish explicit verification records.

The browser player and initial integrations are in development. The public-release gate is eight complete instant-play titles, two local-import integrations, and 30 substantive project entries. Check individual game pages for current availability and test scope.
