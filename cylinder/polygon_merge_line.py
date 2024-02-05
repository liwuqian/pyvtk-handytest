import vtk
import numpy as np

# Create line segment 1
points1 = vtk.vtkPoints()
points1.InsertNextPoint(0.0, 0.0, 0.0)
points1.InsertNextPoint(1.0, 0.0, 0.0)

line1 = vtk.vtkCellArray()
line1.InsertNextCell(2)
line1.InsertCellPoint(0)
line1.InsertCellPoint(1)

polydata1 = vtk.vtkPolyData()
polydata1.SetPoints(points1)
polydata1.SetLines(line1)

# Create line segment 2
points2 = vtk.vtkPoints()
points2.InsertNextPoint(0.0, 1.0, 0.0)
points2.InsertNextPoint(1.0, 1.0, 0.0)

line2 = vtk.vtkCellArray()
line2.InsertNextCell(2)
line2.InsertCellPoint(0)
line2.InsertCellPoint(1)

polydata2 = vtk.vtkPolyData()
polydata2.SetPoints(points2)
polydata2.SetLines(line2)

# Combine vertices of both polydata
vertices = vtk.vtkPoints()
vertices = polydata1.GetPoints()
vertices2 = polydata2.GetPoints()
num_points_2 = vertices2.GetNumberOfPoints()
for i in range(num_points_2-1, -1, -1):
    vertices.InsertNextPoint(vertices2.GetPoint(i))

polygons = vtk.vtkCellArray()
num_points = vertices.GetNumberOfPoints()
for i in range(num_points):
    polygons.InsertNextCell(2)
    polygons.InsertCellPoint(i)
    polygons.InsertCellPoint((i+1) % num_points)

# Create a polygon
polygondata = vtk.vtkPolyData()
polygondata.SetPoints(vertices)
polygondata.SetLines(polygons)

# Visualize the polygon
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(polygondata)

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1,0,0)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)

render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

render_window.Render()
render_window_interactor.Start()
