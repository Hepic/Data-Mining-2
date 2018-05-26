import math


def haversine(lat1, long1, lat2, long2):
    R = 6371000

    latRad1 = math.radians(lat1)
    latRad2 = math.radians(lat2)
    dLatRad = math.radians(lat2 - lat1)
    dLongRad = math.radians(long2 - long1)

    val1 = math.sin(dLatRad / 2) * math.sin(dLatRad / 2) + \
           math.cos(latRad1) * math.cos(latRad2) * \
           math.sin(dLongRad / 2) * math.sin(dLongRad/2)

    val2 = 2 * math.atan2(math.sqrt(val1), math.sqrt(1 - val1))
    dst = R * val2 / 1000
    dst = round(dst, 2)

    return dst


def DTW(seq1, seq2):
    N = len(seq1)
    M = len(seq2)
    dtwArr = [[0] * (M + 1) for i in range(N + 1)]
    
    for i in range(1, N + 1):
        dtwArr[i][0] = float('inf') 

    for i in range(1, M + 1):
        dtwArr[0][i] = float('inf')
    
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            # seq[2] = latitude, seq[1] = longitude
            cost = haversine(seq1[i - 1][2], seq1[i - 1][1], seq2[j - 1][2], seq2[j - 1][1])
            dtwArr[i][j] = cost + min(min(dtwArr[i - 1][j], dtwArr[i][j - 1]), dtwArr[i - 1][j - 1])

    return dtwArr[N][M]


def LCS(seq1, seq2):
    THRESHOLD = 0.2 # 200 meters
    
    N = len(seq1)
    M = len(seq2)
    lcsArr = [[0] * (M + 1) for i in range(N + 1)]

    for i in range(1, N + 1):
        for j in range(1, M + 1): 
            # seq[2] = latitude, seq[1] = longitude
            cost = haversine(seq1[i - 1][2], seq1[i - 1][1], seq2[j - 1][2], seq2[j - 1][1])
            lcsArr[i][j] = max(max(lcsArr[i - 1][j], lcsArr[i][j - 1]), lcsArr[i - 1][j - 1])
 
            if cost <= THRESHOLD:
                lcsArr[i][j] = max(lcsArr[i][j], lcsArr[i - 1][j - 1] + 1)
    
    path = []
    i, j = N, M

    while i >= 1 and j >= 1:
        # seq[2] = latitude, seq[1] = longitude
        cost = haversine(seq1[i - 1][2], seq1[i - 1][1], seq2[j - 1][2], seq2[j - 1][1])

        if cost <= THRESHOLD:
            path.append(seq1[i - 1])
            i, j = i - 1, j - 1 
        elif lcsArr[i - 1][j] > lcsArr[i][j - 1]:
            i -= 1
        else:
            j -= 1

    path = path[::-1]
    return lcsArr[N][M], path
