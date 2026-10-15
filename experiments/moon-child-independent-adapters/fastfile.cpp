// SPDX-License-Identifier: MIT
// New loose-file reader. It does not parse mc.art, FFCREATE directories or .rz.
// Interface/usage were inspected in FE. No clean-room isolation is claimed.
#include "fastfile.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>

namespace {
constexpr size_t MaxFileBytes = 16 * 1024 * 1024;
constexpr char Marker[] = "DecompGames Moon FE independent content v1\n";
struct Slot {
    bool open = false;
    size_t cursor = 0;
    std::vector<unsigned char> bytes;
};
std::vector<Slot> slots;
std::string directory;

Slot* findSlot(HFASTFILE handle)
{
    for (auto& slot : slots)
        if (handle == &slot && slot.open) return &slot;
    return nullptr;
}

bool basename(const char* logicalName, std::string& result)
{
    if (!logicalName) return false;
    const std::string name(logicalName);
    if (name.empty() || name.size() > 255 || name[0] == '/' || name[0] == '\\'
        || name.find(':') != std::string::npos || name.find("..") != std::string::npos)
        return false;
    const auto separator = name.find_last_of("/\\");
    result = name.substr(separator == std::string::npos ? 0 : separator + 1);
    if (result.empty() || result.size() > 127 || result == ".") return false;
    for (char& c : result) {
        if (c >= 'A' && c <= 'Z') c = char(c + ('a' - 'A'));
        if (!((c >= 'a' && c <= 'z') || (c >= '0' && c <= '9')
            || c == '.' || c == '_' || c == '-')) return false;
    }
    return true;
}
}

void FastFileFini()
{
    slots.clear();
    directory.clear();
}

int FastFileInit(const char* logicalPackPath, int maxHandles)
{
    FastFileFini();
    if (!logicalPackPath || maxHandles < 1 || maxHandles > 256) return 0;
    const std::string path(logicalPackPath);
    const auto separator = path.find_last_of("/\\");
    const std::string parent = separator == std::string::npos ? "./" : path.substr(0, separator + 1);
    FILE* marker = std::fopen((parent + "loose-content.marker").c_str(), "rb");
    if (!marker) return 0;
    char contents[sizeof(Marker)] = {};
    const size_t count = std::fread(contents, 1, sizeof(contents), marker);
    const bool valid = !std::ferror(marker) && count == sizeof(Marker) - 1
        && std::memcmp(contents, Marker, sizeof(Marker) - 1) == 0;
    std::fclose(marker);
    if (!valid) return 0;
    directory = parent;
    slots.resize(static_cast<size_t>(maxHandles));
    return 1;
}

HFASTFILE FastFileOpen(const char* logicalName)
{
    std::string name;
    if (directory.empty() || !basename(logicalName, name)) return nullptr;
    Slot* available = nullptr;
    for (auto& slot : slots) if (!slot.open) { available = &slot; break; }
    if (!available) return nullptr;
    FILE* input = std::fopen((directory + name).c_str(), "rb");
    if (!input) return nullptr;
    bool valid = std::fseek(input, 0, SEEK_END) == 0;
    const long length = valid ? std::ftell(input) : -1;
    valid = length >= 0 && static_cast<uint64_t>(length) <= MaxFileBytes
        && std::fseek(input, 0, SEEK_SET) == 0;
    std::vector<unsigned char> bytes;
    if (valid) {
        bytes.resize(static_cast<size_t>(length));
        valid = (bytes.empty() || std::fread(bytes.data(), 1, bytes.size(), input) == bytes.size())
            && !std::ferror(input);
    }
    std::fclose(input);
    if (!valid) return nullptr;
    available->bytes.swap(bytes);
    available->cursor = 0;
    available->open = true;
    return available;
}

bool FastFileClose(HFASTFILE handle)
{
    Slot* slot = findSlot(handle);
    if (!slot) return false;
    slot->open = false;
    slot->cursor = 0;
    std::vector<unsigned char>().swap(slot->bytes);
    return true;
}

bool FastFileRead(HFASTFILE handle, void* destination, int bytes)
{
    Slot* slot = findSlot(handle);
    if (!slot || bytes < 0 || (bytes > 0 && !destination)) return false;
    const size_t count = static_cast<size_t>(bytes);
    if (count > slot->bytes.size() - slot->cursor) return false;
    if (count) std::memcpy(destination, slot->bytes.data() + slot->cursor, count);
    slot->cursor += count;
    return true;
}

bool FastFileSeek(HFASTFILE handle, int offset, int origin)
{
    Slot* slot = findSlot(handle);
    if (!slot) return false;
    int64_t base;
    if (origin == SEEK_SET) base = 0;
    else if (origin == SEEK_CUR) base = static_cast<int64_t>(slot->cursor);
    else if (origin == SEEK_END) base = static_cast<int64_t>(slot->bytes.size());
    else return false;
    const int64_t next = base + static_cast<int64_t>(offset);
    if (next < 0 || static_cast<uint64_t>(next) > slot->bytes.size()) return false;
    slot->cursor = static_cast<size_t>(next);
    return true;
}
