import sys,os

RES_PATH = '../../../../resources'

if not os.path.exists(RES_PATH):
    print( 'cannot find /COMP0119_20-21/resources, please update RES_PATH')
    exit(1)
else:
    print('found resources')
    
import open3d as o3d
import numpy as np 
import trimesh


if __name__ == '__main__':
    
    mesh_fp = os.path.join(RES_PATH,'torus.obj')
    assert os.path.exists(mesh_fp), 'cannot found:'+mesh_fp 
    
    
    mesh1 = o3d.io.read_triangle_mesh(mesh_fp)
    
    o3d.visualization.draw_geometries([mesh1])
    
    #-------------------------------------
    
    t_mesh = trimesh.load(mesh_fp)
    mesh2 = o3d.geometry.TriangleMesh()
    
    mesh2.vertices=o3d.utility.Vector3dVector(t_mesh.vertices)
    mesh2.triangles=o3d.utility.Vector3iVector(t_mesh.faces)
    
    o3d.visualization.draw_geometries([mesh2])
    
    print('done')
