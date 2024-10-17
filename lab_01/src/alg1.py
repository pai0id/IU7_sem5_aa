def reqLev(s1, s2):
    if len(s2) == 0:
        return len(s1)
    elif len(s1) == 0:
        return len(s2)
    elif s1[0] == s2[0]:
        return reqLev(s1[1:], s2[1:])
    else:
        return 1 + min(reqLev(s1[1:], s2), reqLev(s1[1:], s2[1:]), reqLev(s1, s2[1:]))

