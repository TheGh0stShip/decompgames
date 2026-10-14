/* Independently authored scenario adapter. MIT, DecompGames contributors, 2026.
 * survey-levels.h is generated exclusively from CC0 survey-content.json.
 * Reference gameplay APIs and structures remain governed by their BSD notices.
 */
#include <curses.h>
#include <string.h>
#include "rogue.h"
#include "survey-levels.h"

int rnd_room(void) { return 0; }

static void survey_item(int type, int which, int x, int y) {
    THING *obj = new_item();
    memset(obj, 0, sizeof(*obj));
    obj->o_type = type; obj->o_which = which; obj->o_count = 1;
    obj->o_pos.x = x; obj->o_pos.y = y;
    obj->o_launch = -1; obj->o_arm = 11;
    strcpy(obj->o_damage, "0x0"); strcpy(obj->o_hurldmg, "0x0");
    attach(lvl_obj, obj); chat(y, x) = type;
}

void new_level(void) {
    THING *tp;
    int i, x, y;
    /* A corrupted legacy state must never index outside the authored table. */
    if (level < 1 || level > 3) {
        clear(); msg("This checkpoint references an unknown station.");
        my_exit(1); return;
    }
    const struct survey_floor *floor = &survey_floors[level - 1];
    player.t_flags &= ~ISHELD;
    if (level > max_level) max_level = level;
    for (tp = mlist; tp != NULL; tp = next(tp)) free_list(tp->t_pack);
    free_list(mlist); free_list(lvl_obj);
    for (i = 0; i < MAXCOLS * MAXLINES; i++) {
        places[i].p_ch = ' '; places[i].p_flags = F_REAL; places[i].p_monst = NULL;
    }
    clear(); ntraps = 0;
    memset(rooms, 0, sizeof(struct room) * MAXROOMS);
    memset(passages, 0, sizeof(struct room) * MAXPASS);
    for (i = 1; i < MAXROOMS; i++) {
        rooms[i].r_flags = ISGONE; rooms[i].r_max.x = -80; rooms[i].r_max.y = -24;
    }
    rooms[0].r_pos.x = floor->x; rooms[0].r_pos.y = floor->y;
    rooms[0].r_max.x = 30; rooms[0].r_max.y = 12;
    for (y = 0; y < 12; y++) for (x = 0; x < 30; x++)
        chat(floor->y + y, floor->x + x) = floor->rows[y][x];
    stairs.x = floor->x + floor->lift_x; stairs.y = floor->y + floor->lift_y;
    chat(stairs.y, stairs.x) = STAIRS; seenstairs = FALSE;
    hero.x = floor->x + floor->entry_x; hero.y = floor->y + floor->entry_y;
    /* The return trip keeps the authored architecture but does not respawn loot. */
    if (!(amulet && level < max_level)) {
        for (i = 0; i < floor->item_count; i++) {
            const struct survey_object *o = &floor->items[i];
            survey_item(o->type, o->which, floor->x + o->x, floor->y + o->y);
        }
        for (i = 0; i < 2; i++) {
            coord at; at.x = floor->x + floor->actors[i][0]; at.y = floor->y + floor->actors[i][1];
            tp = new_item(); new_monster(tp, 'B', &at); tp->t_flags |= ISMEAN;
        }
    }
    enter_room(&hero); mvaddch(hero.y, hero.x, PLAYER);
    msg("%s: %s", floor->name, floor->briefing);
    if (on(player, SEEMONST)) turn_see(FALSE);
    if (on(player, ISHALU)) visuals();
}
