import  math

# 根据两个点的经纬度求解方位角
def getDegree(latA, lonA, latB, lonB):
    radLatA = math.radians(latA)
    radLonA = math.radians(lonA)
    radLatB = math.radians(latB)
    radLonB = math.radians(lonB)
    dLon = (radLonB - radLonA)
    dLat = (radLatB - radLatA)
    y = math.sin(dLon) * math.cos(radLatB)
    x = math.cos(radLatA) * math.sin(radLatB) - math.sin(radLatA) * math.cos(radLatB) * math.cos(dLon)
    brng = math.degrees(math.atan2(y, x))
    brng = (brng + 360) % 360
    return brng

if __name__ == "__main__":
    d = getDegree(39.97792111, 116.34614112, 39.97792624, 116.34614737)
    print(d)