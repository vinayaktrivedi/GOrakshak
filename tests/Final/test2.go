package main;

import "fmt";

func A(m int, n int) int {
    if m == 0 {
        var v int;
        v = n + 1;
        return v;
    };

    if m > 0{
      if n == 0{
        var b int;
        b = A(m-1, 1);
        return b;
      };
    };
    var u int;
    u =  A(m, n-1);
    var y int;
    y = A(m-1,u);
    return y;
};

func main() int {
    // for i:=0; i<4; i++ {
    //     for j:=0; j<5; j++ {
    //         print %d A(i, j);
    //     };
    // };

    var m int;
    var n int;
    // scan %d m;
    // scan %d n;
    m = 3;
    n = 4;
    var c int;
    c = A(m,n);
    printf("%d",c);
    return 0;
};
