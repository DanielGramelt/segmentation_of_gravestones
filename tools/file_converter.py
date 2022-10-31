import numpy as np
import open3d as o3d


def point_cloud_to_mesh(point_cloud):
    '''
    Converts a point cloud to a mesh
    :param point_cloud: The point cloud to be converted
    :return: The generated mesh
    '''
    distances = point_cloud.compute_nearest_neighbor_distance()
    average_distance = np.mean(distances)
    radius = 1.25 * average_distance
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(point_cloud,
                                                                           o3d.utility.DoubleVector([radius]))
    return mesh


def mesh_to_point_cloud(mesh, number_of_points):
    '''
    Converts a mesh to a point cloud
    :param mesh: The mesh to be converted
    :param number_of_points: The number of how many points shall be in the resulting point cloud
    :return: The generated point cloud
    '''
    point_cloud = mesh.sample_points_poisson_disk(number_of_points)
    return point_cloud
