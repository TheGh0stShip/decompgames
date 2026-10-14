/* Read-only native diagnostic observer. MIT, 2026 DecompGames contributors. */
#include "curses.h"
#include "rogue.h"
#include <emscripten.h>
#include <stdio.h>
EMSCRIPTEN_KEEPALIVE const char *dg_map(void){static char map[24*81+1];int n=0;for(int y=0;y<24;y++){for(int x=0;x<80;x++)map[n++]=chat(y,x);map[n++]='\n';}map[n]=0;return map;}
EMSCRIPTEN_KEEPALIVE const char *dg_state(void){
 static char b[14000];int n=snprintf(b,sizeof(b),"{\"x\":%d,\"y\":%d,\"hp\":%d,\"maxHp\":%d,\"depth\":%d,\"gold\":%d,\"experience\":%d,\"food\":%d,\"playing\":%d,\"pack\":[",hero.x,hero.y,pstats.s_hpt,max_hp,level,purse,pstats.s_exp,food_left,playing);
 THING*t;int first=1;for(t=pack;t&&n<10000;t=t->l_next){n+=snprintf(b+n,sizeof(b)-n,"%s[%d,%d,%d,%d]",first?"":",",t->o_type,t->o_which,t->o_count,t->o_packch);first=0;}
 n+=snprintf(b+n,sizeof(b)-n,"],\"monsters\":[");first=1;
 for(t=mlist;t&&n<12000;t=t->l_next){n+=snprintf(b+n,sizeof(b)-n,"%s[%d,%d,%d,%d]",first?"":",",t->t_type,t->t_pos.x,t->t_pos.y,t->t_stats.s_hpt);first=0;}
 snprintf(b+n,sizeof(b)-n,"]}");return b;
}
