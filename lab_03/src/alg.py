def FindElem(arr, el):
    cnt = 0
    for i in range(len(arr)):
        cnt += 1
        if arr[i] == el:
            return i, cnt
    return -1, cnt

def BinFindElem(arr, el):
    left = 0
    right = len(arr) - 1
    cnt = 0

    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] < el:
            cnt += 1
            left = mid + 1
        elif arr[mid] > el:
            right = mid - 1
            cnt += 2
        else:
            cnt += 2
            return mid, cnt

    return -1, cnt

