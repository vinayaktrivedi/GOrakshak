package main;
import "fmt";
func hello() int {
	return 2;
};
func main(){
	var g [20]int;
	g[10] = 0;
	g[9],g[1] := 90,845;
	g[1] = hello();

	var sum int = 0;
	var i int;
	for i = 0; i < 10; i++ {
		var k int;
		k = 3*i;
		sum += k;
	};
	sum -= k;
	sum  := 10;
};