package main;

import "fmt";


func main(){
	var a int =10;
	var i int=10;
	var b int =100;
	if i<10 {
		a++;
	}
	else if i<20{
		a--;
	}
	else{
		a+=2;
	};
	{
		var c int;
		b+=2;
	};
	{
		c--;
	};
};
