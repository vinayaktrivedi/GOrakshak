package main;
import "fmt";

func main(){
	var i int;
	i= 2;
    switch i==1 {
    case 1:
        i++;
    case 2:
        i--;
    case 3:
        i++;
    default:
    	i--;
    };
};