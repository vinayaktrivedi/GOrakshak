package main;
import "fmt";

LIM := 41;
var facts [LIM]int;


func Factorial(n int)int {

	result := 0;
	if n > 0 {
		result = n * Factorial(n-1);
		return result;
	};
	return 1;
};


// func main() {
// 	c := Factorial(12);
// }

