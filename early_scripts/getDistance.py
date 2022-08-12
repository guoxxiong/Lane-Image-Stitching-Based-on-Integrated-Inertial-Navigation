from geopy.distance import geodesic


level_distance = geodesic((39.97793135, 116.34689478), (39.97793084, 116.34689635)).m #跟据经纬度求解两点之间的距离
print(level_distance)