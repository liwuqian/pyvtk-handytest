import vtkmodules.all as vtk
import math

def create_bent_tube():
    # Create points along the tube's path
    points = vtk.vtkPoints()
    num_points = 6
    for i in range(num_points):
        x = i * 0.1
        y = 0.1 * math.cos(6.28 * i / (num_points - 1))
        z = 0.1 * math.sin(6.28 * i / (num_points - 1))
        points.InsertNextPoint(x, y, z)

    # Create a polyline from the points
    line = vtk.vtkPolyLine()
    line.GetPointIds().SetNumberOfIds(num_points)
    for i in range(num_points):
        line.GetPointIds().SetId(i, i)

    # Create a cell array and add the polyline to it
    cells = vtk.vtkCellArray()
    cells.InsertNextCell(line)

    # Create a polydata to hold the points and cells
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(cells)

    # Create a tube filter to create the bent tube
    tube_filter = vtk.vtkTubeFilter()
    tube_filter.SetInputData(polydata)
    tube_filter.SetRadius(0.05)  # Set the radius of the tube
    tube_filter.SetNumberOfSides(20)  # Set the number of sides for the tube

    # Smooth the bent tube using vtkSmoothPolyDataFilter
    smoother = vtk.vtkSmoothPolyDataFilter()
    smoother.SetInputConnection(tube_filter.GetOutputPort())
    smoother.SetNumberOfIterations(100)  # Adjust the number of iterations as needed
    smoother.SetRelaxationFactor(0.1)  # Adjust the relaxation factor as needed
    smoother.FeatureEdgeSmoothingOff()
    smoother.BoundarySmoothingOn()
    smoother.Update()

    # Create a mapper and actor for visualization
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(smoother.GetOutputPort())
    mapper.SetInputConnection(tube_filter.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor


def create_bent_tube2():
    # Create points along the tube's path
    points = vtk.vtkPoints()
    num_points = 6
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(2, 0, 0)
    points.InsertNextPoint(3, 1, 0)
    points.InsertNextPoint(4, 1, 0)
    points.InsertNextPoint(5, 0, 0)
    points.InsertNextPoint(6, 0, 0)

    # Fit a spile to the points
    spline = vtk.vtkParametricSpline()
    spline.SetPoints(points)
    functionsource = vtk.vtkParametricFunctionSource()
    functionsource.SetParametricFunction(spline)
    functionsource.SetUResolution(10 * points.GetNumberOfPoints())
    functionsource.Update()

    # Interpolate the scalars
    interpolatedRadius = vtk.vtkTupleInterpolator()
    interpolatedRadius.SetInterpolationTypeToLinear()
    interpolatedRadius.SetNumberOfComponents(1)
    interpolatedRadius.AddTuple(0, [0.2])
    interpolatedRadius.AddTuple(1, [0.2])
    interpolatedRadius.AddTuple(2, [0.15])
    interpolatedRadius.AddTuple(3, [0.15])
    interpolatedRadius.AddTuple(4, [0.1])
    interpolatedRadius.AddTuple(5, [0.1])

    # generate the radius scalars
    tubeRadius = vtk.vtkDoubleArray()
    num = functionsource.GetOutput().GetNumberOfPoints()
    tubeRadius.SetNumberOfTuples(num)
    tubeRadius.SetName("TubeRadius")

    tmin = interpolatedRadius.GetMinimumT()
    tmax = interpolatedRadius.GetMaximumT()
    r = [1.0]
    for i in range(num):
        t = (tmax - tmin) / (num -1) * i + tmin
        interpolatedRadius.InterpolateTuple(t, r)
        print(r)
        tubeRadius.SetTuple1(i, r[0])

    # add the scalars into the polydata
    tubePolydata = vtk.vtkPolyData()
    tubePolydata = functionsource.GetOutput()
    # determine if use the scalar data
    if (0):
        tubePolydata.GetPointData().AddArray(tubeRadius)
        tubePolydata.GetPointData().SetActiveScalars("TubeRadius")

    # Create a tube filter to create the bent tube
    tube_filter = vtk.vtkTubeFilter()
    tube_filter.SetInputData(tubePolydata)
    tube_filter.SetRadius(0.1)  # Set the radius of the tube
    tube_filter.SetNumberOfSides(50)  # Set the number of sides for the tube
    tube_filter.SetVaryRadiusToVaryRadiusByAbsoluteScalar()

    # Create a capped cylinder source for the tube's ends
    tube_end_caps = vtk.vtkCylinderSource()
    tube_end_caps.SetRadius(0.1)  # Set the radius to match the tube
    tube_end_caps.SetCenter(0, 0, 0)  # Set the center of the caps (tube's starting point)
    tube_end_caps.SetHeight(0.001)  # Set the height of the caps (small thickness)
    tube_end_caps.SetResolution(20)  # Set the resolution of the caps

    # Combine the tube and its end caps using vtkAppendPolyData
    append_filter = vtk.vtkAppendPolyData()
    append_filter.AddInputConnection(tube_filter.GetOutputPort())
    append_filter.AddInputConnection(tube_end_caps.GetOutputPort())
    append_filter.Update()

    # Create a mapper and actor for visualization
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(append_filter.GetOutputPort())  # Use the smoothed polydata
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    # taking effect wihle not used scalar data
    actor.GetProperty().SetColor(0, 1, 0)

    return actor


def main():
    # Create a renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # Add the bent tube to the renderer
    actor = create_bent_tube2()
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
