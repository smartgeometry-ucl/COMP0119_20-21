###Adapted from https://github.com/carlosrojas/halfedge_mesh/tree/master for educational purposes. Many thanks to Carlos Rojas.



import sys
EPSILON = 1e-6
import math

class HalfedgeMesh:

    def __init__(self, filename=None, vertices=[], halfedges=[], facets=[]):
        """Make an empty halfedge mesh.

           filename   - a string that holds the directory location and name of
               the mesh
            vertices  - a list of Vertex types
            halfedges - a list of HalfEdge types
            facets    - a list of Facet types
        """

        self.vertices = vertices
        self.halfedges = halfedges
        self.facets = facets
        self.filename = filename
        self.edges = None

        if filename:
            self.vertices, self.halfedges, self.facets, self.edges = self.read_file(filename)

    def __eq__(self, other):
        return (isinstance(other, type(self)) and 
            (self.vertices, self.halfedges, self.facets) ==
            (other.vertices, other.halfedges, other.facets))

    def __hash__(self):
        return (hash(str(self.vertices)) ^ hash(str(self.halfedges)) ^ hash(str(self.facets)) ^ 
            hash((str(self.vertices), str(self.halfedges), str(self.facets))))
    
    def flip(self):
        for vertex in self.vertices:
            vertex.x = -1*vertex.x

    def read_file(self, filename):
        """Determine the type of file and use the appropriate parser.

        Returns a HalfedgeMesh
        """
        
        with open(filename, 'r') as file:

            first_line = file.readline().strip().upper()

            if first_line != "OFF":
                raise ValueError("Filetype: " + first_line + " not accepted")

            # TODO: build OBJ, PLY parsers
            parser_dispatcher = {"OFF": self.parse_off}
                                      
            return parser_dispatcher[first_line](file)

        
    def read_off_vertices(self, file_object, number_vertices):
        """Read each line of the file_object and return a list of Vertex types.
        The list will be as [V1, V2, ..., Vn] for n vertices

        Return a list of vertices.
        """
        vertices = []

        # Read all the vertices in
        for index in range(number_vertices):
            line = file_object.readline().split()

            try:
                # convert strings to floats
                line = [float(element) for element in line]
            except ValueError as e:
                raise ValueError("vertices " + str(e))

            vertices.append(Vertex(line[0], line[1], line[2], index))

        return vertices

    def parse_build_halfedge_off(self, file_object, number_facets, vertices):
        """Link to the code:
        http://stackoverflow.com/questions/15365471/initializing-half-edge-
        data-structure-from-vertices

        Pseudo code:
        map< pair<unsigned int, unsigned int>, HalfEdge* > Edges;

        for each face F
        {
            for each edge (u,v) of F
            {
                Edges[ pair(u,v) ] = new HalfEdge();
                Edges[ pair(u,v) ]->face = F;
            }
            for each edge (u,v) of F
            {
                set Edges[ pair(u,v) ]->nextHalfEdge to next half-edge in F
                if ( Edges.find( pair(v,u) ) != Edges.end() )
                {
                    Edges[ pair(u,v) ]->oppositeHalfEdge = Edges[ pair(v,u) ];
                    Edges[ pair(v,u) ]->oppositeHalfEdge = Edges[ pair(u,v) ];
            }
        }

        """
        Edges = {}
        facets = []
        halfedge_count = 0
        

        # For each facet
        for index in range(number_facets):
            line = file_object.readline().split()

            # convert strings to ints
            line = [ int(element) for element in line ]

            
            
            n = line[0]
            facet = Facet(-1, -1, -1, index)
            facets.append(facet)

            # create pairing of vertices for example if the vertices are
            # verts = [1,2,3] then zip(verts, verts[1:]) = [(1,2),(2,3)]
            # note: we skip line[0] because it represents the number of vertices
            # in the facet.
            all_facet_edges = list (zip(line[1:], line[2:]) )
            
            all_facet_edges.append((line[n], line[1]))
            
            #print(all_facet_edges)
            #print(all_facet_edges[0][2::-1])

            # For every halfedge around the facet
            for i in range(n):
                Edges[all_facet_edges[i]] = Halfedge()
                Edges[all_facet_edges[i]].facet = facet
                Edges[all_facet_edges[i]].vertex = vertices[
                    all_facet_edges[i][0]]###
                vertices[all_facet_edges[i][0]].halfedge = Edges[all_facet_edges[i]]###
                halfedge_count +=1

            facet.halfedge = Edges[all_facet_edges[0]]
            
            
            for i in range(n):
                Edges[all_facet_edges[i]].next = Edges[
                    all_facet_edges[(i + 1) % n]]
                Edges[all_facet_edges[i]].prev = Edges[
                    all_facet_edges[(i - 1) % n]]

                # reverse edge ordering of vertex, e.g. (1,2)->(2,1)
                if all_facet_edges[i][2::-1] in Edges:
                    Edges[all_facet_edges[i]].opposite = \
                        Edges[all_facet_edges[i][2::-1]]

                    Edges[all_facet_edges[i][2::-1]].opposite = \
                        Edges[all_facet_edges[i]]
                        
            

        return facets, Edges

    def parse_off(self, file_object):
        """Parses OFF files

        Returns a HalfedgeMesh
        """
        facets, halfedges, vertices = [], [], []

                
        
        line = file_object.readline()
        number_vertices = int ( line.split()[0] )
        vertices = self.read_off_vertices(file_object, number_vertices)

        number_facets = int (  line.split()[1] )
        facets, Edges = self.parse_build_halfedge_off(file_object,
                                                      number_facets, vertices)
        
        i = 0
        for key, value in Edges.items():
            value.index = i
            halfedges.append(value)
            i += 1
            
        
        return vertices, halfedges, facets, Edges
    
    def write_off(self, filename):
        with open(filename, 'w') as file:
            file.write('OFF\n')
            file.write(str(len(self.vertices))+' '+str(len(self.facets))+' 0\n')
            for vertex in self.vertices:
                xyz = vertex.get_vertex()
                file.write(str(xyz[0])+' '+str(xyz[1])+' '+str(xyz[2])+'\n')
                
            for facet in self.facets:
                facet_vertices = facet.get_vertices()
                string = str(len(facet_vertices))
                for vertex in facet_vertices:
                    string = string + ' ' + str(vertex.index)
                string = string + '\n'
                file.write(string)
    
    def write_obj(self, filename):
        with open(filename, 'w') as file:
            for vertex in self.vertices:
                xyz = vertex.get_vertex()
                file.write('v '+ str(xyz[0])+' '+str(xyz[1])+' '+str(xyz[2])+'\n')
                
            for facet in self.facets:
                facet_vertices = facet.get_vertices()
                string = 'f'
                for vertex in facet_vertices:
                    string = string + ' ' + str(vertex.index + 1) ##obj vertex indexing starts at 1
                string = string + '\n'
                file.write(string)

            

    def get_halfedge(self, u, v):
        """Retrieve halfedge with starting vertex u and target vertex v

        u - starting vertex
        v - target vertex

        Returns a halfedge
        """
        return self.edges[(u, v)]

    def update_vertices(self, vertices):
        # update vertices
        vlist = []
        i = 0
        for v in vertices:
            vlist.append(Vertex(v[0], v[1], v[2], i))
            vlist[-1].index = i
            i += 1
        self.vertices = vlist


        hlist = []
        # update all the halfedges
        for he in self.halfedges:
            vi = he.vertex.index
            hlist.append(Halfedge(None, None, None, self.vertices[vi], None,
                he.index))

        flist = []
        # update neighboring halfedges
        for f in self.facets:
            hi = f.halfedge.index
            flist.append(Facet(f.a, f.b, f.c, f.index,  hlist[hi]))
        self.facets = flist


        i = 0
        for he in self.halfedges:
            nextid = he.next.index
            oppid = he.opposite.index
            previd = he.prev.index

            hlist[i].next = hlist[nextid]
            hlist[i].opposite = hlist[oppid]
            hlist[i].prev = hlist[previd]


            fi = he.facet.index
            hlist[i].facet = flist[fi]
            i += 1

        self.halfedges = hlist


class Vertex:

    def __init__(self, x=0, y=0, z=0, index=None, halfedge=None):
        """Create a vertex with given index at given point.

        x        - x-coordinate of the point
        y        - y-coordinate of the point
        z        - z-coordinate of the point
        index    - integer index of this vertex
        halfedge - a halfedge that points to the vertex
        """

        self.x = x
        self.y = y
        self.z = z

        self.index = index

        self.halfedge = halfedge
    
    def update(self, halfedge):
        self.halfedge = halfedge

    def __eq__(x, y):
        return x.__key() == y.__key() and type(x) == type(y)

    def __key(self):
        return (self.x, self.y, self.z, self.index)

    def __hash__(self):
        return hash(self.__key())

    def get_vertex(self):
        return [self.x, self.y, self.z]


class Facet:

    def __init__(self, a=-1, b=-1, c=-1, index=None, halfedge=None):
        """Create a facet with the given index with three vertices.

        a, b, c - indices for the vertices in the facet, counter clockwise.
        index - index of facet in the mesh
        halfedge - a Halfedge that belongs to the facet
        """
        self.a = a
        self.b = b
        self.c = c
        self.index = index
        
        self.halfedge = halfedge
    
    def update(self, halfedge):
        self.halfedge = halfedge

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.c == other.c \
            and self.index == other.index and self.halfedge == other.halfedge

    def __hash__(self):
        return hash(self.halfedge) ^ hash(self.a) ^ hash(self.b) ^ \
            hash(self.c) ^ hash(self.index) ^ \
            hash((self.halfedges, self.a, self.b, self.c, self.index))
            
    def get_vertices(self):
        vertices = []
        h0 = self.halfedge
        v0 = h0.vertex
        vertices.append(v0)
        
        h = h0
        while True:
            h = h.next
            if h == h0:
                break
            else:
                vertices.append(h.vertex)
                
        return vertices

    def get_normal(self):
        """Calculate the normal of facet

        Return a python list that contains the normal
        """
        vertex_a = [self.halfedge.vertex.x, self.halfedge.vertex.y,
                    self.halfedge.vertex.z]

        vertex_b = [self.halfedge.next.vertex.x, self.halfedge.next.vertex.y,
                    self.halfedge.next.vertex.z]

        vertex_c = [self.halfedge.prev.vertex.x, self.halfedge.prev.vertex.y,
                    self.halfedge.prev.vertex.z]

        # create edge 1 with vector difference
        edge1 = [u - v for u, v in zip(vertex_b, vertex_a)]
        edge1 = normalize(edge1)
        # create edge 2 ...
        edge2 = [u - v for u, v in zip(vertex_c, vertex_b)]
        edge2 = normalize(edge2)

        # cross product
        normal = cross_product(edge1, edge2)

        normal = normalize(normal)

        return normal


class Halfedge:

    def __init__(self, next=None, opposite=None, prev=None, vertex=None,
                 facet=None, index=None):
        """Create a halfedge with given index.
        """
        self.opposite = opposite
        self.next = next
        self.prev = prev
        self.vertex = vertex
        self.facet = facet
        self.index = index

    def __eq__(self, other):
        # TODO Test more
        return (self.vertex == other.vertex) and \
               (self.next.vertex == other.next.vertex) ###
               

    def __hash__(self):
        return hash(self.opposite) ^ hash(self.next) ^ hash(self.prev) ^ \
                hash(self.vertex) ^ hash(self.facet) ^ hash(self.index) ^ \
                hash((self.opposite, self.next, self.prev, self.vertex,
                    self.facet, self.index))
    
    def update(self, vertex=None, next=None, facet=None, opposite=None):
        if not vertex is None:
            self.vertex = vertex
        if not next is None:
            self.next = next
        if not facet is None:
            self.facet = facet
        if not opposite is None:
            self.opposite = opposite
            

    def get_angle_normal(self):
        """Calculate the angle between the normals that neighbor the edge.

        Return an angle in radians
        """
        a = self.facet.get_normal()
        b = self.opposite.facet.get_normal()

        dir = [self.vertex.x - self.prev.vertex.x,
               self.vertex.y - self.prev.vertex.y,
               self.vertex.z - self.prev.vertex.z]
        dir = normalize(dir)

        ab = dot(a, b)

        args = ab / (norm(a) * norm(b))

        if allclose(args, 1):
            args = 1
        elif allclose(args, -1):
            args = -1

        assert (args <= 1.0 and args >= -1.0)

        angle = math.acos(args)

        if not (angle % math.pi == 0):
            e = cross_product(a, b)
            e = normalize(e)

            vec = dir
            vec = normalize(vec)

            if (allclose(vec, e)):
                return angle
            else:
                return -angle
        else:
            return 0


def allclose(v1, v2):
    """Compare if v1 and v2 are close

    v1, v2 - any numerical type or list/tuple of numerical types

    Return bool if vectors are close, up to some epsilon specified in config.py
    """

    v1 = make_iterable(v1)
    v2 = make_iterable(v2)

    elementwise_compare = map(
        (lambda x, y: abs(x - y) < config.EPSILON), v1, v2)
    return reduce((lambda x, y: x and y), elementwise_compare)


def make_iterable(obj):
    """Check if obj is iterable, if not return an iterable with obj inside it.
    Otherwise just return obj.

    obj - any type

    Return an iterable
    """
    try:
        iter(obj)
    except:
        return [obj]
    else:
        return obj


def dot(v1, v2):
    """Dot product(inner product) of v1 and v2

    v1, v2 - python list

    Return v1 dot v2
    """
    elementwise_multiply = map((lambda x, y: x * y), v1, v2)
    return reduce((lambda x, y: x + y), elementwise_multiply)


def norm(vec):
    """ Return the Euclidean norm of a 3d vector.

    vec - a 3d vector expressed as a list of 3 floats.
    """
    return math.sqrt(reduce((lambda x, y: x + y * y), vec, 0.0))


def normalize(vec):
    """Normalize a vector

    vec - python list

    Return normalized vector
    """
    if norm(vec) < 1e-6:
        return [0 for i in range(len(vec))]
    return map(lambda x: x / norm(vec), vec)


def cross_product(v1, v2):
    """ Return the cross product of v1, v2.

    v1, v2 - 3d vector expressed as a list of 3 floats.
    """
    x3 = v1[1] * v2[2] - v2[1] * v1[2]
    y3 = -(v1[0] * v2[2] - v2[0] * v1[2])
    z3 = v1[0] * v2[1] - v2[0] * v1[1]
    return [x3, y3, z3]

def create_vector(p1, p2):
    """Contruct a vector going from p1 to p2.

    p1, p2 - python list wth coordinates [x,y,z].

    Return a list [x,y,z] for the coordinates of vector
    """
    return map((lambda x,y: x-y), p2, p1)
