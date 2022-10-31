from datetime import datetime
from segmentation_of_gravestones.segmentation.util.painter import color_point_cloud_by_subset


def segment_point_cloud(point_cloud, threshold, iterations):
    '''
    Calculates the largest plane through RANSAC
    :param point_cloud: The point cloud to be segmented
    :param threshold: The threshold for up to which distance a point still counts as inlier for the plane
    :param iterations: The number of planes to be tested
    :return: Segmented point cloud with coloured inliers of the greatest plane
    '''
    plane, inliers = point_cloud.segment_plane(distance_threshold=threshold, ransac_n=3, num_iterations=iterations)

    return color_point_cloud_by_subset(point_cloud, inliers)
