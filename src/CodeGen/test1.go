package main;
import "df";
import (
    "fmt";
    "strings";
    "adfdf";
);
type vertex struct{
  x int;
  y *vertex;
};


func main() int{
  var aa[10][10]int;

  var head vertex;
  var node1 vertex;
  var node2 vertex;
  head.x = 10;
  head.y = &node1;
  node1.x = 12;
  node1.y = &node2;
  node2.x = 11;
  
  var u int;
  u = 0;
  node2.y = &u;
  var r int;
  r = head.x ;
  printf("%d",r);
  return 0;
};