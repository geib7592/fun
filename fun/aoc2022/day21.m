(* ::Package:: *)

(* ::Input:: *)
(*s=Import[FileNameJoin[{NotebookDirectory[], "input_files","day21_gap.txt"}]];*)
(*s = StringReplace[s,":"->" ->"];*)
(*ssplit =StringSplit[s, "\n"];*)
(*rules=ToExpression/@ssplit;*)
(*Print["Part1: ", root//.rules]*)
(**)
(*names=StringTake[#,4]&/@ssplit;*)
(*rootPosition=Position[names,"root"]//First//First;*)
(*humnPosition=Position[names,"humn"]//First//First;*)
(*rules2 =ToExpression/@Join[*)
(*ssplit[[1;;Min[{rootPosition, humnPosition}]-1]],*)
(*ssplit[[*)
(*Min[{rootPosition, humnPosition}]+1;;Max[{rootPosition, humnPosition}]-1*)
(*]],*)
(*ssplit[[Max[{rootPosition, humnPosition}]+1;;]]*)
(*];*)
(*name1=StringSplit[ssplit[[rootPosition]]][[3]];*)
(*name2=StringSplit[ssplit[[rootPosition]]][[5]];*)
(*humnRule=Solve[(ToExpression[name1]==ToExpression[name2])//.rules2,humn]//First;*)
(*Print["Part 2: ", humn/.humnRule]*)



