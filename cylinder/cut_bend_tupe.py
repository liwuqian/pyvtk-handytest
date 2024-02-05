# Generate a 2d rod wireframe using cutter to cut the tube
import vtkmodules.all as vtk
import math

def create_spline():
    # Create points along the rod's path
    points = vtk.vtkPoints()
    num_points = 6
    points.InsertNextPoint(2, 0, 0)
    points.InsertNextPoint(3, 5, 0)
    points.InsertNextPoint(2, 10, 0)
    # points.InsertNextPoint(3, 5, 0)
    # points.InsertNextPoint(1.5, 7, 0)
    points.InsertNextPoint(3, 19, 0)

    # Fit a spline to the points
    spline = vtk.vtkParametricSpline()
    spline.SetPoints(points)
    functionsource = vtk.vtkParametricFunctionSource()
    functionsource.SetParametricFunction(spline)
    functionsource.SetUResolution(5 * points.GetNumberOfPoints())
    functionsource.Update()
    # polygon_spline = functionsource.GetOutput()
    return functionsource

def create_bent_tube_cutter():
    functionsource = create_spline()
    tubePolydata = functionsource.GetOutput()

    # Create a tube filter to create the bent tube
    radius = 0.5
    tube_filter = vtk.vtkTubeFilter()
    tube_filter.SetInputData(tubePolydata)
    tube_filter.SetRadius(radius)  # Set the radius of the tube
    tube_filter.SetNumberOfSides(50)  # Set the number of sides for the tube
    tube_filter.CappingOn()
    tube_filter.SetVaryRadiusToVaryRadiusByAbsoluteScalar()

    # Create a cutting plane
    plane = vtk.vtkPlane()
    plane.SetOrigin(2.5, 10.0, 0.0)
    plane.SetNormal(0.0, 0.0, 1.0)

    # Create a cutter and set its input and the cutting plane
    cutter = vtk.vtkCutter()
    cutter.SetInputConnection(tube_filter.GetOutputPort())
    cutter.SetCutFunction(plane)

    # Create a mapper and actor for the cutter
    cutter_mapper = vtk.vtkPolyDataMapper()
    cutter_mapper.SetInputConnection(cutter.GetOutputPort())

    cutter_actor = vtk.vtkActor()
    cutter_actor.SetMapper(cutter_mapper)

    # Set the line thickness
    cutter_actor.GetProperty().SetLineWidth(5.0)  # Adjust the thickness as needed
    cutter_actor.GetProperty().LightingOff()

    # taking effect wihle not used scalar data
    cutter_actor.GetProperty().SetColor(0, 1, 0)

    return cutter_actor


def main():
    # Create a renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # Add the bent tube to the renderer
    actor = create_bent_tube_cutter()
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
