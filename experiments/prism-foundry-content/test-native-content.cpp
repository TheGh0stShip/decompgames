// SPDX-License-Identifier: MIT
// This executes native file/animation/collision functions, never Host/main-loop.
#include "frm_wrk.hpp"
#include "asset.hpp"
#include "anim.hpp"
#include "globals.hpp"
#include "editor.hpp"
#include "Resources.h"
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>
#include <emscripten.h>

static uint32_t fnv(const unsigned char* bytes, size_t size)
{
    uint32_t hash=2166136261u;
    for (size_t i=0;i<size;++i) hash=(hash^bytes[i])*16777619u;
    return hash;
}

int main()
{
    assert(FastFileInit("/data/mc.art",16));
    FILE* expected=std::fopen("/expected-images.txt","r");
    assert(expected);
    char name[128]; unsigned w,h; uint32_t hash,paletteHash;
    int images=0;
    while (std::fscanf(expected,"%127s %u %u %u %u",name,&w,&h,&hash,&paletteHash)==5) {
        UINT16 actualW=0,actualH=0;
        assert(PCX_ff_stat(name,&actualW,&actualH)==VG_TRUE);
        assert(w==actualW && h==actualH);
        std::vector<BYTE> pixels(w*h),palette(768);
        assert(PCX_ff_load(name,pixels.data(),palette.data())==VG_TRUE);
        assert(fnv(pixels.data(),pixels.size())==hash);
        assert(fnv(palette.data(),palette.size())==paletteHash);
        // Hash the actual native-decoded WASM buffers with Node's SHA-256.
        EM_ASM({
            const crypto=require('node:crypto');
            const pixelHash=crypto.createHash('sha256').update(HEAPU8.subarray($0,$0+$1)).digest('hex');
            const paletteHash=crypto.createHash('sha256').update(HEAPU8.subarray($3,$3+$4)).digest('hex');
            console.log('NATIVE_IMAGE '+UTF8ToString($2)+' '+pixelHash+' '+paletteHash);
        },pixels.data(),pixels.size(),name,palette.data(),palette.size());
        ++images;
    }
    assert(images==265 && std::feof(expected)); std::fclose(expected);
    allframes=vg_dll_create(1);allsequences=vg_dll_create(1);allanims=vg_dll_create(1);
    assert(asset_parse("/data/foundry.des"));
    assert(vg_dll_count(allframes)==258);
    assert(vg_dll_count(allsequences)==32);
    assert(vg_dll_count(allanims)==12);
    int animationSlots=0;
    const char* animationNames[]={"moonchild","moonrise","skidcloud","bullet1","bump","explosion","heart","smallheart","diamond","glim","endoflevel","cyfers"};
    for (const char* animationName:animationNames) {
        ANIM* animation=anim_retrieveanim(animationName);assert(animation);
        const int steps=std::strcmp(animationName,"cyfers")==0 ? 10:8;
        for (int sequence=0;sequence<21;++sequence) {
            auto frame=anim_setsequence(animation,sequence,SEQ_FORCE);assert(frame);
            assert(animation->sequences[sequence]->nrofsteps==steps);
            for (int index=0;index<steps;++index) {
                frame=anim_forceframe(animation,index);assert(frame);
                assert(frame->get_width()>0 && frame->get_height()>0);
            }
            for (int tick=0;tick<steps*6;++tick) assert(anim_nextframe(animation));
            ++animationSlots;
        }
    }
    expected=std::fopen("/expected-maps.txt","r");assert(expected);
    int maps=0;
    while(std::fscanf(expected,"%127s %u %u %u",name,&w,&h,&hash)==4) {
        const size_t size=w*h/512;
        std::vector<BYTE> map(size);
        assert(loadfile(name,reinterpret_cast<char*>(map.data()),static_cast<UINT32>(size))==VG_TRUE);
        assert(fnv(map.data(),map.size())==hash);
        for(size_t i=0;i<map.size();i+=2)assert(map[i]<=21 && map[i+1]==0);
        ++maps;
    }
    assert(maps==3 && std::feof(expected));std::fclose(expected);
    // The collision sampler uses the same 16-pixel grid convention as the game.
    expected=std::fopen("/expected-collisions.txt","r");assert(expected);
    int grids=0;MAP_DESCR mapDescriptor={};
    while(std::fscanf(expected,"%127s %u %u %u",name,&w,&h,&hash)==4) {
        const size_t size=w*(h+32)/256;
        std::vector<BYTE> grid(size);
        assert(loadfile(name,reinterpret_cast<char*>(grid.data()),static_cast<UINT32>(size))==VG_TRUE);
        assert(fnv(grid.data(),grid.size())==hash);
        levelmap=&mapDescriptor;levelmap->mapsizex=w;levelmap->mapsizey=h;colmap=grid.data();
        for(unsigned y=0;y<h;y+=16)for(unsigned x=0;x<w;x+=16) {
            const int expectedValue=grid[(y/16)*(w/16)+x/16];
            assert(collision(x+8,y+8)==expectedValue);
        }
        assert(collision(w,0)==0 && collision(0,h)==0);
        colmap=nullptr;levelmap=nullptr;++grids;
    }
    assert(grids==3 && std::feof(expected));std::fclose(expected);
    asset_removeall();allframes=nullptr;allsequences=nullptr;allanims=nullptr;
    FastFileFini();
    std::printf("PASS: %d native PCX images, 258 frames, 32 sequences, 12 animations/%d slots, %d maps, %d native collision grids; no game loop, video or audio initialized\n",images,animationSlots,maps,grids);
}
