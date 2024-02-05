import vtkmodules.all as vtk

# Create a cylinder
cylinder = vtk.vtkCylinderSource()
cylinder.SetHeight(3.0)
cylinder.SetRadius(0.5)
cylinder.SetResolution(20)

# Create another cylinder
cylinder2 = vtk.vtkCylinderSource()
cylinder2.SetHeight(1.0)
cylinder2.SetRadius(0.2)
cylinder2.SetResolution(20)

# Combine the two cylinders
transform = vtk.vtkTransform()
transform.Translate(0.0, 0.0, 1.5)
transformFilter = vtk.vtkTransformPolyDataFilter()
transformFilter.SetInputConnection(cylinder2.GetOutputPort())
transformFilter.SetTransform(transform)
appendFilter = vtk.vtkAppendPolyData()
appendFilter.AddInputConnection(cylinder.GetOutputPort())
appendFilter.AddInputConnection(transformFilter.GetOutputPort())

# Visualize the result
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(appendFilter.GetOutputPort())
actor = vtk.vtkActor()
actor.SetMapper(mapper)
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindow.Render()
renderWindowInteractor.Start()