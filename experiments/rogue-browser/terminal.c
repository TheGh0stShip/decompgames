/* Independently authored terminal platform adapter. MIT, 2026 DecompGames contributors. */
#include "curses.h"
#include <stdlib.h>
#include <string.h>
#include <emscripten.h>
int LINES=24,COLS=80;
static WINDOW screen;
static unsigned int physical[24*80];
static int ended=0;
WINDOW *stdscr=&screen,*curscr=&screen;
static unsigned int*cell(WINDOW*w,int y,int x){if(w->parent)return cell(w->parent,y+w->y-w->parent->y,x+w->x-w->parent->x);return &w->cells[y*80+x];}
static void dirty(WINDOW*w){w->dirty=1;if(w->parent)dirty(w->parent);}
static void init_window(WINDOW *w,int h,int c) { memset(w,0,sizeof(*w)); w->height=h;w->width=c;werase(w); }
WINDOW *initscr(void) {ended=0;init_window(stdscr,LINES,COLS);return stdscr;}
WINDOW *newwin(int h,int c,int y,int x) {if(h<1||c<1||y<0||x<0||y+h>24||x+c>80)return NULL;WINDOW*w=malloc(sizeof(*w));if(w){init_window(w,h,c);w->y=y;w->x=x;}return w;}
WINDOW *subwin(WINDOW*p,int h,int c,int y,int x){if(!p||y<p->y||x<p->x||y+h>p->y+p->height||x+c>p->x+p->width)return NULL;WINDOW*w=newwin(h,c,y,x);if(w)w->parent=p;return w;}
int mvwin(WINDOW*w,int y,int x){if(y<0||x<0||y+w->height>24||x+w->width>80)return ERR;w->y=y;w->x=x;dirty(w);return OK;}
int delwin(WINDOW*w){if(w!=stdscr)free(w);return OK;}
int endwin(void){wrefresh(stdscr);ended=1;return OK;}
int isendwin(void){return ended;}
int wmove(WINDOW*w,int y,int x){if(!w||y<0||x<0||y>=w->height||x>=w->width)return ERR;w->_cury=y;w->_curx=x;return OK;}
int waddch(WINDOW*w,chtype c){if(!w)return ERR;if(c=='\n'){wclrtoeol(w);w->_curx=0;if(w->_cury+1<w->height)w->_cury++;return OK;}if(c=='\r'){w->_curx=0;return OK;}if(c=='\b'){if(w->_curx)w->_curx--;return OK;}if(c=='\t'){do{waddch(w,' ');}while(w->_curx%8);return OK;}*cell(w,w->_cury,w->_curx)=(c&255)|w->attr;dirty(w);if(w->_curx+1<w->width)w->_curx++;else{w->_curx=0;if(w->_cury+1<w->height)w->_cury++;}return OK;}
int waddstr(WINDOW*w,const char*s){while(*s)waddch(w,(unsigned char)*s++);return OK;}
static int wp(WINDOW*w,const char*f,va_list a){char b[8192];vsnprintf(b,sizeof(b),f,a);return waddstr(w,b);}
int wprintw(WINDOW*w,const char*f,...){va_list a;va_start(a,f);int r=wp(w,f,a);va_end(a);return r;}
int mvwprintw(WINDOW*w,int y,int x,const char*f,...){wmove(w,y,x);va_list a;va_start(a,f);int r=wp(w,f,a);va_end(a);return r;}
int printw(const char*f,...){va_list a;va_start(a,f);int r=wp(stdscr,f,a);va_end(a);return r;}
int mvprintw(int y,int x,const char*f,...){wmove(stdscr,y,x);va_list a;va_start(a,f);int r=wp(stdscr,f,a);va_end(a);return r;}
int wrefresh(WINDOW*w){for(int y=0;y<w->height;y++)for(int x=0;x<w->width;x++)physical[(y+w->y)*80+x+w->x]=*cell(w,y,x);w->dirty=0;EM_ASM({if(Module.onTerminal)Module.onTerminal(HEAPU32.slice($0/4,$0/4+$1*80),$1,$2,$3,$4);},physical,24,80,w->_cury+w->y,w->_curx+w->x);return OK;}
int werase(WINDOW*w){for(int y=0;y<w->height;y++)for(int x=0;x<w->width;x++)*cell(w,y,x)=' ';dirty(w);w->_cury=w->_curx=0;return OK;}
int wclrtoeol(WINDOW*w){for(int x=w->_curx;x<w->width;x++)*cell(w,w->_cury,x)=' ';dirty(w);return OK;}
chtype winch(WINDOW*w){return *cell(w,w->_cury,w->_curx);}
int wstandout(WINDOW*w){w->attr=A_STANDOUT;return OK;}
int wstandend(WINDOW*w){w->attr=0;return OK;}
int getch(void){if(stdscr->dirty)wrefresh(stdscr);EM_ASM({Module.waiting=true;});for(;;){int c=EM_ASM_INT({return Module.keys&&Module.keys.length?Module.keys.shift():-1;});if(c>=0){EM_ASM({Module.waiting=false;});return c;}emscripten_sleep(16);}}
int wgetnstr(WINDOW*w,char*s,int n){int len=0,c;while((c=getch())!='\n'&&c!='\r'){if(c==8||c==127){if(len)len--;}else if(c>=32&&c<127&&len<n)s[len++]=c;}s[len]=0;return OK;}
int raw(void){return OK;}int noecho(void){return OK;}int nocbreak(void){return OK;}
int keypad(WINDOW*w,int b){return OK;}int idlok(WINDOW*w,int b){return OK;}
int leaveok(WINDOW*w,int b){return OK;}
int clearok(WINDOW*w,int b){if(b)dirty(w);return OK;}int touchwin(WINDOW*w){dirty(w);return OK;}
int mvcur(int a,int b,int c,int d){return wmove(stdscr,c,d);}
int baudrate(void){return 9600;}
int flushinp(void){EM_ASM({Module.keys=[];});return OK;}
int erasechar(void){return 8;}int killchar(void){return 21;}
char*unctrl(chtype c){static char b[3];c&=255;if(c<32){b[0]='^';b[1]=c+64;b[2]=0;}else{b[0]=c;b[1]=0;}return b;}
