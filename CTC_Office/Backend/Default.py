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

def greenSkips()->dict:
    YardtoGlenbury = [i for i in range(63, 66)]
    GlenburytoDormont = [i for i in range(66, 74)]
    DormonttoMTLebanon = [i for i in range(74, 78)]
    MTLebanonToPoplar = [i for i in range(78, 89)]
    PoplarToCastle = [i for i in range(89, 97)]
    #This was really cool, I was able to use the unpacking operator to make the list in one line
    CastleToPoplar = [97, 98, 99, 100, *(i for i in range(85, 76, -1))]
    PoplarToDormont = [i for i in range(101, 106)]
    DormontToGlenbury = [i for i in range(106, 115)]
    GlenburyToOverbrook = [i for i in range(115, 124)]
    OverbrookToInglewood = [i for i in range(124, 133)]
    InglewoodToCentral = [i for i in range(133, 142)]
    CentralToWhited = [*(i for i in range(142, 151)), *(j for j in range(28, 21, -1))]
    WhitedToStationD = [i for i in range(21, 15, -1)]
    StationDtoEdgebrook = [i for i in range(15, 8, -1)]
    EdgebrookToPioneer = [i for i in range(8, 1, -1)]
    PioneerToStationD = [1, *(i for i in range(13, 17))]
    StationDtoWhited = [i for i in range(17, 23)]
    WhitedToSouthBank = [i for i in range(23, 32)]
    SouthBankToCentral = [i for i in range(32, 40)]
    CentralToInglewood = [i for i in range(40, 49)]
    InglewoodToOverbrook = [i for i in range(49, 58)]
    ContinueToStart = [i for i in range(58, 63)]
    skips = {
        0: YardtoGlenbury,
        1: GlenburytoDormont,
        2: DormonttoMTLebanon,
        3: MTLebanonToPoplar,
        4: PoplarToCastle,
        5: CastleToPoplar,
        6: PoplarToDormont,
        7: DormontToGlenbury,
        8: GlenburyToOverbrook,
        9: OverbrookToInglewood,
        10: InglewoodToCentral,
        11: CentralToWhited,
        12: WhitedToStationD,
        13: StationDtoEdgebrook,
        14: EdgebrookToPioneer,
        15: PioneerToStationD,
        16: StationDtoWhited,
        17: WhitedToSouthBank,
        18: SouthBankToCentral,
        19: CentralToInglewood,
        20: InglewoodToOverbrook,
        21: ContinueToStart
    }
    return skips





if __name__ == '__main__':
    print(greenSkips())