from fenics import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri


mesh = RectangleMesh(Point(0,0), Point(1, 2), 64, 64, "right/left")
V = FunctionSpace(mesh, 'P', 1)

u_e = Expression('-sin(5*pi*x[0])*sin(3*pi*x[1])/(34*pi*pi)+sin(pi*x[0])*sinh(pi*(2-x[1]))/sinh(2*pi)+sin(3*pi*x[0])*sinh(3*pi*x[1])/sinh(6*pi)+sin(2*pi*x[1])*sinh(2*pi*(1-x[0]))/sinh(2*pi)+sin(pi*x[1])*sinh(pi*x[0])/sinh(pi)',degree=2)


u_L = Expression('sin(pi*x[0])', degree=2)
def boundary_L(x, on_boundary):
    tol = 1E-14
    return on_boundary and near(x[1], 0, tol)
bc_L = DirichletBC(V, u_L, boundary_L)

u_R = Expression('sin(3*pi*x[0])', degree=2)
def boundary_R(x, on_boundary):
    tol = 1E-14
    return on_boundary and near(x[1], 2, tol)
bc_R = DirichletBC(V, u_R, boundary_R)

u_D = Expression('sin(2*pi*x[1])', degree=2)
def boundary_D(x, on_boundary):
    tol = 1E-14
    return on_boundary and near(x[0], 0, tol)
bc_D = DirichletBC(V, u_D, boundary_D)

u_U = Expression('sin(pi*x[1])', degree=2)
def boundary_U(x, on_boundary):
    tol = 1E-14
    return on_boundary and near(x[0], 1, tol)
bc_U = DirichletBC(V, u_U, boundary_U)

bc = [bc_L, bc_R, bc_D, bc_U]

u = TrialFunction(V)
v = TestFunction(V)
f = Expression('-sin(5*pi*x[0])*sin(3*pi*x[1])',degree=2)
a = dot(grad(u), grad(v))*dx
L = f*v*dx

u = Function(V)
solve(a == L, u, bc)

vtkfile = File('my_poisson/solution.pvd')
vtkfile << u

error_L2 = errornorm(u_e, u, 'L2')

vertex_values_u_e = u_e.compute_vertex_values(mesh)
vertex_values_u = u.compute_vertex_values(mesh)
error_max = np.max(np.abs(vertex_values_u_e - vertex_values_u))

print('error_L2 =', error_L2)
print('error_max =', error_max)

n = mesh.num_vertices()
d = mesh.geometry().dim()
mesh_coordinates = mesh.coordinates().reshape((n, d))
triangles = np.asarray([cell.entities(0) for cell in cells(mesh)])
triangulation = tri.Triangulation(mesh_coordinates[:, 0], mesh_coordinates[:, 1], triangles)
plt.figure()
zfaces = np.asarray([u(cell.midpoint()) for cell in cells(mesh)])
zfaces2 = np.asarray([u_e(cell.midpoint()) for cell in cells(mesh)])
plt.tripcolor(triangulation, facecolors=zfaces, edgecolors='k')
plt.colorbar()
plt.savefig('u_fe.png')

