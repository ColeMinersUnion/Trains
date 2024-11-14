def greenDefault()->list:
    KtoQ = [i for i in range(63, 101)]
    BackwardsN = [i for i in range(85, 76, -1)]
    RtoZ = [i for i in range(101, 151)]
    BackFtoD = [i for i in range(28, 1, -1)]
    Incoming = []
    Incoming.extend(KtoQ)
    Incoming.extend(BackwardsN)
    Incoming.extend(RtoZ)
    Incoming.extend(BackFtoD)
    Outgoing = [1]
    DtoYard = [i for i in range(13, 58)]
    Outgoing.extend(DtoYard)
    return Incoming, Outgoing

    

if __name__ == '__main__':
    I, O = greenDefault()
    print(I)
    print(O)