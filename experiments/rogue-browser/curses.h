/* Independently authored terminal platform adapter. MIT, 2026 DecompGames contributors. */
#ifndef DG_CURSES_H
#define DG_CURSES_H
#include <stdio.h>
#include <stdarg.h>
typedef unsigned char bool;
typedef unsigned int chtype;
#define TRUE 1
#define FALSE 0
#define ERR -1
#define OK 0
#define A_CHARTEXT 255
#define A_STANDOUT 256
typedef struct DGWindow { int _cury,_curx,height,width,attr,y,x,dirty; struct DGWindow *parent; unsigned int cells[24*80]; } WINDOW;
extern WINDOW *stdscr,*curscr;
extern int LINES,COLS;
WINDOW *initscr(void);
WINDOW *newwin(int,int,int,int);
WINDOW *subwin(WINDOW*,int,int,int,int);
int mvwin(WINDOW*,int,int);
int delwin(WINDOW*);
int endwin(void);
int isendwin(void);
int wmove(WINDOW*,int,int);
int waddch(WINDOW*,chtype);
int waddstr(WINDOW*,const char*);
int wprintw(WINDOW*,const char*,...);
int mvwprintw(WINDOW*,int,int,const char*,...);
int printw(const char*,...);
int mvprintw(int,int,const char*,...);
int wrefresh(WINDOW*);
int werase(WINDOW*);
int wclrtoeol(WINDOW*);
chtype winch(WINDOW*);
int wstandout(WINDOW*);
int wstandend(WINDOW*);
int getch(void);
int wgetnstr(WINDOW*,char*,int);
int raw(void);
int noecho(void);
int nocbreak(void);
int keypad(WINDOW*,int);
int idlok(WINDOW*,int);
int leaveok(WINDOW*,int);
int clearok(WINDOW*,int);
int touchwin(WINDOW*);
int mvcur(int,int,int,int);
int baudrate(void);
int flushinp(void);
int erasechar(void);
int killchar(void);
char *unctrl(chtype);
#define getmaxx(w) ((w)->width)
#define getmaxy(w) ((w)->height)
#define getyx(w,y,x) ((y)=(w)->_cury,(x)=(w)->_curx)
#define move(y,x) wmove(stdscr,y,x)
#define addch(c) waddch(stdscr,c)
#define addstr(s) waddstr(stdscr,s)
#define refresh() wrefresh(stdscr)
#define clear() werase(stdscr)
#define wclear(w) werase(w)
#define clrtoeol() wclrtoeol(stdscr)
#define inch() winch(stdscr)
#define mvinch(y,x) (move(y,x),inch())
#define mvwinch(w,y,x) (wmove(w,y,x),winch(w))
#define mvaddch(y,x,c) (move(y,x),addch(c))
#define mvaddstr(y,x,s) (move(y,x),addstr(s))
#define mvwaddch(w,y,x,c) (wmove(w,y,x),waddch(w,c))
#define standout() wstandout(stdscr)
#define standend() wstandend(stdscr)
#endif
