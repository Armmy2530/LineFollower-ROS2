import cv2
import numpy as np

error_gap = 10
min_area = 20

def draw_centerline(img):
    img_with_points = img.copy()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_thr = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
    h, w = img_gray.shape
    
    for row_index in range(0,h,10):
        row_data = img_thr[row_index]
        black_detect = find_rows_blackarea(row_data)
        center_point = filter_areaLargest(black_detect)
        
        # Draw a red point at the center point
        if center_point is not None:
            cv2.circle(img_with_points, (center_point[2], row_index), 3, (0, 0, 255), -1)
    
    return img_with_points

def find_rows_blackarea(rows_data):
    lane_data = []
    t_start = -1
    t_end = -1
    t_error = 0

    for i, data in enumerate(rows_data):
        if data == 255:
            if t_start == -1:
                t_start = i
                t_error = 0
            t_end = i
        else:
            t_error += 1
            if t_error > error_gap:
                if t_end - t_start > min_area:
                    lane_data.append([t_start, t_end])
                t_start = -1
                t_end = -1

    # add data if last data is black to border
    if t_end - t_start > min_area:
        lane_data.append([t_start, t_end])

    return lane_data

def filter_areaLargest(data):
    largest_area = 0
    largest_area_coords = None

    for start, end in data:
        area = end - start
        if area > largest_area:
            largest_area = area
            largest_area_coords = [int(start), int(end), int((end - start) / 2 + start)]
            
    return largest_area_coords

def find_point(img,rows_position):
    data = []
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_thr = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
    h, w = img_gray.shape
    try:
        for row_index in rows_position:
            row_data = img_thr[row_index]
            black_detect = find_rows_blackarea(row_data)
            center_point = filter_areaLargest(black_detect)
            center_point.extend([int(row_index)])
            data.append(center_point)
        return data
    except:
        return [[-1,-1,-1,-1]]

def drawimg_point(img,point):
    # Draw a red point at the center point
    for i in point:
        if i is not None:
            cv2.circle(img, (i[2], i[3]), 3, (0, 0, 255), -1)
    return img
