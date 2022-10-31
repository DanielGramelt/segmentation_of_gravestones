import numpy as np
from segmentation_of_gravestones.segmentation.util.painter import color_point_cloud_by_threshold


def segment_point_cloud(point_cloud, number_of_thresholds):
    '''
    Calculates the best global threshold with Otsu's method
    :param point_cloud: The point cloud to be segmented
    :param number_of_thresholds: The number of thresholds from which the best one shall be selected
    :return: Colored segmented point cloud
    '''
    point_array = point_cloud.points
    depth_data = [row[2] for row in point_array]
    best_threshold = 0
    best_variance = 0
    step = abs(min(depth_data) - max(depth_data)) / number_of_thresholds
    for step_counter in range(number_of_thresholds):
        threshold = min(depth_data) + step_counter * step
        between_class_variance = rate_threshold(depth_data, threshold)
        if between_class_variance > best_variance:
            best_threshold = threshold
            best_variance = between_class_variance
        print(str((step_counter / number_of_thresholds) * 100) + "%")
    print("Best threshold is: " + str(best_threshold))
    return color_point_cloud_by_threshold(point_cloud, best_threshold)


def rate_threshold(depth_data, threshold):
    '''
    Calculates the between class variance for a given threshold
    :param depth_data: An array of depth values of the point cloud
    :param threshold: The threshold to be tested
    :return: The between class variance for the given threshold
    '''
    unique, counts = np.unique(depth_data, return_counts=True)
    total_points = len(depth_data)

    w_inscription = 0
    for index in range(len(unique)):
        if unique[index] <= threshold:
            w_inscription += counts[index] / total_points
        else:
            break
    w_not_inscription = 1 - w_inscription
    y_inscription = 0
    for index in range(len(unique)):
        if unique[index] <= threshold:
            y_inscription += (unique[index] * (counts[index] / total_points) / w_inscription)
        else:
            break
    y_not_inscription = 0
    for index in range(len(unique)):
        if unique[index] > threshold:
            y_not_inscription += (unique[index] * (counts[index] / total_points) / w_not_inscription)

    between_class_variance = w_inscription * w_not_inscription * pow((y_not_inscription - y_inscription), 2)
    return between_class_variance
