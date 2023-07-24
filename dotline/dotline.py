import vtk

# Create a renderer and a render window
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

# Create a interactor and set the render window
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Create a line source and set its properties
line_source = vtk.vtkLineSource()
line_source.SetPoint1(0, 0, 0)
line_source.SetPoint2(1, 1, 0)
line_source.SetResolution(10)

# Create a mapper and set the line source as input
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(line_source.GetOutputPort())

# Create an actor and set the mapper as input
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Set the actor's properties
actor.GetProperty().SetColor(1, 0, 0)
actor.GetProperty().SetLineWidth(2)
actor.GetProperty().SetLineStipplePattern(0xf0f0)
actor.GetProperty().SetLineStippleRepeatFactor(1)

# Add the actor to the renderer
renderer.AddActor(actor)

# Set the background color and size of the render window
renderer.SetBackground(1, 1, 1)
render_window.SetSize(400, 400)

# Start the interactor and render the scene
interactor.Initialize()
render_window.Render()
interactor.Start()

