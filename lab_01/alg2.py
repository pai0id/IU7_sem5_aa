def memLev(s1, s2):
    n, m = len(s1), len(s2)
    if n > m:
        s1, s2 = s2, s1
        n, m = m, n

    curr = range(n + 1)
    for i in range(1, m + 1):
        prev, curr = curr, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = prev[j] + 1, curr[j - 1] + 1, prev[j - 1]
            if s1[j - 1] != s2[i - 1]:
                change += 1
            curr[j] = min(add, delete, change)
    
    return curr[n]

