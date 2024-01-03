# import vtk
import vtkmodules.all as vtk

# 创建钉子圆柱体
nail_height = 50.0
nail_cylinder = vtk.vtkCylinderSource()
nail_cylinder.SetRadius(1)
nail_cylinder.SetHeight(nail_height)
nail_cylinder.SetResolution(100)
nail_cylinder.Update()

# 创建一个变换，将钉子原点设置到上边缘
transform_nail = vtk.vtkTransform()
transform_nail.Translate(0, -(nail_height)/2.0, 0)

transform_filter_nail = vtk.vtkTransformPolyDataFilter()
transform_filter_nail.SetTransform(transform_nail)
transform_filter_nail.SetInputConnection(nail_cylinder.GetOutputPort())
transform_filter_nail.Update()

# 创建一个 Mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(transform_filter_nail.GetOutputPort())

# 创建一个 Actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

actor.GetProperty().SetColor(0.5, 0.8, 0)
actor.GetProperty().SetOpacity(0.6)
actor.GetProperty().LightingOff()

# 创建一个渲染器
renderer = vtk.vtkRenderer()

# 创建一个渲染窗口
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

# 创建一个渲染窗口交互器
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# 将 Actor 添加到渲染器
renderer.AddActor(actor)

axes = vtk.vtkAxesActor()
axes.SetTotalLength(60, 80, 60)
renderer.AddActor(axes)

# 设置背景颜色
renderer.SetBackground(0.0, 0.0, 0.0)

# 重置相机并渲染场景
renderer.ResetCamera()
render_window.Render()

# 开始交互
render_window_interactor.Start()
