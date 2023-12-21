import vtk

# Create a sample vtkPolyData object
points = vtk.vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(1, 1, 0)

polygons = vtk.vtkCellArray()
polygons.InsertNextCell(3, [0, 1, 2])

polyData = vtk.vtkPolyData()
polyData.SetPoints(points)
polyData.SetPolys(polygons)

# Extract points
num_points = polyData.GetNumberOfPoints()
vtk_points = polyData.GetPoints()

print("Points:")
for i in range(num_points):
    point = vtk_points.GetPoint(i)
    print(f"Point {i}: {point}")

# Extract polygons
num_cells = polyData.GetNumberOfCells()
vtk_cells = polyData.GetPolys()

print("\nPolygons:")
vtk_cells.InitTraversal()
for i in range(num_cells):
    cell_points = vtk.vtkIdList()
    vtk_cells.GetNextCell(cell_points)
    
    num_cell_points = cell_points.GetNumberOfIds()
    cell_point_ids = [cell_points.GetId(j) for j in range(num_cell_points)]
    
    print(f"Polygon {i}: {cell_point_ids}")
