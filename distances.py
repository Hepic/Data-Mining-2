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
