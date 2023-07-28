from random import randint


def get_random(num=7):
    return [randint(1, 15) for _ in range(num)]

def sort_values(arr):
    for num in range(len(arr)-1, -1, -1):
        for val in range(0, num+1):
            if arr[val] > arr[num]:
                arr[val], arr[num] = arr[num], arr[val]
    return sorted(arr)

def binarySearch(arr, x, low, high):
    if low > high:
        return False 
    else:
        mid = int((low + high) / 2)
        if x == arr[mid]:
            return True
        elif x > arr[mid]:
            return binarySearch(arr, x, mid + 1, high)
        else:
            return binarySearch(arr, x, low, mid - 1)
        

