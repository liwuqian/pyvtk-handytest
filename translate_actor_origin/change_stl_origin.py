import vtkmodules.all as vtk

def change_origin(new_pos, polydata):
    # Update the points of the polydata
    points = polydata.GetPoints()
    numPoints = polydata.GetNumberOfPoints()
    for i in range(numPoints):
        point = points.GetPoint(i)
        newPoint = [
            # point[0] + translation[0],
            # point[1] + translation[1],
            # point[2] + translation[2]
            point[0] - newOrigin[0],
            point[1] - newOrigin[1],
            point[2] - newOrigin[2]
        ]
        points.SetPoint(i, newPoint)

    # Update the polydata
    polydata.Modified()

# Read the STL file
reader = vtk.vtkSTLReader()
reader.SetFileName("data/37125550-01.stl")
reader.Update()


# Visualize the modified STL actor
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

mapper = vtk.vtkPolyDataMapper()
# mapper.SetInputData(polydata)
mapper.SetInputData(reader.GetOutput())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer.AddActor(actor)

# add axes
axes = vtk.vtkAxesActor()
axes.SetTotalLength(70,70,70)
renderer.AddActor(axes)

newOrigin = [0, -50, 0]
transform = vtk.vtkTransform()
transform.RotateWXYZ(45, 0, 0, 1)

transform.Translate(0, 00, 0)
actor.SetUserTransform(transform)
# print(transform)
print("after transform: \n", actor.GetMatrix())

# calculate the world pos of new origin, for translate here after changing origin
# the new origin is in the model frame
# or backup transform origin
backpos = transform.TransformDoublePoint(0, 0, 0)
print('backpos: ', backpos)

# Get the polydata
polydata = reader.GetOutput()
change_origin(newOrigin, polydata)
# print("after change origin: \n", actor.GetMatrix())

# translate to previous pos
# back to previous position
# calculate the world pos of new origin, for translate here after changing origin
# the new origin is in the model frame
# backpos = transform.TransformDoublePoint(newOrigin[0], newOrigin[1], newOrigin[2])
mat4 = vtk.vtkMatrix4x4()
mat4.SetElement(0,3,newOrigin[0])
mat4.SetElement(1,3,newOrigin[1])
mat4.SetElement(2,3,newOrigin[2])
# transform.Concatenate(mat4)
# Translate equal to right multiply matrix with new origin
transform.Translate(newOrigin)
# transform.GetMatrix().SetElement(0,3,newOrigin[0])
# transform.GetMatrix().SetElement(1,3,newOrigin[1])
# transform.GetMatrix().SetElement(2,3,newOrigin[2])

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

renderer.ResetCamera()
renderWindow.Render()
renderWindowInteractor.Start()
