def reward_function(params):
    import math

    reward = 0
    score_except = 100
    score_max = 5

    progress = params['progress']
    steering_angle = params['steering_angle']
    steps = params['steps']
    track_width = params['track_width']
    heading = params['heading']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']

    x = params['x']
    y = params['y']
    source_idx = closest_waypoints[0]  # closest before car
    target_idx = source_idx + 2

    # algorithm to find the farest visible waypoints
    loop = True
    while loop:
        if source_idx == target_idx:
            # all waypoints has been checked
            return -score_except

        target = waypoints[target_idx % len(waypoints)]

        for i in range(source_idx + 1, target_idx):
            current = waypoints[i % len(waypoints)]
            print(current)
            if (dps(current[0], current[1], x, y, target[0], target[1]) >= math.hypot(track_width / 2,
                                                                                      track_width / 2)):
                loop = False
                break

        if loop:
            target_idx = target_idx + 1
        else:
            target_idx = target_idx - 1
            # then exit the loop

    target = waypoints[target_idx % len(waypoints)]
    print("target: " + str(target))

    # angle from car to the farest visible waypoint
    best_dir = atan2_deg(x, y, target[0], target[1])
    best_dir = nor(best_dir)
    print("best dir: " + str(best_dir))

    heading = nor(heading)
    print("heading: " + str(heading))

    # compute angle diff
    angle_diff = math.fabs(angle_min_diff(heading, best_dir))
    print("diff: " + str(angle_diff))

    # reward computing
    ratio = round(pow(float(1 - angle_diff / 180), 2), 1)
    reward += score_max * ratio
    if progress == 100:
        reward += score_except

    log(closest_waypoints, track_width, steering_angle, steps, x, y, target[0], target[1], best_dir)

    return reward


def dps(px, py, x1, y1, x2, y2):
    import math

    mag = math.hypot(x2 - x1, y2 - y1)

    if mag < 0.00000001:
        dst = 9999
        return dst

    u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
    u = u1 / (mag * mag)

    if (u < 0.00001) or (u > 1):
        ix = math.hypot(x1 - px, y1 - py)
        iy = math.hypot(x2 - px, y2 - py)
        if ix > iy:
            dst = iy
        else:
            dst = ix
    else:
        ix = x1 + u * (x2 - x1)
        iy = y1 + u * (y2 - y1)
        dst = math.hypot(ix - px, iy - py)

    return dst


def angle_min_diff(x, y):
    arg = (y - x) % 360
    if arg < 0:
        arg = arg + 360
    if arg > 180:
        arg = arg - 360
    return -arg


def atan2_deg(x1, y1, x2, y2):
    import math
    rad = math.atan2(y2 - y1, x2 - x1)
    deg = math.degrees(rad)
    return nor(deg)


def nor(angle):
    angle = angle % 360
    if angle < 0:
        angle = angle + 360
    return angle


def log(closest_waypoints, track_width, steering_angle, steps, x, y, target_x, target_y, best_dir):
    print("Waypoint0:{},X:{},Y:{},targetX:{},targetY:{},heading:{},trackwidth:{},steeringangle:{},steps:{}".format(
        closest_waypoints[0], x, y, target_x, target_y, best_dir, track_width, steering_angle, steps))
