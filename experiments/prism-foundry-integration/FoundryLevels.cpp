// SPDX-License-Identifier: MIT
// Authored campaign selection and placements; uses the retained native actors.
#include "FoundryLevels.h"
#include "FoundryCourseData.h"
#include "globals.hpp"
#include "hoi.hpp"
#include "diamond.hpp"
#include "objects.hpp"
#include "trigger.hpp"
#include "anim.hpp"
#include "scroll.hpp"
#include <cstdlib>

namespace {
TRIGGER_ITEM NoTriggers[]={{0,0,0,0,nullptr}};
HOI_CAPS Movement={ID_HOI,1,1,1,140,4,54,54}; // Retained native movement configuration.
char Description[]="foundry.des";
char Background[]="foundry-back.pcx";
char Tiles[]="foundry-tiles.pcx";

int gateTick(OBJECT* gate,UINT32)
{
    gate->frame=anim_nextframe(gate->animate);
    const FoundryCourse* course=FoundryGetCourse(level);
    if (!course || !hoi || hoi->live!=hoi_live) return 0;
    if (hoi->x>=course->checkpointX && hoi->y<course->height-64) {
        restartx=course->checkpointX;restarty=course->checkpointY;
    }
    const bool overlaps=int(hoi->x)+hoi->sizex>gate->x && hoi->x<int(gate->x)+gate->sizex
        && int(hoi->y)+hoi->sizey>gate->y && hoi->y<int(gate->y)+gate->sizey;
    if (overlaps && player1.nrofblack<=4) nextlvlflg=1;
    return 0;
}
}

const FoundryCourse* FoundryGetCourse(int index)
{
    return index>=0 && index<3 ? &FoundryCourses[index]:nullptr;
}

void FoundryConfigureLevels()
{
    for (auto& worldLevels:levels) for (auto& entry:worldLevels) entry=LEVEL_DESCR{};
    for (int i=0;i<3;++i) {
        const auto& course=FoundryCourses[i];
        levels[0][i]=LEVEL_DESCR{Description,Background,Tiles,const_cast<char*>(course.map),
            const_cast<char*>(course.collision),static_cast<UINT16>(course.width),static_cast<UINT16>(course.height),
            FoundryInitCourse,NoTriggers};
    }
}

void FoundryInitCourse()
{
    const FoundryCourse* course=FoundryGetCourse(level);
    if (world!=0 || !course || !orghoi || !orgdiamond || !orgendoflevel) std::abort();
    hoi=hoi_globinit(orghoi,&Movement,hoi_ai,0,nullptr);
    hoi_init(hoi,course->spawnX,course->spawnY);
    restartx=course->spawnX;restarty=course->spawnY;
    player1.worldx=0;player1.worldy=course->spawnY>320 ? course->spawnY-320:0;
    player1.focusx=player1.worldx;player1.focusy=player1.worldy;
    for (int i=0;i<3;++i) diamond_init(course->prismX[i],course->prismY[i]);
    OBJECT* gate=static_cast<OBJECT*>(std::calloc(1,sizeof(OBJECT)));
    if (!gate) std::abort();
    gate->x=course->gateX;gate->y=course->gateY;gate->live=gateTick;
    gate->animate=copy_anim(orgendoflevel);gate->frame=anim_setsequence(gate->animate,0,SEQ_FORCE);
    if (!gate->frame) std::abort();
    gate->sizex=gate->frame->get_width();gate->sizey=gate->frame->get_height();
    object_add(gate);
    hoi_cam(&player1);scrolling(&player1);
}
