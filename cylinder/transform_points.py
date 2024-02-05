import vtk

# Create a line source
line_source = vtk.vtkLineSource()
point1 = [0, 0, 0]
point2 = [1, 1, 0]
line_source.SetPoint1(point1)
line_source.SetPoint2(point2)

# Create a transform
transform = vtk.vtkTransform()
# transform.Translate(1.0, 2.0, 0.0) 
dir_vector = [point2[i] - point1[i] for i in range(3)]
vtk.vtkMath.Normalize(dir_vector)
normal_vector = [-dir_vector[1], dir_vector[0], 0]
distance = 2
distance_vector = [normal_vector[i]*distance for i in range(3)]
transform.Translate(distance_vector)

# Apply the transform to the line source
transform_filter = vtk.vtkTransformPolyDataFilter()
transform_filter.SetInputConnection(line_source.GetOutputPort())
transform_filter.SetTransform(transform)
transform_filter.Update()

# Get the transformed line
transformed_line = transform_filter.GetOutput()

# Print the original and transformed points
original_points = line_source.GetOutput().GetPoints()
transformed_points = transformed_line.GetPoints()

print("Original Line Points:")
for i in range(original_points.GetNumberOfPoints()):
    print(original_points.GetPoint(i))

print("\nTransformed Line Points:")
for i in range(transformed_points.GetNumberOfPoints()):
    print(transformed_points.GetPoint(i))
