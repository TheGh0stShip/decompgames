// Independently authored MIT host value types; no XNA/FNA/Monocle files.
namespace Microsoft.Xna.Framework {
 public struct Point { public int X,Y; public Point(int x,int y){X=x;Y=y;} }
 public struct Rectangle {public int X,Y,Width,Height;public Rectangle(int x,int y,int w,int h){X=x;Y=y;Width=w;Height=h;}}
 public struct Vector2 {public float X,Y;public Vector2(float x,float y){X=x;Y=y;} public static Vector2 operator +(Vector2 a,Vector2 b)=>new(a.X+b.X,a.Y+b.Y);public static Vector2 operator -(Vector2 a,Vector2 b)=>new(a.X-b.X,a.Y-b.Y);public static Vector2 operator *(Vector2 a,float b)=>new(a.X*b,a.Y*b);}
}
