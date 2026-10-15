// SPDX-License-Identifier: MIT
// Authored bounded implementation of the retained native animation interface.
// Interface/callers were inspected; no clean-room isolation claim.
#include "anim.hpp"
#include "globals.hpp"
#include <cstdlib>
#include <cstring>

namespace {
SEQUENCE* sequenceAt(ANIM* animation,int index)
{
    if (!animation || index<0 || index>=MAXSEQUENCES) return nullptr;
    SEQUENCE* sequence=animation->sequences[index];
    return sequence && sequence->nrofsteps>0 ? sequence:nullptr;
}
SEQUENCE* current(ANIM* animation)
{
    if (!animation) return nullptr;
    SEQUENCE* sequence=sequenceAt(animation,animation->cursequence);
    if (!sequence) return nullptr;
    animation->maxstep=sequence->nrofsteps;
    if (animation->stepnr>=sequence->nrofsteps) animation->stepnr=0;
    return sequence;
}
}

ANIM* copy_anim(ANIM* source)
{
    if (!source) return nullptr;
    ANIM* result=static_cast<ANIM*>(std::malloc(sizeof(ANIM)));
    if (result) std::memcpy(result,source,sizeof(ANIM));
    return result;
}

Cspr_frame* anim_forceframe(ANIM* animation,INT16 frame)
{
    SEQUENCE* sequence=current(animation);
    if (!sequence) return nullptr;
    int index=frame;
    if (index<0) index=0;
    if (index>=sequence->nrofsteps) index=sequence->nrofsteps-1;
    animation->stepnr=static_cast<UINT16>(index);
    animation->delay=animation->delaycnt;
    return sequence->frame[index];
}

Cspr_frame* anim_nextframe(ANIM* animation)
{
    SEQUENCE* sequence=current(animation);
    if (!sequence) return nullptr;
    if (animation->delay>0) --animation->delay;
    else {
        animation->delay=animation->delaycnt;
        animation->stepnr=static_cast<UINT16>((animation->stepnr+1)%sequence->nrofsteps);
    }
    return sequence->frame[animation->stepnr];
}

Cspr_frame* anim_prevframe(ANIM* animation)
{
    SEQUENCE* sequence=current(animation);
    if (!sequence) return nullptr;
    if (animation->delay>0) --animation->delay;
    else {
        animation->delay=animation->delaycnt;
        animation->stepnr=static_cast<UINT16>((animation->stepnr+sequence->nrofsteps-1)%sequence->nrofsteps);
    }
    return sequence->frame[animation->stepnr];
}

Cspr_frame* anim_setsequence(ANIM* animation,int index,int force)
{
    SEQUENCE* sequence=sequenceAt(animation,index);
    if (!sequence) return nullptr;
    if (!force && animation->cursequence==index) {
        current(animation);
        return sequence->frame[animation->stepnr];
    }
    animation->cursequence=static_cast<UINT16>(index);
    animation->maxstep=sequence->nrofsteps;
    animation->stepnr=0;
    animation->delay=3;
    animation->delaycnt=3;
    return sequence->frame[0];
}

ANIM* anim_retrieveanim(const char* name)
{
    if (!name || !allanims || !vg_dll_first(allanims)) return nullptr;
    do {
        ANIM* animation=static_cast<ANIM*>(vg_dll_collect(allanims));
        if (animation && animation->name && std::strcmp(animation->name,name)==0) return animation;
    } while (vg_dll_next(allanims));
    return nullptr;
}
