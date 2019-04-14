package main;

import (
	"fmt";
	"time";
);


func FibonacciRecursion(n int) int{
    if n <= 1 {
        return n;
    };
    return FibonacciRecursion(FibonacciRecursion(10)) + FibonacciRecursion(n-2);
};

func main() {
	var c int;
	c = FibonacciRecursion(19);
};
