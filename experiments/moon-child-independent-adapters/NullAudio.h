// SPDX-License-Identifier: MIT
// Independently authored silent implementation of FE's IAudio interface.
#pragma once
#include "IAudio.h"

class NullAudio final : public IAudio
{
public:
    bool Init() override { return true; }
    void Destroy() override {}
    SoundHandle CreateSound(int, int) override { return 1; }
    void DestroySound(SoundHandle) override {}
    void PlayOneShot(SoundHandle, int32_t, int32_t) override {}
    void PlayLoop(SoundHandle, int32_t, int32_t) override {}
    void StopSound(SoundHandle) override {}
    void StopCurrent(SoundHandle) override {}
    void SetVolume(SoundHandle, int32_t) override {}
    void SetPan(SoundHandle, int32_t) override {}
    void Reset() override {}
    bool PlayMusic(int) override { return false; }
    void StopMusic() override {}
    bool OpenMovieStream(int, int) override { return false; }
    void SubmitMovieAudio(const float*, int) override {}
    void CloseMovieStream() override {}
};
