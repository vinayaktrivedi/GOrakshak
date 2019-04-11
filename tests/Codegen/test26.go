package main;

import (
	"fmt";
	"time";
);


func FibonacciRecursion(n int) int{
    if n <= 1 {
        return n;
    };
    return FibonacciRecursion(n-1) + FibonacciRecursion(n-2);
};
func foo(n int) int, int {
  c := n - 1;
  return n,c;
};
func main() {
	var c int;
	c := FibonacciRecursion(19);
  v,m := foo(10);
};
