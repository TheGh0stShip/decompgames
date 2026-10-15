// SPDX-License-Identifier: MIT
// Minimal function interface used by FE's PCX reader; no legacy pack structs.
#pragma once
using HFASTFILE = void*;
int FastFileInit(const char* logicalPackPath, int maxHandles);
void FastFileFini();
HFASTFILE FastFileOpen(const char* logicalName);
bool FastFileClose(HFASTFILE handle);
bool FastFileRead(HFASTFILE handle, void* destination, int bytes);
bool FastFileSeek(HFASTFILE handle, int offset, int origin);
