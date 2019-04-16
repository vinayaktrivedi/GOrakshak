package main;
import "fmt";
func f(a int,b int) int {
	return a+b;
};
func main() int{
	var a int;
	var b int;
	a = 10;
	b = 90;
	var c int;
	// var d int;
	c = f(a,b);
	printf("%d",c);
	return 0;
};
