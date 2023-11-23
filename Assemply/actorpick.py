import vtkmodules.all as vtk

# Create a rendering window and renderer
ren = vtk.vtkRenderer()
ren_win = vtk.vtkRenderWindow()
ren_win.AddRenderer(ren)

# Create a render window interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(ren_win)

# Create a cube actor
cube = vtk.vtkCubeSource()
cube_mapper = vtk.vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())
cube_actor = vtk.vtkActor()
cube_actor.SetMapper(cube_mapper)

# Add the cube actor to the renderer
ren.AddActor(cube_actor)

# Set up a picker
picker = vtk.vtkPicker()
iren.SetPicker(picker)

def on_mouse_click(obj, event):
    click_pos = iren.GetEventPosition()
    picker.Pick(click_pos[0], click_pos[1], 0, ren)
    picked_actor = picker.GetActor()

    if picked_actor:
        print("Picked Actor:", picked_actor)

# Set up a mouse click event
iren.AddObserver("LeftButtonPressEvent", on_mouse_click)

# Set background color
ren.SetBackground(0.1, 0.1, 0.1)

# Start the rendering loop
ren_win.Render()
iren.Start()
