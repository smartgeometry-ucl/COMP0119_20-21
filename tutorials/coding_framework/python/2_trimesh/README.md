
# Trimesh Quickstart
version 3.5.7 - 3.9.1

## Load a mesh

Functions:  
+ [trimesh.load(...)](https://trimsh.org/trimesh.html?highlight=load#trimesh.load)
+ [trimesh.load_mesh(...)](https://trimsh.org/trimesh.html?highlight=load#trimesh.load_mesh)

Remember to set the argument <span style="color:red">process=False</span> or trimesh might change the mesh.

## Create a mesh

You can create a mesh object from a list of *vertices* and *faces*.

+ [trimesh.Trimesh(....)](https://trimsh.org/trimesh.html#trimesh.Trimesh)

It is also possible to create a point cloud object from a list of *points*.

+ [trimesh.PointCloud(....)](https://trimsh.org/trimesh.html#trimesh.PointCloud)

Remember to set the argument <span style="color:red">process=False</span> or trimesh might change the mesh.

## Trimesh Object
After you loaded a mesh, you will get a [Trimesh]( https://trimsh.org/trimesh.html#trimesh.Trimesh ) object.  
Some useful attributes are listed below:  

## Attributes

### Vertices
| attribute     | type | description   |
|:------------- |:-------------|:-------------|  
| vertices | (n, 3) float | The vertices of the mesh. | 
| vertex_normals | (n, 3) float | The vertex normals of the mesh. |
| vertex_faces | (n,m) int | Each row contains the face indices that correspond to the given vertex. m == max number of faces for a single vertex |
| vertex_neighbors | (len(self.vertices), ) int |  The vertex neighbors of each vertex of the mesh. |

### Edges
| attribute     | type | description   |
|:------------- |:-------------|:-------------|  
| edges | (n, ) int  | Edges of the mesh (derived from faces). |
| edges_face | (n, ) int | Which face does each edge belong to.|

### Faces
| attribute     | type | description   |
|:------------- |:-------------|:-------------|  
| faces | (n, 3) int | The faces of the mesh. |
| faces_sparse | scipy.sparse.coo_matrix  | A sparse matrix representation of the faces. |
| face_normals | (n, 3) np.float64 | Return the unit normal vector for each face. |
| face_adjacency | (k, 2) int | Pairs of faces which share an edge |
| face_adjacency_angles| (k, ) | Angle between adjacent faces Each value corresponds with self.face_adjacency |
| face_adjacency_edges | (k, 2) int | Returns the edges that are shared by the adjacent faces. | 
| face_angles | (n, 3) | Returns the angle at each vertex of a face. |
| area_faces  | (n, ) float | The area of each face in the mesh. | 

### Others
| attribute     | type | description   |
|:------------- |:-------------|:-------------|  
| visual | [object]( https://trimsh.org/trimesh.html#trimesh.Trimesh.visual ) | Get the stored visuals for the current mesh.|
| is_watertight | bool | Check if a mesh is watertight by making sure every edge is included in two faces. |
| is_winding_consistent | bool | Does the mesh have consistent winding or not. |
| euler_number | int | Return the Euler characteristic (a topological invariant) for the mesh |

## Frequently used Methods

Trimesh.[apply_transform(matrix)](  https://trimsh.org/trimesh.html#trimesh.Trimesh.apply_transform  )  
Trimesh.[copy()](  https://trimsh.org/trimesh.html#trimesh.Trimesh.copy  )  
Trimesh.[show()](  https://trimsh.org/trimesh.html#trimesh.Trimesh.show  )  


