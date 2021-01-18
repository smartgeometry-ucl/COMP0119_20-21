# Coursework 1 FAQ list


1. Loading PLY: you can also use igl::readPLY and writePLY.

2. Sub-sampling step in ICP: we suggest you start with non-subsampling step (use all input points if your machine allows). After your implementation looks work, you can try sub-sampling and answer question `4. Instead of directly aligning...` 

3. Rejection step in ICP: a simple one is to check normal vectors' angle

4. Visualization: you can also use MeshLab to create some result screenshots. 

5. Can I just visualize 'points' instead of meshes ? : ok -- make sure we can understand your alignment results and also see the normal information through point color (question 6)

6. What is `Adjust the amount of noise based on the bounding box dimensions ...` 
Give a point set, its bounding box can be defined by the maximum and the minimum coordinates. This step is used to add meaningful noises since the coordinate of a mesh is not always aligned with the real world metric (so 0.1 in M2's space can be 0.1 cm/0.1 meters or 0.1 X depends on how M2 is created) 

7. What is normal shading:
Normal shading : points colored based on their normals being mapped to rgb. It can be changing vertices color using normal vectors, e.g.,

![Image](/course_work_1/imgs/nv_shading.png)

8. Question 4, subsample rate - trimesh.sample is a function for sampling points on the input MESH. Question 4 is asking to reduce the # of input points(vertices in our case). If you do trimesh.sample on the input bunny mesh (which is a imperfect mesh as you can see), you will introduce many noisy points. In pratical, we have input scans as points sets, then we do registeration and get a reconstructed mesh. Please apply your sampling method directly on the input points(vertices). 

9. Point selection in ICP: there are many subsampling strategies. In this [paper](https://graphics.stanford.edu/papers/stabicp/stabicp.pdf), they subsample on the source points (see Section 3).


## Results reference

**bun045.ply TO bun000.ply**  
Config: no noise/no subsampling/no rejection/point2point  
![Image](/course_work_1/imgs/45_to_00.gif)
![Image](/course_work_1/imgs/45_to_00_fin.jpg) 
![Image](/course_work_1/imgs/45_to_00_err.jpg)  


**bun090.ply TO bun000.ply**  
Config: no noise/no subsampling/no rejection/point2point  
![Image](/course_work_1/imgs/90_to_00.gif)
![Image](/course_work_1/imgs/90_to_00_fin.jpg) 
![Image](/course_work_1/imgs/90_to_00_err.jpg)
