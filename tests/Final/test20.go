package main;
import "fmt";

//type ttype new_type struct{a, c int; b pointer ttype new_type;};
type ttype struct{c int; b int;};


func main() int{
    var a ttype;
    // var b ttype;
    var c int;
     // = 2;
    a.b = 4;
    a.c = 33;
    // d = a.b;
    c = a.b + a.c;
    printf("%d",c);
    return 0;
    // fun(a);
    //c = a.a + a.b;
    //print %d c;
};
