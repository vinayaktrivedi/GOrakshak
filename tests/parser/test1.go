// // package main;

// // import (
// // 	"fmt";
// // 	"time";
// // );

// // // In order to sort by a custom function in Go, we need a
// // // corresponding type. Here we've created a `byLength`
// // // type that is just an alias for the builtin `[]string`
// // // type.

// // func main() {
// // 	fmt.Println("Welcome to the playground!");
// // 	var b string = "4";
// // 	var a = 5;
// // 	f(b, a);
// // };


// // package main;

// // import "sort";
// // import "fmt";

// // // In order to sort by a custom function in Go, we need a
// // // corresponding type. Here we've created a `byLength`
// // // type that is just an alias for the builtin `[]string`
// // // type.
// // type byLength []string;

// // // We implement `sort.Interface` - `Len`, `Less`, and
// // // `Swap` - on our type so we can use the `sort` package's
// // // generic `Sort` function. `Len` and `Swap`
// // // will usually be similar across types and `Less` will
// // // hold the actual custom sorting logic. In our case we
// // // want to sort in order of increasing string length, so
// // // we use `len(s[i])` and `len(s[j])` here.
// // // func Len(s byLength) int {
// // //     return len(s);
// // // };
// // func add(x int, y int) int {
// // 	return x + y;
// // };
// // // func (s byLength) Swap(i, j int) {
// // //     s[i], s[j] = s[j], s[i];
// // // };
// // // func (s byLength) Less(i, j int) bool {
// // //     return len(s[i]) < len(s[j]);
// // // };
// // /*
// //  With all of this in place, we can now implement our
// //  custom sort by casting the original `fruits` slice to
// //  `byLength`, and then use `sort.Sort` on that typed
// //  slice.
// // */
// // func main() {
// //     // fruits := []string{"peach", "banana", "kiwi"};
// // 	sort.Sort(byLength(fruits));
// // 	//d jasd
// // 	var x float = 9.89898989898989;
// // 	/*alsdj 
// // 	*askd*/
// //     fmt.Println(fruits);
// // };

// //this file consist of struct and its methods
// package main;

// import "fmt";

// type Rectangle struct {
//     length, width int;
// };

// func Area_by_value(r Rectangle) int {
//     return r.length * r.width;
// };

// // func (r *Rectangle) Area_by_reference() int {
// //     return r.length * r.width
// // }

// func main() int {
// 	var r1 Rectangle;
// 	r1.length=1;
// 	r1.width=2;

//     fmt.Println("Rectangle is: ", r1);
//     fmt.Println("Rectangle area is: ", r1.Area_by_value());
//     fmt.Println("Rectangle area is: ", r1.Area_by_reference());
//     fmt.Println("Rectangle area is: ", (&r1).Area_by_value());
//     fmt.Println("Rectangle area is: ", (&r1).Area_by_reference());

//     if 8%4 == 0 {
//         fmt.Println("8 is divisible by 4");
//     };

//     sum := 0;
// 	for i := 0; i < 10; i++ {
// 		sum += i;
// 		//sdaadsd
// 		hsi = -1;
// 	};
// 	fmt.Println(sum);
// };



// _Interfaces_ are named collections of method
// signatures.

// package main;

// import "fmt";
// import "math";

// // Here's a basic interface for geometric shapes.
// type geometry interface {
//     area() float64;
//     perim() float64;
// };

// // For our example we'll implement this interface on
// // `rect` and `circle` types.
// type rect struct {
//     width, height float64;
// };
// type circle struct {
//     radius float64;
// };

// To implement an interface in Go, we just need to
// implement all the methods in the interface. Here we
// implement `geometry` on `rect`s.
// func area(r rect) (float64,int) {
//     return r.width * r.height, 34;
// };
// func  perim(r rect) float64 {
//     return 2*r.width + 2*r.height;
// };

// The implementation for `circle`s.
// func  area(c circle) float64 {
//     return math.Pi * c.radius * c.radius;
// };
// func  perim(c circle) float64 {
//     return 2 * math.Pi * c.radius;
// };

// If a variable has an interface type, then we can call
// methods that are in the named interface. Here's a
// generic `measure` function taking advantage of this
// to work on any `geometry`.
// func measure(g geometry) {
// 	fmt.Println(g);
// 	x,y = area(g);
//     fmt.Println(g.area());
//     fmt.Println(g.perim());
// };

// func main() {
    // r := rect{width: 3, height: 4};
    // c := circle{radius: 5};

    // The `circle` and `rect` struct types both
    // implement the `geometry` interface so we can use
    // instances of
	// these structs as arguments to `measure`.
	
//     measure(r);
//     measure(c);
// };

// type Node struct {
// 	Next  *Node;
// 	Value interface{};
// };
// var first *Node;


// func main() {
//     // r := rect{width: 3, height: 4}
//     // c := circle{radius: 5}
    
//     // The `circle` and `rect` struct types both
//     // implement the `geometry` interface so we can use
//     // instances of
// 	// these structs as arguments to `measure`.
// 	// visited := make(a);
// 	// for n := first; n != nil; n = n.Next {
// 	// 	if visited[n] {
// 	// 		fmt.Println("cycle detected");
// 	// 		break;
// 	// 	};
// 	// 	visited[n] = true;
// 	// 	fmt.Println(n.Value);
// 	// };
//     // measure(r);
// 	// measure(c);
// 	// var n int =10;
// 	var a [2]string;
// 	a[n] = 2;
// 	a[1] = "World";
// 	if a == 0{
// 		v = 90;
// 	}
// 	else{
// 		g = 0-9;
// 		i = 90*7;
// 	};
// 	// var b int = map[1];
// 	// visited[n] = true;
// 	// fmt.Println(a[0], a[1]);
// };


//this file contains opening and closing file example
package main;
import (
    "bufio";
    "fmt";
    "io";
    "io/ioutil";
    "os";
);

func check(e error) {
    if e != nil {
        panic(e);
    };
};

type geometry interface {
	    area() float64;
	    perim() float64;
	};
	
	// For our example we'll implement this interface on
	// `rect` and `circle` types.
	type rect struct {
	    width, height float64;
	};
	type circle struct {
	    radius float64;
	};

	func check(e ...int,r int) int{
		if e != nil {
			panic(e);
		};
	};
func main() {
	i = 0;
	// var a = map[Node];
	m := make(map[string]int);
// Set key/value pairs using typical name[key] = val syntax.

	m["k1"] = 7;
	_, prs := m["k2"];
    fmt.Println("prs:", prs);
// You can also declare and initialize a new map in the same line with this syntax.

	n := map[string]int{"foo": 1, "bar": 2};
	r := rect{width: 3, height: 4};
    fmt.Println("map:", n);
};