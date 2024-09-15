def dLev(s1, s2):
    d = {}
    
    for i in range(-1,len(s1)+1):
        d[(i,-1)] = i+1
    for j in range(-1,len(s2)+1):
        d[(-1,j)] = j+1
 
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i,j)] = min(
                           d[(i-1,j)] + 1,
                           d[(i,j-1)] + 1,
                           d[(i-1,j-1)] + cost,
                          )
            if i and j and s1[i] == s2[j-1] and s1[i-1] == s2[j]:
                d[(i,j)] = min(d[(i,j)], d[i-2,j-2] + 1)
 
    return d[len(s1)-1,len(s2)-1]


# s1 = "1234"
# s2 = "2143"

# print(dlev(s1, s2))