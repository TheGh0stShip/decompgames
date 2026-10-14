// Independently authored compatibility host. MIT; original commercial Emulator.cs is excluded.
namespace Celeste {
 public enum Stat {PICO_BERRIES,PICO_COMPLETES,PICO_DEATHS} public enum Achievement {PICO8}
 public static class Stats {public static readonly Dictionary<Stat,int> Values=new();public static void Increment(Stat s){Values[s]=Values.GetValueOrDefault(s)+1;}}
 public static class Achievements {public static readonly HashSet<Achievement> Values=new();public static void Register(Achievement a)=>Values.Add(a);}
 public class Settings {public static readonly Settings Instance=new();public bool DisableScreenShake=true;}
}
namespace Celeste.Pico8 {
 public class Emulator {
  public readonly bool[] Input=new bool[6];public readonly int[] MapData=new int[128*64];private readonly Random Random=new(20261014);
  public readonly List<object[]> Commands=new();public int MutedAudioCalls;private float CameraX,CameraY;
  public void BeginFrame()=>Commands.Clear();
  public bool btn(int k)=>Input[k];public float rnd(float v)=>(float)Random.NextDouble()*v;public float abs(float v)=>MathF.Abs(v);public float min(float a,float b)=>MathF.Min(a,b);public float max(float a,float b)=>MathF.Max(a,b);public int flr(float v)=>(int)MathF.Floor(v);public int sign(float v)=>Math.Sign(v);
  public float cos(float v)=>MathF.Cos(v*2*MathF.PI);public float sin(float v)=>-MathF.Sin(v*2*MathF.PI);
  public int dashDirectionX(int face){if(Input[0])return -1;if(Input[1])return 1;if(!Input[2]&&!Input[3])return face;return 0;}public int dashDirectionY(int face)=>Input[2]?-1:Input[3]?1:0;
  public int mget(int x,int y)=>x>=0&&x<128&&y>=0&&y<64?MapData[x+y*128]:0;public bool fget(int t,int f)=>t==2&&(f==0||f==2);
  public void spr(float id,float x,float y,int w=1,int h=1,bool flipX=false,bool flipY=false)=>Commands.Add(new object[]{"sprite",(int)id,x-CameraX,y-CameraY,w,h,flipX,flipY});
  public void rectfill(float x,float y,float x1,float y1,float color)=>Commands.Add(new object[]{"rect",x-CameraX,y-CameraY,x1-CameraX,y1-CameraY,(int)color});
  public void circfill(float x,float y,float radius,float color)=>Commands.Add(new object[]{"circle",x-CameraX,y-CameraY,radius,(int)color});
  public void print(string t,float x,float y,float c){
   // Authored presentation text substitutes for the original game's expressive labels.
   if(t=="press button")t="START";else if(t=="old site"||t=="summit"||t.EndsWith("m"))t="BEACON";else if(t.StartsWith("deaths:"))t="RETRY:"+t[7..];else if(t=="1000")t="LIGHT";
   Commands.Add(new object[]{"text",t.ToUpperInvariant(),x-CameraX,y-CameraY,(int)c});
  }
  public void camera(float x=0,float y=0){CameraX=x;CameraY=y;}
  public void pal(int a=-1,int b=-1)=>Commands.Add(new object[]{"palette",a,b});
  public void map(int sx,int sy,float dx,float dy,int w,int h,int layer){if(layer!=1)return;for(int y=0;y<h;y++)for(int x=0;x<w;x++)if(mget(sx+x,sy+y)==2)Commands.Add(new object[]{"tile",dx+x*8-CameraX,dy+y*8-CameraY});}
  // This prototype is intentionally silent. No audio API, original sound or music is included.
  public void sfx(int n){MutedAudioCalls++;}public void music(int n,int a,int b){MutedAudioCalls++;}
 }
}
