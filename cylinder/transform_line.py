import vtkmodules.all as vtk

# 创建两个点
point1 = [1.0, 0.0, 0.0]
point2 = [2.0, 1.0, 0.0]

# 创建vtkPoints对象并添加点
points = vtk.vtkPoints()
points.InsertNextPoint(point1)
points.InsertNextPoint(point2)

# 创建vtkCellArray对象并添加线段
line = vtk.vtkLine()
line.GetPointIds().SetId(0, 0)
line.GetPointIds().SetId(1, 1)

lines = vtk.vtkCellArray()
lines.InsertNextCell(line)

# 创建vtkPolyData对象并设置点和线
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetLines(lines)

# 创建vtkActor和vtkRenderer用于显示
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(polydata)

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1, 0, 0)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)

render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# 创建法向方向的平移变换
translation = vtk.vtkTransform()
# translation.Translate(0.0, 1.0, 0.0) 
dir_vector = [point2[i] - point1[i] for i in range(3)]
vtk.vtkMath.Normalize(dir_vector)
normal_vector = [-dir_vector[1], dir_vector[0], 0]
distance = 1
distance_vector = [normal_vector[i]*distance for i in range(3)]
translation.Translate(distance_vector)

# 创建vtkTransformPolyDataFilter进行变换
transform_filter = vtk.vtkTransformPolyDataFilter()
transform_filter.SetTransform(translation)
transform_filter.SetInputData(polydata)
trans_polydata = transform_filter.GetOutput()
print("\nTransformed Line Points:")
for i in range(trans_polydata.GetNumberOfPoints()):
    print(trans_polydata.GetPoint(i))

# 创建vtkPolyDataMapper和vtkActor用于显示平移后的线
transformed_mapper = vtk.vtkPolyDataMapper()
transformed_mapper.SetInputConnection(transform_filter.GetOutputPort())

transformed_actor = vtk.vtkActor()
transformed_actor.SetMapper(transformed_mapper)
transformed_actor.GetProperty().SetColor(0, 1, 0)

# 将平移后的线添加到渲染器
renderer.AddActor(transformed_actor)

axes = vtk.vtkAxesActor()
renderer.AddActor(axes)

# 设置相机和渲染窗口
# renderer.ResetCamera()
render_window.Render()
render_window_interactor.Start()
