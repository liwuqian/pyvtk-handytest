import vtkmodules.all as vtk
import math


def set_z_direction_of_matrix(m, v):
    # Normalize vector v to unit length
    normalized_v = v
    vtk.vtkMath.Normalize(normalized_v)
    print(normalized_v)

    # Find two perpendicular vectors in the plane formed by x and y directions
    x_axis = [1.0, 0.0, 0.0]  # Assuming x-direction of the matrix is [1, 0, 0]
    y_axis = [0.0, 1.0, 0.0]  # Assuming y-direction of the matrix is [0, 1, 0]

    # Compute the cross product to find the perpendicular vector in the plane
    a = [0.0, 0.0, 0.0]
    vtk.vtkMath.Cross(normalized_v, x_axis, a)
    if vtk.vtkMath.Norm(a) == 0:
        vtk.vtkMath.Cross(normalized_v, y_axis, a)

    # Normalize the perpendicular vector 'a'
    vtk.vtkMath.Normalize(a)

    # Compute the second perpendicular vector
    b = [0.0, 0.0, 0.0]
    vtk.vtkMath.Cross(normalized_v, a, b)

    # Set the first three columns of the matrix
    for i in range(3):
        m.SetElement(i, 0, a[i])
        m.SetElement(i, 1, b[i])
        m.SetElement(i, 2, normalized_v[i])

    return m


def create_bent_tube2():
    # Create points along the tube's path
    points = vtk.vtkPoints()
    num_points = 6
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(2, 0, 0)
    points.InsertNextPoint(3, 1, 0)
    points.InsertNextPoint(4, 1, 0)
    points.InsertNextPoint(5, 0, 0)
    points.InsertNextPoint(6, 0, 0)

    # Fit a spline to the points
    spline = vtk.vtkParametricSpline()
    spline.SetPoints(points)
    functionsource = vtk.vtkParametricFunctionSource()
    functionsource.SetParametricFunction(spline)
    functionsource.SetUResolution(10 * points.GetNumberOfPoints())
    functionsource.Update()

    # polydata
    tubePolydata = vtk.vtkPolyData()
    tubePolydata = functionsource.GetOutput()
    # print(tubePolydata)

    tube_radius = 0.5
    # Create a tube filter to create the bent tube
    tube_filter = vtk.vtkTubeFilter()
    tube_filter.SetInputData(tubePolydata)
    tube_filter.SetRadius(tube_radius)  # Set the radius of the tube
    tube_filter.SetNumberOfSides(50)  # Set the number of sides for the tube
    tube_filter.SetVaryRadiusToVaryRadiusByAbsoluteScalar()

     # Create a disk source for the tube's end caps
    disk_source = vtk.vtkDiskSource()
    disk_source.SetInnerRadius(0)  # Inner radius (zero for a complete disk)
    disk_source.SetOuterRadius(tube_radius)  # Outer radius (matching the tube radius)
    disk_source.SetRadialResolution(20)  # Number of radial divisions
    disk_source.SetCircumferentialResolution(20)  # Number of circumferential divisions

    # Translate the disks to the starting and ending points of the tube
    num_interpolate = tubePolydata.GetNumberOfPoints()
    p_start_0 = [0, 0, 0]
    p_start_1 = [0, 0, 0]
    p_end_0 = [0, 0, 0]
    p_end_1 = [0, 0, 0]
    tubePolydata.GetPoints().GetPoint(0, p_start_0)
    tubePolydata.GetPoints().GetPoint(1, p_start_1)
    tubePolydata.GetPoints().GetPoint(num_interpolate - 1, p_end_0)
    tubePolydata.GetPoints().GetPoint(num_interpolate - 2, p_end_1)

    # tube_start = points.GetPoint(0)
    # tube_start_1 = points.GetPoint(1)
    start_dir = [p_start_0[0] - p_start_1[0], 
                 p_start_0[1] - p_start_1[1], 
                 p_start_0[2] - p_start_1[2]]
    # print('start_dir:', start_dir)
    end_dir = [p_end_0[0] - p_end_1[0], 
               p_end_0[1] - p_end_1[1], 
               p_end_0[2] - p_end_1[2]]

    start_disk_transform = vtk.vtkTransform()
    mat = vtk.vtkMatrix4x4()
    set_z_direction_of_matrix(mat, start_dir)
    mat.SetElement(0, 3, p_start_0[0])
    mat.SetElement(1, 3, p_start_0[1])
    mat.SetElement(2, 3, p_start_0[2])
    start_disk_transform.SetMatrix(mat)

    end_disk_transform = vtk.vtkTransform()
    mat_end = vtk.vtkMatrix4x4()
    set_z_direction_of_matrix(mat_end, end_dir)
    mat_end.SetElement(0, 3, p_end_0[0])
    mat_end.SetElement(1, 3, p_end_0[1])
    mat_end.SetElement(2, 3, p_end_0[2])
    end_disk_transform.SetMatrix(mat_end)

    start_disk = vtk.vtkTransformPolyDataFilter()
    start_disk.SetInputConnection(disk_source.GetOutputPort())
    start_disk.SetTransform(start_disk_transform)

    end_disk = vtk.vtkTransformPolyDataFilter()
    end_disk.SetInputConnection(disk_source.GetOutputPort())
    end_disk.SetTransform(end_disk_transform)

    # Combine the tube and its end caps using vtkAppendPolyData
    append_filter = vtk.vtkAppendPolyData()
    append_filter.AddInputConnection(tube_filter.GetOutputPort())
    append_filter.AddInputConnection(start_disk.GetOutputPort())
    append_filter.AddInputConnection(end_disk.GetOutputPort())
    append_filter.Update()

    # Create a mapper and actor for visualization
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(append_filter.GetOutputPort())  # Use the smoothed polydata
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    # taking effect wihle not used scalar data
    actor.GetProperty().SetColor(0, 1, 0)

    return actor


def main():
    # Create a renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # Add the bent tube to the renderer
    actor = create_bent_tube2()
    renderer.AddActor(actor)

    # add axes
    axes = vtk.vtkAxesActor()
    # renderer.AddActor(axes)

    # Set the background color and start the interaction
    renderer.SetBackground(1, 1, 1)  # White background
    render_window.SetSize(800, 600)
    render_window.Render()
    interactor.Start()

if __name__ == "__main__":
    main()
