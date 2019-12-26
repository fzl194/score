import numpy as np

def List_Max(a):
    return np.array(a).max()

def List_Min(a):
    return np.array(a).min()

def List_Avg(a):
    return round(np.array(a).mean(), 3)

def List_Var(a):
    return round(np.array(a).var(), 3)

def List_Std(a):
    return round(np.array(a).std(), 3)

def List_Mid(a):
    return np.median(np.array(a))

def List_Count(a, L, R):
    ans = 0
    for i in a:
        if i >= L and i <= R:
            ans += 1
    return ans

def List_Length(a):
    return len(a)

def List_Sort(a):
    a.sort(reverse=True)
    Map = {}
    n = len(a)
    for i in range(n):
        if i != 0 and a[i] == a[i - 1]:
            continue
        else:
            Map[a[i]] = i + 1
    return Map