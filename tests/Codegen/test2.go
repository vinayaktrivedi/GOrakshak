package main;
import "fmt";
func ss(a int,b int) int {
	return a+b;
};
func f(a int,b int) int {
	var u int;
	u = ss(6,7);
	return a+b + u;
};
func main() int{
	var a int;
	var b int;
	a = 10;
	b = 90;
	var c int;
	// var d int;
	c = f(a,b-9);
	printf("%d",c);

	var v int;
	v = f(a,b) + 10;
	printf("%d",v);
	// printf("%d",b);
	// printf("%d",c);


	return 0;
};
