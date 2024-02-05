# generate a 2d bend rod through translating spline and making a closed loop
import vtkmodules.all as vtk

def create_spline():
    # Create points along the rod's path
    points = vtk.vtkPoints()
    num_points = 6
    points.InsertNextPoint(2, 0, 0)
    points.InsertNextPoint(3, 5, 0)
    points.InsertNextPoint(2, 10, 0)
    # points.InsertNextPoint(3, 5, 0)
    # points.InsertNextPoint(1.5, 7, 0)
    points.InsertNextPoint(3, 19, 0)

    # Fit a spline to the points
    spline = vtk.vtkParametricSpline()
    spline.SetPoints(points)
    functionsource = vtk.vtkParametricFunctionSource()
    functionsource.SetParametricFunction(spline)
    functionsource.SetUResolution(5 * points.GetNumberOfPoints())
    functionsource.Update()
    # polygon_spline = functionsource.GetOutput()
    return functionsource

def transform_spline(functionsource, distance):
    polygon_spline = functionsource.GetOutput()
    points = polygon_spline.GetPoints()
    # translate
    num_points = points.GetNumberOfPoints()
    point1 = points.GetPoint(0)
    point2 = points.GetPoint(num_points-1)
    # Create a transform
    transform = vtk.vtkTransform()
    dir_vector = [point2[i] - point1[i] for i in range(3)]
    vtk.vtkMath.Normalize(dir_vector)
    normal_vector = [-dir_vector[1], dir_vector[0], 0]
    distance_vector = [normal_vector[i]*distance for i in range(3)]
    transform.Translate(distance_vector)
    # Apply the transform to the line source
    transform_filter = vtk.vtkTransformPolyDataFilter()
    transform_filter.SetInputConnection(functionsource.GetOutputPort())
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    transform_polygon = transform_filter.GetOutput()
    return transform_polygon

def create_polygon():
    source = create_spline()
    transform_spline1 = transform_spline(source, 0.5)
    transform_spline2 = transform_spline(source, -0.5)
    # Combine vertices of both polydata
    vertices = vtk.vtkPoints()
    vertices = transform_spline1.GetPoints()
    vertices2 = transform_spline2.GetPoints()
    num_points_2 = vertices2.GetNumberOfPoints()
    for i in range(num_points_2-1, -1, -1):
        vertices.InsertNextPoint(vertices2.GetPoint(i))

    polygons = vtk.vtkCellArray()
    num_points = vertices.GetNumberOfPoints()
    for i in range(num_points):
        polygons.InsertNextCell(2)
        polygons.InsertCellPoint(i)
        polygons.InsertCellPoint((i+1) % num_points)

    # Create a polygon
    polygondata = vtk.vtkPolyData()
    polygondata.SetPoints(vertices)
    polygondata.SetLines(polygons)

    # Visualize the polygon
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polygondata)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor


renderer = vtk.vtkRenderer()
actor = create_polygon()
renderer.AddActor(actor)
axes = vtk.vtkAxesActor()
renderer.AddActor(axes)

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

# 创建 vtkRenderWindowInteractor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# 设置背景颜色
# renderer.SetBackground(1.0, 1.0, 1.0)

# 设置相机位置
# renderer.GetActiveCamera().Azimuth(30)
# renderer.GetActiveCamera().Elevation(30)

# 启动交互
renderWindow.Render()
renderWindowInteractor.Start()
