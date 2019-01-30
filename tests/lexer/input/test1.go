package main

import (
	"fmt"
	"math/cmplx"
)

var (
	ToBe   bool       = false
	MaxInt uint64     = 1<<64 - 1
	z      complex128 = cmplx.Sqrt(-5.9 + 12iota)
)


func main() {
	const x = "%T(x)\n" // comment
	fmt.Printf(f, ToBe, ToBe) // Hi this is a comment too
	// This is as well! // yo
	// This is a comment too!
	fmt.Printf(f, MaxInt, MaxInt) // yo yo
	fmt.Printf(f, z, z)
	var a = 0xffff
	var d int8 = 32
	v := 89.09
}
