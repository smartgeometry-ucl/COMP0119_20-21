
import numpy as np 
import os 
import pyrender


def scene_factory(render_list, return_nodes=False):
    
    scene = pyrender.Scene(ambient_light=0.5*np.array([1.0, 1.0, 1.0, 1.0]))
    
    nd_list=[]
    for m in render_list:
        nd=scene.add(m)
        nd_list.append(nd)
    
    if return_nodes:
        return scene, nd_list
    else:
        return scene

def run_gui(render_list, **kargs ):
    scene = scene_factory(render_list)
    # call GUI
    v=pyrender.Viewer(scene, use_raymond_lighting=True, **kargs)
    # free resources
    del v 
    return None



def save_pcd_obj(fp, data_n3):
    
    assert data_n3.shape[1] == 3, 'data is not a (n,3) array'
    
    with open(fp,'w') as fout:
        for i in range(data_n3.shape[0]):
            fout.write('v {:} {:} {:}\n'.format(data_n3[i,0],data_n3[i,1],data_n3[i,2]))
    
    

def load_pcd_obj(fp):

    #fp ='../temp/final_p2p_aligned_p.obj'

    assert os.path.exists(fp), fp 

    with open(fp,'r') as fin:
        content = fin.readlines()

    vex_content=[l[2:].strip() for l in content if len(l)>0 and l[:2]=='v ']
    vn_content=[l[2:].strip() for l in content if len(l)>0 and l[:2]=='vn']

    vertices=[]
    for l in vex_content:
        tks= [ float(t) for t in l.split(' ') ]
        vertices.append(tks)

    vnormal=[]
    for l in vn_content:
        tks= [ float(t) for t in l.split(' ') ]
        vnormal.append(tks)


    vertices=np.array(vertices)
    
    if len(vnormal)>0:
        vnormal=np.array(vnormal)
    else:
        vnormal=None 

    return vertices,vnormal


def create_edges( p0_pts,  p1_pts, p0_color=np.array([1.0,0.0,0.0]), p1_color=np.array([0.0,1.0,0.0]), line_color=np.array((0.0,0.0,1.0)) , no_vex=False ):
    # N,3
    if p1_pts.size<=0:
        return None 

    assert p0_pts.shape[1] == 3, p0_pts.shape
    assert p1_pts.shape[1] == 3, p1_pts.shape
    
    num = p0_pts.shape[0]

    line_pts=[]
    for i in range(num):
        line_pts.append(p0_pts[i])
        line_pts.append(p1_pts[i])

    line_pts = np.array(line_pts)

    plist=[]
    plist.append(
                pyrender.Primitive(
                    positions=line_pts, 
                    color_0=line_color,
                    mode=pyrender.constants.GLTF.LINES )  )
    if not no_vex:
	    plist.append( 
		        pyrender.Primitive(
		            positions=p0_pts, 
		            color_0=p0_color,
		            mode=pyrender.constants.GLTF.POINTS )  )
	    plist.append( 
		         pyrender.Primitive(
		             positions=p1_pts, 
		             color_0=p1_color,
		             mode=pyrender.constants.GLTF.POINTS )  )
    
    vecs_mesh = pyrender.Mesh(primitives=plist, is_visible=True) 
    return vecs_mesh 
