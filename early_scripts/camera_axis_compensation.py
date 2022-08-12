def get_distance_point(Gpfpd, distance, direction):
    """
    根据经纬度，距离，方向获得一个地点
    :param lat: 纬度
    :param lon: 经度
    :param distance: 距离（千米）
    :param direction: 方向（北：0，东：90，南：180，西：360）
    :return:
    """
    cam_pos = np.zeros([len(Gpfpd),2])
    for ipos in range(1,len(Gpfpd)):
        lat = float(Gpfpd[ipos][6])
        lon = float(Gpfpd[ipos][7])
        start = geopy.Point(lat, lon)
        dire = float(gpfpd[ipos][3]) - direction
        d = geopy.distance.VincentyDistance(meters=distance)
        dst = d.destination(point=start, bearing=dire)
        cam_pos[ipos][0] = dst.latitude
        cam_pos[ipos][1] = dst.longitude
    return cam_pos
