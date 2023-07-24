import vtkmodules.all as vtk

# Create a sphere geometry
sphere_source = vtk.vtkLineSource()
sphere_source.SetPoint1([0, 0, 0])
sphere_source.SetPoint2([1, 0, 0])
sphere_source.Update()

# Create a mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(sphere_source.GetOutput())

# Create an actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)
print('origin: ', actor.GetOrigin())
print('position: ', actor.GetPosition())
print(actor.GetMatrix())
actor.SetOrigin(0.5, 0, 0)
print("--- after set origin ---")
print('origin: ', actor.GetOrigin())
print('position: ', actor.GetPosition())
print(actor.GetMatrix())

# Create a renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)

# add axes
axes = vtk.vtkAxesActor()
renderer.AddActor(axes)

# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

# Create an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


if 1: 
    # Define the rotation angle and the rotation point in the world coordinate system
    angle = 45.0  # in degrees
    rotation_point = [0.5, 0, 0]

    # Translate the actor's position
    # translation = vtk.vtkTransform()
    # translation.Translate(rotation_point[0], rotation_point[1], rotation_point[2])
    # matrix = vtk.vtkMatrix4x4()
    # matrix.Identity()
    # matrix.SetElement(0,3, rotation_point[0])
    # matrix.SetElement(1,3, rotation_point[1])
    # matrix.SetElement(2,3, rotation_point[2])

    # actor.SetUserTransform(translation)
    
    # actor.RotateZ(45)
    # Rotate the actor around its local origin
    # rotation = vtk.vtkTransform()
    # rotation.RotateWXYZ(angle, 0, 0, 1)  # Rotate around Z-axis

    # actor.GetUserTransform().Concatenate(rotation)

    # # Translate the actor's position back to the original position
    # reverse_translation = vtk.vtkTransform()
    # reverse_translation.Translate(-rotation_point[0], -rotation_point[1], -rotation_point[2])

    # actor.GetUserTransform().Concatenate(reverse_translation)

    # # rotate again
    # tran2 = actor.GetUserTransform()
    # print(tran2)
    # tran2.Translate(rotation_point[0], rotation_point[1], rotation_point[2])
    # tran2.RotateWXYZ(angle, 0, 0, 1)
    # tran2.Translate(-rotation_point[0], -rotation_point[1], -rotation_point[2])

# Start the interactor
interactor.Initialize()
render_window.Render()
interactor.Start()
