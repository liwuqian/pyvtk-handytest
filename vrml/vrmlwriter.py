import vtkmodules.all as vtk

# Create a renderer, window, and interactor
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)

# Create a cone and add it to the renderer
cone = vtk.vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)
coneMapper = vtk.vtkPolyDataMapper()
coneMapper.SetInputConnection(cone.GetOutputPort())
coneActor = vtk.vtkActor()
coneActor.SetMapper(coneMapper)
renderer.AddActor(coneActor)

# Export the scene to VRML 2.0 format
exporter = vtk.vtkVRMLExporter()
exporter.SetInput(renderWindow)
exporter.SetFileName("output/polydata.wrl")
exporter.Write()

