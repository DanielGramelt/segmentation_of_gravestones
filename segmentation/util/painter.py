import numpy as np
import open3d as o3d


def color_point_cloud_by_threshold(point_cloud, threshold):
    '''
    Colors a point cloud by a given global threshold
    :param point_cloud: The point cloud to be colored
    :param threshold: The threshold that segments the point cloud
    :return: The colored point cloud
    '''
    point_values = point_cloud.points
    colors = np.empty_like(point_values)
    for i in range(len(colors)):
        if point_values[i][2] <= threshold:
            colors[i] = [0.5, 0.5, 0.5]
        else:
            colors[i] = [1, 0, 0]
    return create_point_cloud(point_cloud.points, colors)


def color_point_cloud_by_values(point_cloud, segmented_data_array):
    '''
    Colors a point cloud with confidence values
    :param point_cloud: The to be colored point cloud
    :param segmented_data_array: The confidence values for the point cloud points
    :return: The colored point cloud
    '''
    colors = np.empty_like(point_cloud.points)
    for i in range(len(colors)):
        if segmented_data_array[i] >= 0:
            colors[i] = [segmented_data_array[i], segmented_data_array[i], segmented_data_array[i]]
        else:
            colors[i] = [0, 0, 0]
    return create_point_cloud(point_cloud.points, colors)


def color_point_cloud_by_subset(point_cloud, subset):
    '''
    Colors a subset of a point cloud
    :param point_cloud: The to be colored point cloud
    :param subset: The subset of points which shall be highlighted
    :return: The colored point cloud
    '''
    inlier_cloud = point_cloud.select_by_index(subset)
    inlier_cloud.paint_uniform_color([1.0, 0, 0])
    outlier_cloud = point_cloud.select_by_index(subset, invert=True)
    outlier_cloud.paint_uniform_color([0.5, 0.5, 0.5])

    segmented_points = np.concatenate((inlier_cloud.points, outlier_cloud.points))
    segmented_colors = np.concatenate((inlier_cloud.colors, outlier_cloud.colors))
    return create_point_cloud(segmented_points, segmented_colors)


def color_segmented_point_cloud_by_confidence(segmented_point_cloud, confidence):
    '''
    Colors only the confident inscription points of a segmented point cloud
    :param segmented_point_cloud: The segmented point cloud
    :param confidence: The confidence value between 0 and 1. Smaller equals more confident
    :return: The colored point cloud
    '''
    cloud_colors = segmented_point_cloud.colors
    colors = np.zeros_like(cloud_colors)
    for index in range(len(colors)):
        if cloud_colors[index][0] < confidence:
            colors[index] = [0, 0, 0]
        else:
            colors[index] = [1, 1, 1]
    return create_point_cloud(segmented_point_cloud.points, colors)


def create_point_cloud(points, colors):
    '''
    Creates a new point cloud with given point and color values
    :param points: The point values of the point cloud
    :param colors: The color values of the point cloud
    :return: The created point cloud
    '''
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    point_cloud.colors = o3d.utility.Vector3dVector(colors)
    return point_cloud
