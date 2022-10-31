from datetime import datetime

from segmentation_of_gravestones.segmentation import local_threshold_segmentation
from segmentation_of_gravestones.segmentation import otsu_segmentation
from segmentation_of_gravestones.segmentation import ransac_segmentation
from segmentation_of_gravestones.segmentation.util.painter import color_segmented_point_cloud_by_confidence
import open3d as o3d


def start_otsu_segmentation(output_file_path, point_cloud, number_of_thresholds):
    '''
    Starts the segmentation with Otsu's method, measures the time needed and saves the segmented point cloud
    :param output_file_path: The file path where the segmented point cloud shall be saved
    :param point_cloud: The point cloud to be segmented
    :param number_of_thresholds: The number of how many thresholds shall be compared by Otsu's method.
    :return: The segmented point cloud
    '''
    print("Starting segmentation with Otsu...")
    start = datetime.now()
    print("Segmentation started at: " + start.strftime("%H:%M:%S"))
    segmented = otsu_segmentation.segment_point_cloud(point_cloud, number_of_thresholds)
    end = datetime.now()
    print("\nSegmentation started at: " + start.strftime("%H:%M:%S") + " and ended at: " + end.strftime("%H:%M:%S"))
    duration = end - start
    print("Duration: " + str(duration))
    o3d.io.write_point_cloud(output_file_path, point_cloud)
    print("Saved result to " + output_file_path + "\n\n")
    return segmented


def start_ransac_segmentation(output_file_path, point_cloud, threshold, iterations):
    '''
    Starts the segmentation with RANSAC, measures the time needed and saves the segmented point cloud
    :param output_file_path: The file path where the segmented point cloud shall be saved
    :param point_cloud: The point cloud to be segmented
    :param threshold: The threshold for up to which distance a point still counts as inlier for the plane
    :param iterations: The number of planes to be tested
    :return: The segmented point cloud
    '''
    print("Starting segmentation with ransac...")
    start = datetime.now()
    print("Segmentation started at: " + start.strftime("%H:%M:%S"))
    segmented = ransac_segmentation.segment_point_cloud(point_cloud, threshold, iterations)
    end = datetime.now()
    print("\nSegmentation started at: " + start.strftime("%H:%M:%S") + " and ended at: " + end.strftime("%H:%M:%S"))
    duration = end - start
    print("Duration: " + str(duration))
    o3d.io.write_point_cloud(output_file_path, point_cloud)
    print("Saved result to " + output_file_path + "\n\n")
    return segmented


def start_local_threshold_segmentation(output_file_path, point_cloud, region_fraction):
    '''
    Starts the segmentation with local thresholds, measures the time needed and saves the segmented point cloud
    :param output_file_path: The file path where the segmented point cloud shall be saved
    :param point_cloud: The point cloud to be segmented
    :param region_fraction: The fraction of points, which defines the region of each local threshold
    :return: The segmented point cloud
    '''
    print("Starting segmentation with local thresholds...")
    start = datetime.now()
    print("Segmentation started at: " + start.strftime("%H:%M:%S"))
    segmented = local_threshold_segmentation.segment_point_cloud(point_cloud, region_fraction)
    end = datetime.now()
    print("\nSegmentation started at: " + start.strftime("%H:%M:%S") + " and ended at: " + end.strftime(
        "%H:%M:%S"))
    duration = end - start
    print("Duration: " + str(duration))
    o3d.io.write_point_cloud(output_file_path, point_cloud)
    print("Saved result to " + output_file_path + "\n\n")
    return segmented


if __name__ == '__main__':
    cloud = o3d.io.read_point_cloud("data/gravestone.ply")

    otsu_result = start_otsu_segmentation("output/otsu.ply", cloud, 10)
    ransac_result = start_ransac_segmentation("output/ransac.ply", cloud, 1, 500)
    local_threshold_result = start_local_threshold_segmentation("output/local_threshold.ply", cloud, 5000)

    confident_local_threshold_result = color_segmented_point_cloud_by_confidence(local_threshold_result, 0.15)

    print("Visualizing RANSAC result")
    o3d.visualization.draw_geometries([ransac_result])
    print("Visualizing Otsu result")
    o3d.visualization.draw_geometries([otsu_result])
    print("Visualizing local threshold result")
    o3d.visualization.draw_geometries([local_threshold_result])
    print("Visualizing confident local threshold result")
    o3d.visualization.draw_geometries([confident_local_threshold_result])
