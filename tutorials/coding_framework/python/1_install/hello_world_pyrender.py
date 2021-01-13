import sys,os

RES_PATH = '../../../../resources'

if not os.path.exists(RES_PATH):
    print( 'cannot find /COMP0119_20-21/resources, please update RES_PATH')
    exit(1)
else:
    print('found resources')

import pyglet
pyglet.options['shadow_window'] = False

import pyrender
import numpy as np
import trimesh


if __name__ == '__main__':
    
    mesh_fp = os.path.join(RES_PATH,'torus.obj')
    assert os.path.exists(mesh_fp), 'cannot found:'+mesh_fp 
    
    t_mesh = trimesh.load(mesh_fp)     
    mesh = pyrender.Mesh.from_trimesh(t_mesh)
    scene = pyrender.Scene(ambient_light=0.5*np.array([1.0, 1.0, 1.0, 1.0]))
    
    scene.add(mesh)
    pyrender.Viewer(scene, use_raymond_lighting=True)
    
    print('done')
