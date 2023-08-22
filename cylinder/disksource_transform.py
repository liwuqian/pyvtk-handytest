import vtkmodules.all as vtk

def set_z_direction_of_matrix(m, v):
    # Normalize vector v to unit length
    normalized_v = v
    vtk.vtkMath.Normalize(normalized_v)
    print(normalized_v)

    # Find two perpendicular vectors in the plane formed by x and y directions
    x_axis = [1.0, 0.0, 0.0]  # Assuming x-direction of the matrix is [1, 0, 0]
    y_axis = [0.0, 1.0, 0.0]  # Assuming y-direction of the matrix is [0, 1, 0]

    # Compute the cross product to find the perpendicular vector in the plane
    a = [0.0, 0.0, 0.0]
    vtk.vtkMath.Cross(normalized_v, x_axis, a)
    if vtk.vtkMath.Norm(a) == 0:
        vtk.vtkMath.Cross(normalized_v, y_axis, a)

    # Normalize the perpendicular vector 'a'
    vtk.vtkMath.Normalize(a)

    # Compute the second perpendicular vector
    b = [0.0, 0.0, 0.0]
    vtk.vtkMath.Cross(normalized_v, a, b)

    # Set the first three columns of the matrix
    for i in range(3):
        m.SetElement(i, 0, a[i])
        m.SetElement(i, 1, b[i])
        m.SetElement(i, 2, normalized_v[i])

    return m


def getActorCircle(radius_inner=100, radius_outer=99, color=(1,0,0)):
    """"""
    # create source
    source = vtk.vtkDiskSource()
    source.SetInnerRadius(radius_inner)
    source.SetOuterRadius(radius_outer)
    source.SetRadialResolution(100)
    source.SetCircumferentialResolution(100)

    # Transformer
    transform = vtk.vtkTransform()
    
    # Example usage:
    v = [1.0, .0, .0]  # Replace this with your desired vector
    # Create a vtkMatrix4x4 transformation matrix
    m = vtk.vtkMatrix4x4()
    m.Identity()  # Initialize as an identity matrix
    resulting_matrix = set_z_direction_of_matrix(m, v)
    print(resulting_matrix)
    transform.SetMatrix(resulting_matrix)
    # transform.RotateWXYZ(90, 1, 0, 0)
    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetTransform(transform)
    transformFilter.SetInputConnection(source.GetOutputPort())
    transformFilter.Update()

    # mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transformFilter.GetOutputPort())

    # actor
    actor = vtk.vtkActor()
    actor.GetProperty().SetColor(color)
    actor.SetMapper(mapper)

    return actor


def main():
    # Create a renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    actor = getActorCircle(1, 0)
    renderer.AddActor(actor)

    # add axes
    axes = vtk.vtkAxesActor()
    renderer.AddActor(axes)

    # Set the background color and start the interaction
    renderer.SetBackground(1, 1, 1)  # White background
    render_window.SetSize(800, 600)
    render_window.Render()
    interactor.Start()

if __name__ == "__main__":
    main()
