import vtk

def generate_closed_polygon(points):
    # 创建VTK场景
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    # 创建多边形数据
    poly_data = vtk.vtkPolyData()
    points_list = vtk.vtkPoints()

    for point in points:
        points_list.InsertNextPoint(point[0], point[1], 0)

    # 定义多边形的连接信息
    polygon = vtk.vtkCellArray()
    for i in range(len(points)):
        polygon.InsertNextCell(2)
        polygon.InsertCellPoint(i)
        polygon.InsertCellPoint((i + 1) % len(points))

    poly_data.SetPoints(points_list)
    poly_data.SetLines(polygon)

    # 创建线框表示
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(poly_data)

    # 创建演员
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # 将演员添加到场景
    renderer.AddActor(actor)

    # 设置渲染窗口属性
    render_window.SetSize(600, 600)
    renderer.SetBackground(0.2, 0.3, 0.4)

    # 创建交互器
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # 开启交互
    render_window.Render()
    interactor.Start()

# 输入点的坐标列表（示例）
points = [(0, 0), (1, 0), (1, 1), (0.5, 1.5), (0, 1)]

generate_closed_polygon(points)
