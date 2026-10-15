// SPDX-License-Identifier: MIT
#pragma once
int FoundryReadResume();
void FoundryBeginCourse(int course);
void FoundryRestoreCourse();
void FoundryResetCourse();
bool FoundryPrismAvailable(int slot);
void FoundryPrismCollected(int x,int y);
int FoundryPrismMask();
int FoundryCheckpointActive();
int FoundryResumeUsed();
