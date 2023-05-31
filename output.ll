; ModuleID = "C:\Users\1\OneDrive\Desktop\formless\compik2.2.2a\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  %"a" = alloca i32
  store i32 7, i32* %"a"
  %"b" = alloca i32
  store i32 8, i32* %"b"
  %".4" = load i32, i32* %"a"
  %".5" = load i32, i32* %"b"
  %".6" = icmp slt i32 %".4", %".5"
  br i1 %".6", label %"if", label %"else"
if:
  %".8" = load i32, i32* %"a"
  %".9" = load i32, i32* %"b"
  %".10" = add i32 %".8", %".9"
  %".11" = bitcast [5 x i8]* @"fstr1" to i8*
  %".12" = call i32 (i8*, ...) @"printf"(i8* %".11", i32 %".10")
  br label %"merge"
else:
  br label %"merge"
merge:
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@"fstr1" = internal constant [5 x i8] c"%i \0a\00"