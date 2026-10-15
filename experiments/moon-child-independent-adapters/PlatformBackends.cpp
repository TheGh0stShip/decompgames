// SPDX-License-Identifier: MIT
// Concrete selection for this experimental SDL2/GLES2, silent build only.
#include "PlatformBackends.h"
#include "SDL2Window.h"
#include "GLESRenderer.h"
#include "SDL2Input.h"
#include "NullAudio.h"

PlatformBackends MakeDefaultBackends()
{
    PlatformBackends result;
    result.Window.reset(new SDL2Window());
    result.Renderer.reset(new GLESRenderer());
    result.Input.reset(new SDL2Input());
    result.Audio.reset(new NullAudio());
    return result;
}
