package main;
import "fmt";
haystack := []int{1,2, 9, 20, 31, 45, 63, 70, 100};
func binarySearch(needle int) bool {
 
    low := 0;
    high := len(haystack) - 1;
 
    for low <= high{
        median := (low + high) / 2;
 
        if haystack[median] < needle {
            low = median + 1;
        }else{
            high = median - 1;
        };
    };
 
    if low == len(haystack) || haystack[low] != needle {
        return 0;
    };
 
    return 1;
}
 
 
func main(){
    // items := []int{1,2, 9, 20, 31, 45, 63, 70, 100};
    v := binarySearch(63);
    printf("%d",v);
}