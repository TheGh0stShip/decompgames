// Independently authored course controller and browser bridge, MIT.
using System.Runtime.InteropServices.JavaScript;using System.Runtime.Versioning;using System.Reflection;using System.Text.Json;using Celeste;using Celeste.Pico8;
[SupportedOSPlatform("browser")] public static partial class GameBridge {
 static Emulator E;static Classic G;static int Frames,Course;static bool Cleared,Completed;
 static readonly BindingFlags Private=BindingFlags.Instance|BindingFlags.NonPublic;
 static List<Classic.ClassicObject> Objects()=>(List<Classic.ClassicObject>)typeof(Classic).GetField("objects",Private).GetValue(G);
 static string State(){var p=Objects().OfType<Classic.player>().FirstOrDefault();return JsonSerializer.Serialize(new {frames=Frames,course=Course,cleared=Cleared,completed=Completed,player=p!=null,x=p?.x??0,y=p?.y??0,dx=p?.spd.X??0,dy=p?.spd.Y??0,dashes=p?.djump??0,mutedAudioCalls=E.MutedAudioCalls,stats=Stats.Values.ToDictionary(x=>x.Key.ToString(),x=>x.Value),commands=E.Commands});}
 static void Tile(int room,int x,int y,int t)=>E.MapData[room*16+x+y*128]=t;
 static void OwnMaps(){
  // CC0: three courses authored here without reading or loading the original maps.
  for(int r=0;r<3;r++){
   for(int x=0;x<16;x++){Tile(r,x,0,2);Tile(r,x,15,2);}
   Tile(r,2,13,1);Tile(r,7,14,26);Tile(r,14,14,118);
  }
  // Course 2 has a short raised ledge; jumping is required to cross it.
  Tile(1,6,14,2);Tile(1,7,14,2);Tile(1,7,13,26);Tile(1,7,14,2);
  // Course 3 has an open three-tile trench. A dash can bridge it; falling respawns normally.
  for(int x=7;x<=9;x++)Tile(2,x,15,0);Tile(2,7,14,0);Tile(2,11,14,26);
 }
 static void Render(){E.BeginFrame();G.Draw();}
 [JSExport] public static string Init(int savedCourse){Stats.Values.Clear();Achievements.Values.Clear();E=new Emulator();OwnMaps();G=new Classic();G.Init(E);Frames=0;Course=Math.Clamp(savedCourse,0,3);Completed=Course==3;Cleared=false;if(Course>0)G.load_room(Math.Min(Course,2),0);Render();return State();}
 [JSExport] public static string Step(int mask){for(int i=0;i<6;i++)E.Input[i]=(mask&(1<<i))!=0;if(!Cleared&&!Completed){G.Update();Frames++;Render();var flag=Objects().OfType<Classic.flag>().FirstOrDefault();Cleared=flag!=null&&(bool)typeof(Classic.flag).GetField("show",Private).GetValue(flag);}return State();}
 [JSExport] public static string Next(){if(Cleared&&!Completed){Course++;Completed=Course==3;Cleared=false;if(!Completed){G.load_room(Course,0);Render();}}return State();}
}
class Program {static void Main(){}}
