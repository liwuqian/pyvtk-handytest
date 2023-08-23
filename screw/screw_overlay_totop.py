# using coincident pology technique to render actor to top view
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

units = -66000
# Create a mapper
mapper_1 = vtk.vtkPolyDataMapper()
mapper_1.SetInputConnection(stl_reader.GetOutputPort())
mapper_1.SetResolveCoincidentTopologyToPolygonOffset()
mapper_1.SetRelativeCoincidentTopologyLineOffsetParameters(0, units)
mapper_1.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, units)
mapper_1.SetRelativeCoincidentTopologyPointOffsetParameter(units)
# disble coincident topoly
mapper_1.SetResolveCoincidentTopologyToOff() 

mapper_2 = vtk.vtkPolyDataMapper()
mapper_2.SetInputConnection(stl_reader.GetOutputPort())
mapper_2.SetResolveCoincidentTopologyToPolygonOffset()
mapper_2.SetRelativeCoincidentTopologyLineOffsetParameters(0, units)
mapper_2.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, units)
mapper_2.SetRelativeCoincidentTopologyPointOffsetParameter(units)
# mapper_2.SetResolveCoincidentTopologyToOff()

# Create an actor 1
actor_1 = vtk.vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetColor(0.5, 0.8, 0)
# actor_1.GetProperty().SetOpacity(0.9)
actor_1.GetProperty().LightingOff()
# actor_1.RotateZ(30)
actor_1.SetPosition(1,5,0)

actor_2 = vtk.vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetColor(0.0, 0.8, 0.5)
# actor_2.GetProperty().SetOpacity(0.9)
actor_2.GetProperty().LightingOff()

cone = vtk.vtkConeSource()
cone.SetRadius(10)
cone.SetHeight(20)
cone.Update()
cone_mapper = vtk.vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())
cone_actor = vtk.vtkActor()
cone_actor.SetMapper(cone_mapper)

# Add the actor to the renderer
# renderer.AddActor(actor_2)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
# renderer.AddActor(cone_actor)


axes = vtk.vtkAxesActor()
axes.SetTotalLength(60, 80, 60)
# renderer.AddActor(axes)

# Set background color
renderer.SetBackground(0.1, 0.1, 0.1)

# Reset the camera to show the object
renderer.ResetCamera()

# Start rendering
render_window.Render()

# Start the interaction
render_window_interactor.Start()
