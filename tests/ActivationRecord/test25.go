package main;

import (
	"fmt";
	"time";
);


func FibonacciRecursion(n int) int {
    if n <= 1 {
        return n;
    };
    return FibonacciRecursion(n-1) + FibonacciRecursion(n-2);
};

func main() {
	FibonacciRecursion(19);
};