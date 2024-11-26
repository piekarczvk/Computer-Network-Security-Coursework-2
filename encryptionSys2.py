#Generate a set of positive integers (e1, e2, ..., en) where each element ei is greater than the sum of all previous elements in the set
#n-elements in the set 
#returns a list
def generate_e(n):
    if n<=0:
        return []
    result=[1]
    for i in range(1,n):
        next_element=sum(result)+1
        result.append(next_element)
    return result