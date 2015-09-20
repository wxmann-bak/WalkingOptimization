__author__ = 'tangz'

def streetwidth(lanes, lanewidth=12, unit='ft'):
    total_width = lanes * lanewidth
    if unit == 'ft':
        # conversion from ft to mi
        return total_width * 0.000189394
    elif unit == 'yd':
        # yd to mi
        return total_width * 0.000568182
    else:
        # assume mi
        return total_width

def hr_to_min(hr):
    return hr * 60


walk_speed = 3 / (hr_to_min(1))  # 3 mph => mi/min
block_distance = 0.5  # mi
street_width = streetwidth(4)

time_cross_street = street_width / walk_speed
time_cross_block = block_distance / walk_speed
light_wait_time = time_cross_street * 2

