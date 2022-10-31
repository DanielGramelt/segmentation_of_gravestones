import multiprocessing
import os
from multiprocessing import shared_memory
from segmentation_of_gravestones.segmentation.util.time_estimator import estimate_time
from segmentation_of_gravestones.segmentation.util.painter import color_point_cloud_by_values

import numpy as np
import open3d as o3d


def segment_point_cloud(point_cloud, region_fraction):
    '''
    Set up of multiprocessing and shared memory for the segmentation with local thresholds
    :param point_cloud: The point cloud to be segmented
    :param region_fraction: The fraction of points, which defines the region of each local threshold
    :return: Colored segmentation result
    '''
    size = int(len(point_cloud.points) / region_fraction)
    print("Region size: " + str(size))
    cores = os.cpu_count()

    result_array_blueprint = np.zeros(len(point_cloud.points))
    completed_points_blue_print = np.zeros(cores)

    shared_mem = shared_memory.SharedMemory(create=True, size=result_array_blueprint.nbytes)
    counts_shared = shared_memory.SharedMemory(create=True, size=completed_points_blue_print.nbytes)

    completed_points_shared_name = counts_shared.name
    result_array_shared_name = shared_mem.name

    print("CPU Cores: " + str(cores))
    step = int(len(point_cloud.points) / cores)
    futures = []
    print("Starting Threads...")
    time_estimator = multiprocessing.Process(target=estimate_time, args=(
        result_array_shared_name, completed_points_shared_name, result_array_blueprint.shape,
        completed_points_blue_print.shape))
    time_estimator.daemon = True
    for core in range(cores):
        process = multiprocessing.Process(target=segment_array, args=(
            np.asarray(point_cloud.points), core * step, (core + 1) * step, size, result_array_shared_name, core,
            completed_points_shared_name, result_array_blueprint.shape, completed_points_blue_print.shape))

        futures.append(process)
        process.start()
    print("Threads started")
    time_estimator.start()
    for process in futures:
        process.join()
    time_estimator.kill()
    for process in futures:
        process.kill()
    result_memory = shared_memory.SharedMemory(name=result_array_shared_name)
    result_array = np.ndarray((result_array_blueprint.shape), dtype=np.float16, buffer=result_memory.buf)
    return color_point_cloud_by_values(point_cloud, result_array)


def segment_array(points, begin, stop, size, result_array_name, thread_number, point_counts_name, result_arrays_shape,
                  point_counts_shape):
    '''
    Segments a part of an array with point values
    :param points: Point values of a point cloud
    :param begin: Begin index on the point array for the segmentation
    :param stop: End index on the point array for the segmentation
    :param size: Size of the region for the local thresholds
    :param result_array_name: Name of the shared memory result array
    :param thread_number: Number of this thread
    :param point_counts_name: Name of the shared memory array for the count of already segmented points
    :param result_arrays_shape: Shape of the shared memory result array
    :param point_counts_shape: Shape of the shared memory array for the count of already segmented points
    :return: Nothing, result is accessible through the shared memory arrays
    '''
    result_memory = shared_memory.SharedMemory(name=result_array_name)
    result_array = np.ndarray((result_arrays_shape), dtype=np.float16, buffer=result_memory.buf)
    point_counts_memory = shared_memory.SharedMemory(name=point_counts_name)
    point_counts = np.ndarray((point_counts_shape), dtype=np.int64, buffer=point_counts_memory.buf)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    kd_tree = o3d.geometry.KDTreeFlann(pcd)
    for index in range(begin, stop):
        [k, idx, _] = kd_tree.search_knn_vector_3d(points[index], size)
        nearest_neighbours = np.asarray(points)[idx[1:], :]
        sub_array = [row[2] for row in nearest_neighbours]
        k = np.mean(sub_array)
        min = np.min(sub_array)
        max = np.max(sub_array)
        if points[index][2] >= k:
            result_array[index] = (points[index][2] - k) / (max - k)
        else:
            result_array[index] = (-1 * (k - points[index][2]) / (k - min))
        point_counts[thread_number] += 1


