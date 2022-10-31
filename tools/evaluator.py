import math
import numpy as np
import open3d as o3d


def compare_to_ground_truth(ground_truth_point_cloud, segmented_point_cloud, color_value_inscription):
    '''
    Compares a ground truth with a segmentation and calculates precision, recall, accuracy, the f1 score and the
    Matthews correlation coefficient.
    :param ground_truth_point_cloud: The ground truth point cloud
    :param segmented_point_cloud: The segmentation to be compared to the ground truth
    :param color_value_inscription: The value of the segmentation color until when a color describes an inscription
    :return: A coloured point cloud which displays the false and correct segmented points
    '''
    truth_colors = np.asarray(ground_truth_point_cloud.colors)
    segmented_colors = np.asarray(segmented_point_cloud.colors)

    result_colors = np.zeros_like(segmented_colors)
    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0
    for i in range(len(segmented_colors) - 1):
        if not is_red(truth_colors[i]) and segmented_colors[i][0] > color_value_inscription:
            true_positives = true_positives + 1
            result_colors[i] = [0, 1, 0]
        elif not is_green(truth_colors[i]) and segmented_colors[i][0] <= color_value_inscription:
            true_negatives = true_negatives + 1
            result_colors[i] = [0, 1, 0]
        elif is_green(truth_colors[i]) and segmented_colors[i][0] <= color_value_inscription:
            false_negatives = false_negatives + 1
            result_colors[i] = [1, 0, 0]
        elif is_red(truth_colors[i]) and segmented_colors[i][0] > color_value_inscription:
            false_positives = false_positives + 1
            result_colors[i] = [1, 0, 0]
    print("True positives: " + str(true_positives))
    print("True negatives: " + str(true_negatives))
    print("False positives: " + str(false_positives))
    print("False negatives: " + str(false_negatives))

    precision = true_positives / (false_positives + true_positives)
    print("Precision: " + str(precision))

    recall = true_positives / (false_negatives + true_positives)
    print("Recall: " + str(recall))

    accuracy = (true_positives + true_negatives) / (true_positives + true_negatives + false_positives + false_negatives)
    print("accuracy: " + str(accuracy))

    f1 = 2 * (precision * recall) / (precision + recall)
    print("f1: " + str(f1))

    mcc = (true_positives * true_negatives - false_positives * false_negatives) / math.sqrt(
        (true_positives + false_positives) * (true_positives + false_negatives) * (true_negatives + false_positives) * (
                true_negatives + false_negatives))
    print("Matthews correlation coefficient: " + str(mcc))

    result_cloud = o3d.geometry.PointCloud()
    result_cloud.points = segmented_point_cloud.points
    result_cloud.colors = o3d.utility.Vector3dVector(result_colors)
    return result_cloud


def is_green(array):
    '''
    Says if a RGB color array represents green
    :param array: The RGB color array
    :return: True or False
    '''
    red = 0
    green = 1
    blue = 2
    if array[green] > array[red] \
            and array[green] > array[blue]:
        return True
    else:
        return False


def is_blue(array):
    '''
    Says if a RGB color array represents blue
    :param array: The RGB color array
    :return: True or False
    '''
    red = 0
    green = 1
    blue = 2
    if array[blue] > array[red] \
            and array[blue] > array[green]:
        return True
    else:
        return False


def is_red(array):
    '''
    Says if a RGB color array represents red
    :param array: The RGB color array
    :return: True or False
    '''
    red = 0
    green = 1
    blue = 2
    if array[red] > array[green] \
            and array[red] > array[blue]:
        return True
    else:
        return False
