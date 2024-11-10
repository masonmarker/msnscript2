





def rotate(array, k):
    
    part1 = array[0:-k]
    part2 = array[-k:]
    return part2 + part1
    
    
    
assert(rotate([1,2,3,4,5,6,7], 3) == [5,6,7,1,2,3,4])
assert(rotate([-1,-100,3,99], 2) == [3,99,-1,-100])
assert(rotate([1,2,3,4,5,6,7], 0) == [1,2,3,4,5,6,7])
assert(rotate([1,2,3,4,5,6,7], 7) == [1,2,3,4,5,6,7])