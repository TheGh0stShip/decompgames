/* Independently authored single-user browser platform. MIT, 2026 DecompGames contributors. */
#include "curses.h"
#include <unistd.h>
#include <sys/stat.h>
#include <emscripten.h>
#include "extern.h"
void md_init(void){}
int md_chmod(char*f,int m){return chmod(f,m);}
int md_unlink(char*f){return unlink(f);}
int md_unlink_open_file(char*f,FILE*i){return unlink(f);}
char*md_gethomedir(void){return "/";}
char*md_getusername(void){return "Explorer";}
char*md_getrealname(int u){return "Explorer";}
int md_getuid(void){return 1;}
int md_getpid(void){return 1;}
void md_normaluser(void){}
int md_dsuspchar(void){return 26;}
int md_suspchar(void){return 26;}
int md_setdsuspchar(int c){return c;}
int md_erasechar(void){return 8;}
int md_killchar(void){return 21;}
int md_hasclreol(void){return 1;}
int md_readchar(void){return getch();}
int md_shellescape(void){return -1;}
void md_sleep(int s){emscripten_sleep(s*1000);}
void md_raw_standout(void){standout();}
void md_raw_standend(void){standend();}
void md_tstpsignal(void){}
void md_tstphold(void){}
void md_tstpresume(void){}
void md_ignoreallsignals(void){}
void md_onsignal_autosave(void){}
void md_onsignal_exit(void){}
void md_onsignal_default(void){}
int md_issymlink(char*s){struct stat b;return lstat(s,&b)==0&&S_ISLNK(b.st_mode);}
