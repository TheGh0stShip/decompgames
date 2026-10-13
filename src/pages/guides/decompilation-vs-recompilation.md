---
layout: ../../layouts/Article.astro
title: Decompilation, recompilation, or source port?
description: The differences between decompiled games, recompilations, engine recreations, and released-source ports.
---
These projects can all keep an old game playable, but they get there in different ways. We label each catalog entry so the wider collection does not inflate the number of actual decompilations.

## Decompilation

Developers reconstruct source code from an existing executable. Some projects aim to reproduce the original binary exactly; others prioritize readable, portable code. The reconstructed engine may still require original game data. [Super Mario 64](/games/super-mario-64/) is a useful starting point for understanding this distinction.

## Recompilation

A recompilation translates the original program into code that runs on a different system, often combining generated code with a runtime and patches. This can preserve behavior without manually reconstructing every function. It does not remove the need for the original game content.

## Engine recreation

A recreation implements compatible behavior with a new engine. [ScummVM](/?c=adventure) reads adventure-game data using its own implementations. Compatibility depends on both the specific game and its edition.

## Released-source port

The original developers released source code and a community adapted it to new platforms. [Doom](/games/doom/) is an example. The source license and the commercial game-data license are separate.

## Where emulation fits

An emulator reproduces a machine’s behavior so original software can run. It is valuable preservation work, but an ordinary emulated game is not counted as a decompilation here. For a broader browser-emulation collection, visit [ExeBrowser](https://exebrowser.com/).

A decompilation can also produce a console ROM that runs through an emulator. In that case, the source project is a decompilation and the browser execution is emulation; it is not a native WebAssembly game port. A modified retail ROM with replacement media is classified as emulation when this distribution does not establish a source rebuild. Having a ROM supplied by the hosting site does not make the distribution ROM-free.
