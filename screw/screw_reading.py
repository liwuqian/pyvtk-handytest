import vtkmodules.all as vtk

# Create a renderer
renderer = vtk.vtkRenderer()

# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

# Create a render window interactor
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Create a STL reader
stl_reader = vtk.vtkSTLReader()
stl_reader.SetFileName("data/screw_general.stl")

# Create a mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(stl_reader.GetOutputPort())

# Create an actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0.5, 0.8, 0)
actor.GetProperty().SetOpacity(0.6)
actor.GetProperty().LightingOff()

# Add the actor to the renderer
renderer.AddActor(actor)

axes = vtk.vtkAxesActor()
axes.SetTotalLength(60, 80, 60)
renderer.AddActor(axes)

# Set background color
renderer.SetBackground(0.1, 0.1, 0.1)

# Reset the camera to show the object
renderer.ResetCamera()

# Start rendering
render_window.Render()

# Start the interaction
render_window_interactor.Start()
