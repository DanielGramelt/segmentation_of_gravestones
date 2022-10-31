# Implemented features

- Segmentation
  - RANSAC (segmentation/ransac_segmentation.py)
  - Otsu's method (segmentation/otsu_segmentation.py)
  - Local thresholds (segmentation/local_threshold_segmentation.py)
    - Show only confident inscriptions (segmentation/util/painter.py)


- Evaluation
  - Comparing a segmented point cloud to a ground truth (tools/evaluator)


- File types
  - Converting a mesh to a point cloud (tools/file_converter.py)
  - Converting a point cloud to a mesh  (tools/file_converter.py)


# Starting the program

Executing the main.py file through an editor or the console starts the program. The desired features are controlled via the main method in the main.py file. If one wants to apply this program to a use case, one must change this method.

By default, the program expects PLY files which are to be segmented in the data folder and writes the segmented results in the output folder. The desired paths must be adjusted in the main.py file before starting the program.