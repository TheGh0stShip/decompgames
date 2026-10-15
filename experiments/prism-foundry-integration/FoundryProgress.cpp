// SPDX-License-Identifier: MIT
// Authored progression: fixed checkpoint resume, never an arbitrary-position save.
#include "FoundryProgress.h"
#include "FoundryLevels.h"
#include "FoundrySaveRevision.h"
#include "globals.hpp"
#include "hoi.hpp"
#include <cstdlib>
#include <emscripten.h>

extern int FoundryComplete;
namespace {
int courseIndex=0,mask=0,resumeCode=-1,resumeUsed=0;
EM_JS(int,readResume,(const char* revision),{
    const r=Module['foundryResume'];
    if(!r||r.v!==1||r.revision!==UTF8ToString(revision))return -1;
    if(!Number.isInteger(r.course)||r.course<0||r.course>2||!Number.isInteger(r.prisms)||r.prisms<0||r.prisms>7||typeof r.checkpoint!=='boolean'||typeof r.complete!=='boolean')return -1;
    return r.course|(r.prisms<<2)|(r.checkpoint?32:0)|(r.complete?64:0);
});
}
int FoundryReadResume()
{
    resumeCode=readResume(FoundrySaveRevision);
    if(resumeCode<0||resumeCode>127||(resumeCode&3)>2||((resumeCode&64)&&((resumeCode&63)!=62)))resumeCode=-1;
    resumeUsed=resumeCode>=0?1:0;
    return resumeUsed?(resumeCode&3):0;
}
void FoundryBeginCourse(int course)
{
    if(!FoundryGetCourse(course))std::abort();
    courseIndex=course;
    mask=resumeCode>=0&&(resumeCode&3)==course?((resumeCode>>2)&7):0;
}
bool FoundryPrismAvailable(int slot)
{
    return slot>=0&&slot<3&&(mask&(1<<slot))==0;
}
void FoundryPrismCollected(int x,int y)
{
    const auto* course=FoundryGetCourse(courseIndex);
    if(!course)std::abort();
    for(int slot=0;slot<3;++slot)if(course->prismX[slot]==x&&course->prismY[slot]==y){mask|=1<<slot;return;}
    std::abort();
}
void FoundryRestoreCourse()
{
    if(resumeCode<0)return;
    const auto* course=FoundryGetCourse(courseIndex);
    if(!course||(resumeCode&3)!=courseIndex)std::abort();
    if(resumeCode&32){restartx=course->checkpointX;restarty=course->checkpointY;hoi_init(hoi,restartx,restarty);}
    int count=0;for(int slot=0;slot<3;++slot)if(mask&(1<<slot))++count;
    player1.nrofblack=7-count;
    if(resumeCode&64)FoundryComplete=1;
    resumeCode=-1;
}
void FoundryResetCourse(){resumeCode=-1;mask=0;FoundryComplete=0;}
int FoundryPrismMask(){return mask;}
int FoundryCheckpointActive()
{
    const auto* course=FoundryGetCourse(courseIndex);
    return course&&restartx==course->checkpointX&&restarty==course->checkpointY?1:0;
}
int FoundryResumeUsed(){return resumeUsed;}
