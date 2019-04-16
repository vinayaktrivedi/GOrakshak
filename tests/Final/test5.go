package main;

import (
	"fmt";
	"time";
);


func FibonacciRecursion(n int) int{
    if n <= 1 {
        return n;
    };
		var a int;
		a = FibonacciRecursion(n-1);
		var b int;
		b = FibonacciRecursion(n-2);
		printf("%d",a);
		var c int;
		// printf("%d",b);
		c = a + b;
    return c;
};
// func foo(n int) int, int {
//   c := n - 1;
//   return n,c;
// };
func main() int{
	var c int;
	c = FibonacciRecursion(9);
  // v,m := foo(10);
	printf("%d",c);
	return 0;
};
