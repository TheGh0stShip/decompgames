// SPDX-License-Identifier: MIT
#pragma once
struct FoundryCourse {
    const char* name;
    const char* map;
    const char* collision;
    int width,height;
    int spawnX,spawnY,checkpointX,checkpointY,gateX,gateY;
    int prismX[3],prismY[3];
};
const FoundryCourse* FoundryGetCourse(int index);
void FoundryConfigureLevels();
void FoundryInitCourse();
