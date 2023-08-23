# import vtk
import vtkmodules.all as vtk

# 创建钉帽圆柱体
cap_height = 6.0
cap_cylinder = vtk.vtkCylinderSource()
cap_cylinder.SetRadius(7)
cap_cylinder.SetHeight(cap_height)
cap_cylinder.SetResolution(50)
cap_cylinder.Update()

# 创建钉子圆柱体
nail_height = 50.0
nail_cylinder = vtk.vtkCylinderSource()
nail_cylinder.SetRadius(4.5)
nail_cylinder.SetHeight(nail_height)
nail_cylinder.SetResolution(50)
nail_cylinder.Update()

# 创建一个变换，将钉帽移到钉子顶部
transform = vtk.vtkTransform()
transform.Translate(0, (cap_height + nail_height)/2.0, 0)  # 移动到钉子顶部

transform_filter = vtk.vtkTransformPolyDataFilter()
transform_filter.SetTransform(transform)
transform_filter.SetInputConnection(cap_cylinder.GetOutputPort())
transform_filter.Update()

# 将钉帽和钉子合并
append_filter = vtk.vtkAppendPolyData()
append_filter.AddInputConnection(transform_filter.GetOutputPort())
append_filter.AddInputConnection(nail_cylinder.GetOutputPort())
append_filter.Update()

# 创建一个 Mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(append_filter.GetOutputPort())

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
renderer.AddActor(axes)

# 设置背景颜色
renderer.SetBackground(0.0, 0.0, 0.0)

# 重置相机并渲染场景
renderer.ResetCamera()
render_window.Render()

# 开始交互
render_window_interactor.Start()
