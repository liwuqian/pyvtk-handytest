import vtkmodules.all as vtk
# for assembly, vtk picker can not pick actor
# Create global variables to store the selected actor and the original position
selected_actor = None
original_position = (0, 0, 0)

def create_cube():
    cube = vtk.vtkCubeSource()
    cube_mapper = vtk.vtkPolyDataMapper()
    cube_mapper.SetInputConnection(cube.GetOutputPort())
    cube_actor = vtk.vtkActor()
    cube_actor.SetMapper(cube_mapper)
    return cube_actor

def create_sphere():
    sphere = vtk.vtkSphereSource()
    sphere_mapper = vtk.vtkPolyDataMapper()
    sphere_mapper.SetInputConnection(sphere.GetOutputPort())
    sphere_actor = vtk.vtkActor()
    sphere_actor.SetMapper(sphere_mapper)
    return sphere_actor

def create_cone():
    cone = vtk.vtkConeSource()
    cone_mapper = vtk.vtkPolyDataMapper()
    cone_mapper.SetInputConnection(cone.GetOutputPort())
    cone_actor = vtk.vtkActor()
    cone_actor.SetMapper(cone_mapper)
    return cone_actor

def on_mouse_press_callback(obj, event):
    global selected_actor, original_position
    print("mouse press")
    click_pos = iren.GetEventPosition()
    picker = vtk.vtkPicker()
    iren.SetPicker(picker)
    picker.Pick(click_pos[0], click_pos[1], 0, ren)
    picked_actor = picker.GetActor()
    if picked_actor:
        print("Picked Actor: ")
        print(picked_actor)

    if picked_actor and picked_actor in assembly.GetParts():
        print("actor is picked")
        selected_actor = picked_actor
        original_position = selected_actor.GetPosition()
        selected_actor.GetProperty().SetColor(1, 0.5, 0)

def main(): 
    global ren_win, ren, iren, assembly

    ren = vtk.vtkRenderer()
    ren_win = vtk.vtkRenderWindow()
    ren_win.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(ren_win)

     # Create cube and sphere actors
    cube_actor = create_cube()
    sphere_actor = create_sphere()
    cone_actor = create_cone()

    # Set positions
    cube_actor.SetPosition(0, 0, 0)
    sphere_actor.SetPosition(2, 0, 0)
    cone_actor.SetPosition(0, 2, 0)

    # Create an assembly to group the cube and sphere
    assembly = vtk.vtkAssembly()
    assembly.AddPart(cube_actor)
    assembly.AddPart(sphere_actor)

    # Add the assembly to the renderer
    ren.AddActor(assembly)
    ren.AddActor(cone_actor)

    # Set background color
    ren.SetBackground(0.1, 0.1, 0.1)

    # Set up a callback for mouse press events
    iren.AddObserver("LeftButtonPressEvent", on_mouse_press_callback)

    # Start the rendering loop
    ren_win.Render()
    iren.Start()

if __name__ == "__main__":
    main()
