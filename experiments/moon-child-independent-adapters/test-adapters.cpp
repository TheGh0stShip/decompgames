// SPDX-License-Identifier: MIT
#include "fastfile.h"
#include "NullAudio.h"
#include <cassert>
#include <cstdio>
#include <cstring>
#include <climits>
#include <initializer_list>
#include <vector>
#include <sys/stat.h>
#include "mydefs.hpp"
#include "pcxff.hpp"

static void writeFile(const char* name, const char* data)
{
    FILE* file = std::fopen(name, "wb");
    assert(file);
    const size_t length = std::strlen(data);
    assert(std::fwrite(data, 1, length, file) == length);
    assert(std::fclose(file) == 0);
}

int main()
{
    mkdir("authored", 0700);
    writeFile("authored/mc.art", "not a content marker");
    assert(!FastFileInit("authored/mc.art", 2));
    writeFile("authored/loose-content.marker", "DecompGames Moon FE independent content v1\nextra");
    assert(!FastFileInit("authored/mc.art", 2));
    writeFile("authored/loose-content.marker", "DecompGames Moon FE independent content v1\n");
    assert(!FastFileInit("authored/mc.art", 0));
    assert(!FastFileInit("authored/mc.art", 257));
    assert(!FastFileInit(nullptr, 2));
    writeFile("authored/a.pcx", "0123456789");
    writeFile("authored/b.pcx", "abcdef");
    writeFile("authored/empty.pcx", "");
    assert(FastFileInit("authored/mc.art", 2));
    for (const char* bad : {"", ".", "../a.pcx", "a/../../a.pcx", "/a.pcx", "C:a.pcx", "a?.pcx", "missing.pcx"})
        assert(!FastFileOpen(bad));
    assert(!FastFileOpen(nullptr));
    auto a = FastFileOpen("assets\\A.PCX");
    auto b = FastFileOpen("b.pcx");
    assert(a && b && a != b);
    assert(!FastFileOpen("empty.pcx"));
    char buffer[16] = {};
    assert(FastFileRead(a, buffer, 3) && std::memcmp(buffer, "012", 3) == 0);
    assert(FastFileRead(b, buffer, 2) && std::memcmp(buffer, "ab", 2) == 0);
    assert(!FastFileRead(a, buffer, 8));
    assert(FastFileRead(a, buffer, 2) && std::memcmp(buffer, "34", 2) == 0);
    assert(!FastFileRead(a, nullptr, 1));
    assert(!FastFileRead(a, buffer, -1));
    assert(!FastFileSeek(a, INT_MIN, SEEK_CUR));
    assert(!FastFileSeek(a, INT_MAX, SEEK_END));
    assert(!FastFileSeek(a, 0, 123));
    assert(FastFileRead(a, buffer, 1) && buffer[0] == '5');
    assert(FastFileSeek(a, -2, SEEK_END));
    assert(FastFileRead(a, buffer, 2) && std::memcmp(buffer, "89", 2) == 0);
    assert(!FastFileRead(a, buffer, 1));
    assert(FastFileRead(a, nullptr, 0));
    assert(FastFileSeek(a, 0, SEEK_SET));
    assert(FastFileSeek(a, 10, SEEK_CUR));
    assert(FastFileClose(a));
    assert(!FastFileClose(a) && !FastFileRead(a, buffer, 1));
    assert(FastFileRead(b, buffer, 2) && std::memcmp(buffer, "cd", 2) == 0);
    auto empty = FastFileOpen("empty.pcx");
    assert(empty && FastFileRead(empty, nullptr, 0) && FastFileSeek(empty, 0, SEEK_END));
    assert(!FastFileRead(empty, buffer, 1));
    assert(!FastFileClose(nullptr) && !FastFileSeek(nullptr, 0, SEEK_SET));
    FastFileFini();
    assert(!FastFileRead(b, buffer, 1) && !FastFileOpen("a.pcx"));
    assert(FastFileInit("authored/mc.art", 1));
    FILE* oversized = std::fopen("authored/oversize.pcx", "wb");
    assert(oversized && std::fseek(oversized, 16 * 1024 * 1024, SEEK_SET) == 0);
    assert(std::fputc(0, oversized) != EOF && std::fclose(oversized) == 0);
    assert(!FastFileOpen("oversize.pcx"));
    assert(!FastFileInit("missing/mc.art", 1) && !FastFileOpen("a.pcx"));
    // Original test pixels and palette; no original game media or reference art.
    std::vector<unsigned char> pcx(128, 0);
    pcx[0] = 10; pcx[1] = 5; pcx[2] = 1; pcx[3] = 8;
    pcx[8] = 7; pcx[10] = 3; pcx[65] = 1; pcx[66] = 8;
    for (int y = 0; y < 4; ++y) {
        pcx.push_back(0xc4); pcx.push_back(static_cast<unsigned char>(y + 1));
        pcx.push_back(0xc4); pcx.push_back(static_cast<unsigned char>(200 + y));
    }
    pcx.push_back(12);
    for (int i = 0; i < 768; ++i) pcx.push_back(static_cast<unsigned char>(i % 256));
    FILE* image = std::fopen("authored/probe.pcx", "wb");
    assert(image && std::fwrite(pcx.data(), 1, pcx.size(), image) == pcx.size());
    assert(std::fclose(image) == 0 && FastFileInit("authored/mc.art", 2));
    UINT16 width = 0, height = 0;
    assert(PCX_ff_stat("probe.pcx", &width, &height) == VG_TRUE && width == 8 && height == 4);
    BYTE pixels[32] = {}, palette[768] = {};
    assert(PCX_ff_load("probe.pcx", pixels, palette) == VG_TRUE);
    for (int y = 0; y < 4; ++y) for (int x = 0; x < 8; ++x)
        assert(pixels[y * 8 + x] == static_cast<BYTE>(x < 4 ? y + 1 : 200 + y));
    for (int i = 0; i < 768; ++i) assert(palette[i] == static_cast<BYTE>(i % 256));
    FastFileFini();
    NullAudio audio;
    assert(audio.Init());
    const auto sound = audio.CreateSound(-1, INT_MAX);
    audio.PlayOneShot(sound, INT_MAX, INT_MIN);
    audio.PlayLoop(sound, 0, 0);
    audio.SetVolume(sound, 1); audio.SetPan(sound, 1);
    audio.StopCurrent(sound); audio.StopSound(sound);
    assert(!audio.PlayMusic(1) && !audio.OpenMovieStream(44100, 2));
    audio.SubmitMovieAudio(nullptr, INT_MAX);
    audio.CloseMovieStream(); audio.StopMusic();
    audio.DestroySound(sound); audio.Reset(); audio.Destroy(); audio.Destroy();
    std::puts("PASS: loose-file boundaries, isolated handles, fail-closed marker, file cap, native PCX decode and null-audio API");
}
