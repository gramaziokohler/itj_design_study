import sys
path = "C:\Users\Wenqian\Documents\GitHub"
if path not in sys.path:
    sys.path.append(path)

import rhinoscriptsyntax as rs

import mola

guid = rs.GetObject()

def mesh_from_rhino_mesh(guid):
    mesh=mola.Mesh()
    vertices = rs.MeshVertices(guid)
    for v in vertices:
        mesh.vertices.append(mola.Vertex(v[0],v[1],v[2]))
    faceVerts = rs.MeshFaceVertices(guid)
    for face in faceVerts:
        if face[2]==face[3]:
            mesh.faces.append(mola.Face([mesh.vertices[face[0]],mesh.vertices[face[1]],mesh.vertices[face[2]]]))
        else:
            mesh.faces.append(mola.Face([mesh.vertices[face[0]],mesh.vertices[face[1]],mesh.vertices[face[2]],mesh.vertices[face[3]]]))
    return mesh


new_mesh = mesh_from_rhino_mesh(guid)

print(new_mesh)