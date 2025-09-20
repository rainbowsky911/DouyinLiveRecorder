def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid=left+(right-left)//2
        if arr[mid] == target:
            return mid
        if(arr[mid] < target):
            left = mid + 1
        if(arr[mid] > target):
            right = mid - 1


# 示例
arr = [1, 3, 5, 7, 9, 11]
print(binary_search(arr, 7))