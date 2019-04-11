package main;
import "fmt";
func hello() int,int {
	return 2,3;
};
func main(){
	var g [20]int;
	g[10] = 0;
	g[9],g[1] := 90,845;
	g[1],g[4] = hello();

	var sum int = 0;
	var i int;
	for i = 0; i < 10; i++ {
		sum += i;
	};
};