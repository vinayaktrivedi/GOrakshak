package main;
import "fmt";

func f(a int,b int, c int, d int, e int, f int, g int, h int) int {
	return a+b;
};
func main() int{
	var a int;
	var b int;
	a = 8;
	b = 8;
	var c int;
	// var d int;
	c = f(a,b,12,2,3,4,13,2);
	printf("%d",c);



	return 0;
};
