// SPDX-License-Identifier: MIT
#include "frm_wrk.hpp"
#include "anim.hpp"
#include "asset.hpp"
#include "globals.hpp"
#include "FoundryLevels.h"
#include <cassert>
#include <climits>
#include <cstdio>
#include <string>
#include <vector>

static int rejected=0;
static void writeFile(const char* path,const std::string& value)
{
    FILE* file=std::fopen(path,"wb");assert(file);
    assert(std::fwrite(value.data(),1,value.size(),file)==value.size());assert(std::fclose(file)==0);
}
static void lists()
{
    allframes=vg_dll_create(1);allsequences=vg_dll_create(1);allanims=vg_dll_create(1);
    assert(allframes && allsequences && allanims);
}
static std::string descriptor(int frames,int slots,const char* image="c00-0.pcx")
{
    std::string result="S \"frames\"\n";
    for(int i=0;i<frames;++i)result+=" \""+std::string(image)+"\"\n";
    result+="A \"actor\"\n";
    for(int i=0;i<slots;++i)result+=" \"frames\"\n";
    return result+"E\n";
}
static void rejects(const std::string& value)
{
    lists();writeFile("/probe.des",value);assert(asset_parse("/probe.des")==0);
    assert(vg_dll_count(allframes)==0 && vg_dll_count(allsequences)==0 && vg_dll_count(allanims)==0);
    assert(!anim_retrieveanim("actor"));asset_removeall();++rejected;
}

int main()
{
    FoundryConfigureLevels();
    assert(!FoundryGetCourse(-1) && !FoundryGetCourse(3));
    const int widths[]={2048,2304,2560},heights[]={768,768,896};
    const char* maps[]={"assembly.map","cooling.map","night.map"};
    for(int w=0;w<5;++w)for(int l=0;l<4;++l) {
        const auto& entry=levels[w][l];
        if(w==0 && l<3) {
            assert(entry.mapsizex==widths[l] && entry.mapsizey==heights[l]);
            assert(std::string(entry.map)==maps[l] && std::string(entry.descr)=="foundry.des");
            assert(std::string(entry.parallax)=="foundry-back.pcx" && std::string(entry.patspic)=="foundry-tiles.pcx");
            assert(entry.level_init_fn==FoundryInitCourse && entry.triglist);
        } else assert(!entry.descr && !entry.level_init_fn && !entry.map && entry.mapsizex==0);
    }
    assert(FastFileInit("/data/mc.art",16));
    assert(!anim_retrieveanim(nullptr) && !anim_retrieveanim("missing"));
    assert(!copy_anim(nullptr));
    assert(!anim_forceframe(nullptr,0) && !anim_nextframe(nullptr) && !anim_prevframe(nullptr));
    assert(!anim_setsequence(nullptr,0,1));
    lists();writeFile("/probe.des",descriptor(2,21));assert(asset_parse("/probe.des"));
    auto* animation=anim_retrieveanim("actor");assert(animation);
    auto* first=anim_setsequence(animation,0,1);
    auto* last=animation->sequences[0]->frame[1];assert(first && last && first!=last);
    assert(anim_forceframe(animation,SHRT_MIN)==first);
    assert(anim_forceframe(animation,SHRT_MAX)==last);
    assert(anim_forceframe(animation,2)==last && animation->stepnr==1);
    assert(anim_forceframe(animation,0)==first);
    animation->delay=0;assert(anim_prevframe(animation)==last);
    animation->delay=0;assert(anim_nextframe(animation)==first);
    assert(!anim_setsequence(animation,-1,1) && !anim_setsequence(animation,21,1));
    assert(animation->cursequence==0 && animation->stepnr==0);
    assert(anim_setsequence(animation,20,1)==first);
    animation->cursequence=65535;assert(!anim_nextframe(animation));
    animation->cursequence=0;animation->stepnr=65535;
    assert(anim_forceframe(animation,0)==first);
    animation->sequences[0]->nrofsteps=0;
    assert(!anim_nextframe(animation) && !anim_prevframe(animation) && !anim_forceframe(animation,0));
    animation->sequences[0]->nrofsteps=2;
    assert(!asset_parse("/probe.des")); // Never replace existing live lists.
    asset_removeall();asset_removeall();
    lists();writeFile("/probe.des",descriptor(100,1));assert(asset_parse("/probe.des"));
    assert(vg_dll_count(allframes)==100);asset_removeall();
    rejects(descriptor(101,1));rejects(descriptor(1,22));
    rejects(descriptor(0,1));rejects(descriptor(1,0));
    rejects("S \"frames\"\n \"c00-0.pcx\"\nA \"actor\"\n \"missing\"\nE\n");
    rejects("S \"frames\n \"c00-0.pcx\"\nE\n");
    rejects(descriptor(1,1)+"A \"extra\"\n");
    rejects("S \"frames\"\n \"c00-0.pcx\"\nA \"actor\"\n \"frames\"\n");
    rejects(descriptor(1,1,"missing.pcx"));
    rejects("S \"frames\"\n \"c00-0.pcx\"\nS \"frames\"\n \"c00-0.pcx\"\nE\n");
    rejects("S \""+std::string(251,'x')+"\"\nE\n");
    rejects(std::string(256*1024+1,' '));
    FILE* file=std::fopen("/data/c00-0.pcx","rb");assert(file);
    std::vector<char> image;char buffer[1024];size_t count;
    while((count=std::fread(buffer,1,sizeof(buffer),file))>0)image.insert(image.end(),buffer,buffer+count);
    assert(std::fclose(file)==0 && image.size()>900);
    const std::string original(image.begin(),image.end());
    auto badImage=[&](const std::string& data) {
        writeFile("/data/bad.pcx",data);rejects(descriptor(1,1,"bad.pcx"));
    };
    badImage(original.substr(0,100));
    auto bad=original;bad[65]=2;badImage(bad);
    bad=original;bad[4]=1;badImage(bad);
    bad=original;bad[66]=0;bad[67]=0;badImage(bad);
    bad=original;bad[128]=char(192);badImage(bad); // Zero-length RLE packet.
    badImage(original.substr(0,original.size()-1));
    badImage(original+"extra");
    const std::string longName=std::string(90,'x')+".pcx";
    writeFile(("/data/"+longName).c_str(),original);
    rejects(descriptor(1,1,longName.c_str()));
    // Four 4-MiB sprites fit the decoded-pixel budget; a fifth must roll back.
    std::string large=original.substr(0,128);
    large[8]=char(255);large[9]=7;large[10]=char(255);large[11]=7;
    large[66]=0;large[67]=8;
    for(int y=0;y<2048;++y) {
        for(int run=0;run<32;++run) { large+=char(255);large+=char(1); }
        large+=char(224);large+=char(1);
    }
    large+=char(12);large+=original.substr(original.size()-768);
    writeFile("/data/large.pcx",large);
    lists();writeFile("/probe.des",descriptor(4,1,"large.pcx"));assert(asset_parse("/probe.des"));
    assert(vg_dll_count(allframes)==4);asset_removeall();
    rejects(descriptor(5,1,"large.pcx"));
    // Actual authored content must still parse through native sprite/PCX code.
    lists();assert(asset_parse("/data/foundry.des"));
    assert(vg_dll_count(allframes)==258 && vg_dll_count(allsequences)==32 && vg_dll_count(allanims)==12);
    asset_removeall();FastFileFini();
    std::printf("PASS: three authored native level descriptors, other 17 absent; animation index/null/zero-count/wrap bounds; 21-slot and 100-frame limits; %d rejected descriptor/image cases leave empty lists; authored 258-frame pack accepted; course initialization not executed\n",rejected);
}
