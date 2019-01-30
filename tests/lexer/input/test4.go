//this file consist of struct and its methods
package main

import "fmt"

type Rectangle struct {
    length, width int
}

func (r Rectangle) Area_by_value() int {
    return r.length * r.width
}

func (r *Rectangle) Area_by_reference() int {
    return r.length * r.width
}

func main() {
    r1 := Rectangle{4, 3}
    fmt.Println("Rectangle is: ", r1)
    fmt.Println("Rectangle area is: ", r1.Area_by_value())
    fmt.Println("Rectangle area is: ", r1.Area_by_reference())
    fmt.Println("Rectangle area is: ", (&r1).Area_by_value())
    fmt.Println("Rectangle area is: ", (&r1).Area_by_reference())
}