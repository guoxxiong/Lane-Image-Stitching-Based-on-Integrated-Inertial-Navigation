import geopy.distance
from geopy.distance import geodesic
import math

def get_distance_point(lat, lon, distance, direction):
    """
    根据经纬度，距离，方向获得一个地点
    :param lat: 纬度
    :param lon: 经度
    :param distance: 距离（千米）
    :param direction: 方向（北：0，东：90，南：180，西：360）
    :return:
    """
    start = geopy.Point(lat, lon)
    d = geopy.distance.VincentyDistance(meters=distance)
    return d.destination(point=start, bearing=direction)

if __name__ == "__main__":
    dst = get_distance_point(39.97792111, 116.34614112, pow(pow(0.5, 2) + pow(0.6, 2), 0.5), 82.936 - math.atan2(0.5, 0.6) * 180 / math.pi)
    print(dst.latitude, dst.longitude)
    level_distance = geodesic((39.97792111, 116.34614112), (dst.latitude, dst.longitude)).m
    print(level_distance)