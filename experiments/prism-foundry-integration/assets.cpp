// SPDX-License-Identifier: MIT
// Authored transactional parser for the selected S/A/E descriptor profile.
// It retains actual native sprite construction/PCX decoding after validation.
#include "frm_wrk.hpp"
#include "asset.hpp"
#include "anim.hpp"
#include "globals.hpp"
#include <cctype>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <string>
#include <vector>

namespace {
std::string trim(const std::string& value)
{
    const auto first=value.find_first_not_of(" \t\r\n");
    if (first==std::string::npos) return "";
    return value.substr(first,value.find_last_not_of(" \t\r\n")-first+1);
}
bool quoted(const std::string& input,std::string& result)
{
    const std::string value=trim(input);
    if (value.size()<3 || value.front()!='"' || value.back()!='"') return false;
    result=value.substr(1,value.size()-2);
    if (result.empty() || result.size()>127) return false;
    for (unsigned char byte:result) if (byte<32 || byte>=127 || byte=='"') return false;
    return true;
}
char* copyName(const std::string& name)
{
    char* result=static_cast<char*>(std::malloc(name.size()+1));
    if (result) std::memcpy(result,name.c_str(),name.size()+1);
    return result;
}
unsigned little16(const unsigned char* value) { return value[0]|(unsigned(value[1])<<8); }

bool validFrameFile(const std::string& name,size_t budget,size_t& pixels)
{
    // The retained Cblitbuf constructor has a 100-byte diagnostic buffer.
    if (name.size()>80) return false;
    HFASTFILE file=FastFileOpen(name.c_str());
    if (!file) return false;
    unsigned char header[128],byte,value,palette[768];
    bool valid=FastFileRead(file,header,128);
    unsigned width=0,height=0;
    if (valid) {
        width=little16(header+8)+1;height=little16(header+10)+1;
        valid=header[0]==10 && header[2]==1 && header[3]==8 && header[65]==1
            && little16(header+4)==0 && little16(header+6)==0
            && width>0 && width<=2048 && height>0 && height<=4096
            && width%2==0 && little16(header+66)==width
            && static_cast<size_t>(width)*height<=budget;
    }
    size_t remaining=static_cast<size_t>(width)*height;
    while (valid && remaining>0) {
        valid=FastFileRead(file,&byte,1);
        if (!valid) break;
        unsigned count=1;
        if (byte>=192) {
            count=byte&63;
            valid=count>0 && FastFileRead(file,&value,1);
        }
        valid=valid && count<=remaining;
        if (valid) remaining-=count;
    }
    valid=valid && FastFileRead(file,&byte,1) && byte==12
        && FastFileRead(file,palette,768) && !FastFileRead(file,&byte,1);
    FastFileClose(file);
    if (valid) pixels=static_cast<size_t>(width)*height;
    return valid;
}

struct Pending {
    std::vector<Cspr_frame*> frames;
    std::vector<SEQUENCE*> sequences;
    std::vector<ANIM*> animations;
    bool committed=false;
    ~Pending() {
        if (committed) return;
        for (auto* item:animations) { std::free(item->name);std::free(item); }
        for (auto* item:sequences) { std::free(item->name);std::free(item); }
        for (auto* item:frames) delete item;
    }
    SEQUENCE* findSequence(const std::string& name) {
        for (auto* item:sequences) if (name==item->name) return item;
        return nullptr;
    }
    bool nameUsed(const std::string& name,bool animation) {
        if (animation) {
            for (auto* item:animations) if (name==item->name) return true;
        } else if (findSequence(name)) return true;
        return false;
    }
};
}

int asset_parse(const char* filename)
{
    if (!filename || !allframes || !allsequences || !allanims) return 0;
    // The transaction requires an empty target. It never replaces live content.
    if (vg_dll_count(allframes) || vg_dll_count(allsequences) || vg_dll_count(allanims)) return 0;
    std::ifstream input(filename,std::ios::binary);
    if (!input) return 0;
    input.seekg(0,std::ios::end);
    const auto length=input.tellg();
    if (length<0 || length>256*1024) return 0;
    input.seekg(0,std::ios::beg);
    if (!input) return 0;
    Pending pending;
    std::vector<Cspr_frame*> sequenceFrames;
    std::string sequenceName,line;
    ANIM* animation=nullptr;
    int mode=0,slots=0;
    bool ended=false;
    size_t spritePixels=0,descriptorBytes=0;
    constexpr size_t MaxSpritePixels=16*1024*1024;
    auto closeContext=[&]() -> bool {
        if (mode==1) {
            if (sequenceFrames.empty() || pending.sequences.size()>=256) return false;
            SEQUENCE* sequence=static_cast<SEQUENCE*>(std::calloc(1,sizeof(SEQUENCE)+sizeof(void*)*sequenceFrames.size()));
            if (!sequence) return false;
            sequence->name=copyName(sequenceName);
            if (!sequence->name) { std::free(sequence);return false; }
            sequence->nrofsteps=static_cast<UINT16>(sequenceFrames.size());
            for (size_t i=0;i<sequenceFrames.size();++i) sequence->frame[i]=sequenceFrames[i];
            pending.sequences.push_back(sequence);sequenceFrames.clear();
        } else if (mode==2) {
            if (!animation || slots==0) return false;
            animation->cursequence=0;animation->maxstep=animation->sequences[0]->nrofsteps;
        }
        mode=0;return true;
    };
    while (std::getline(input,line)) {
        descriptorBytes+=line.size()+1;
        if (descriptorBytes>256*1024) return 0;
        if (line.size()>250) return 0;
        const std::string clean=trim(line);
        if (clean.empty() || clean[0]=='#') continue;
        if (ended) return 0;
        const bool indented=!line.empty() && std::isspace(static_cast<unsigned char>(line[0]));
        if (indented) {
            std::string name;
            if (!quoted(clean,name)) return 0;
            if (mode==1) {
                size_t pixels=0;
                if (sequenceFrames.size()>=100 || pending.frames.size()>=4096
                    || !validFrameFile(name,MaxSpritePixels-spritePixels,pixels)) return 0;
                Cspr_frame* frame=new Cspr_frame(const_cast<char*>(name.c_str()),0,0,0);
                spritePixels+=pixels;
                pending.frames.push_back(frame);sequenceFrames.push_back(frame);
            } else if (mode==2) {
                if (slots>=MAXSEQUENCES) return 0;
                SEQUENCE* sequence=pending.findSequence(name);
                if (!sequence) return 0;
                animation->sequences[slots++]=sequence;
            } else return 0;
        } else {
            if (!closeContext()) return 0;
            if (clean=="E") { ended=true;continue; }
            if (clean.size()<3 || (clean[0]!='S' && clean[0]!='A') || !std::isspace(static_cast<unsigned char>(clean[1]))) return 0;
            std::string name;
            if (!quoted(clean.substr(1),name) || pending.nameUsed(name,clean[0]=='A')) return 0;
            if (clean[0]=='S') { mode=1;sequenceName=name; }
            else {
                if (pending.animations.size()>=256) return 0;
                animation=static_cast<ANIM*>(std::calloc(1,sizeof(ANIM)));
                if (!animation) return 0;
                animation->name=copyName(name);
                if (!animation->name) { std::free(animation);return 0; }
                pending.animations.push_back(animation);slots=0;mode=2;
            }
        }
    }
    if (!ended || pending.animations.empty() || input.bad()) return 0;
    for (auto* item:pending.frames) vg_dll_add(allframes,item,VG_DLL_LAST);
    for (auto* item:pending.sequences) vg_dll_add(allsequences,item,VG_DLL_LAST);
    for (auto* item:pending.animations) vg_dll_add(allanims,item,VG_DLL_LAST);
    pending.committed=true;
    return 1;
}

void asset_removeall()
{
    if (allframes) {
        while (vg_dll_first(allframes)) {
            delete static_cast<Cspr_frame*>(vg_dll_collect(allframes));vg_dll_remcur(allframes);
        }
        vg_dll_free(allframes);allframes=nullptr;
    }
    if (allsequences) {
        while (vg_dll_first(allsequences)) {
            auto* item=static_cast<SEQUENCE*>(vg_dll_collect(allsequences));
            std::free(item->name);std::free(item);vg_dll_remcur(allsequences);
        }
        vg_dll_free(allsequences);allsequences=nullptr;
    }
    if (allanims) {
        while (vg_dll_first(allanims)) {
            auto* item=static_cast<ANIM*>(vg_dll_collect(allanims));
            std::free(item->name);std::free(item);vg_dll_remcur(allanims);
        }
        vg_dll_free(allanims);allanims=nullptr;
    }
}
