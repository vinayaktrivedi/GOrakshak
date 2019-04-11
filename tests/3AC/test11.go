package main;
import "fmt";

func main(){
	var sum int = 0;
	var i int;
	for i = 0; i < 10; i++ {
		sum += i;
		var num int = 0;
		if sum*i > 89 {
			sum = num - sum;
		}
		else {
			sum = -25;
		};
		if num < 0 {
        	num = -num;
    	} else if num < 10 {
        	num += 85;
        	num++;
    	} else {
        	num = 90-56;
        	num = 2*num - 67;
    	};
	};
};