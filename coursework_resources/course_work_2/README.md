# Coursework 2 F&Q list


1. Gaussian curvature: Gaussian curvature only depends on angle deficit AND your A_i. the choices of A_i include Barycentric area and Voronoi area. 

2. curvature visualization: a basic version is to show the difference between flat area and complex area. 
https://stackoverflow.com/questions/15140072/how-to-map-number-to-color-using-matplotlibs-colormap 
   <img src="https://libigl.github.io/images/bumpy-gaussian-curvature.jpg" height="250">

3. question 4, eigenvectors of the Laplace-Beltrami : please use cotangent version

4. question 4, 
reference handout: 
https://moodle.ucl.ac.uk/pluginfile.php/1425455/mod_resource/content/1/laplace_beltrami_and_eigenanalysis.pdf  

   reference paper: [Spectral Geometry Processing with Manifold Harmonics](http://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Vallet08.pdf).  
    
```Section 2.3 and 3.1 provide the details related to question3.  
Equation (7) shows how to transform between canonical and MHB space (eigen space)  
`star_0` => our `M`  
`x` => canonical coordinates  
`\tilde{x}` => the coordinates in eigen space  
````

5. Sparse solver in python:
 https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.eigs.html 

6. Sparse solver opotions in cpp - use **igl::eigs**  
[igl::eigs(A,B,EIGS_TYPE_SM ,x,s)](https://github.com/libigl/libigl/blob/508cb9940f4d1e8e54137d5afe2fd2eb9c4dc672/include/igl/eigs.h).  
It solves the generalized eigenvalue problem `A x = s B x`.  
STEPS:  
i. apply a hotfix at here [url](https://gist.github.com/yushiangw/c4579efca5a7ee7c5a0e3903dc8d165a) by replacing the file `libigl\include\igl\eigs.cpp`. The original implementation has numerical problems.  
ii. solve : `(-1*C) x = s M x`. `(-1*C)` is a trick to make this matrix become P.S.D.  
iii. `(-1*C) x = s M x` is equal to `M^(-1)(-1*C) x = s x` so now `x` is the eigenvectors of `M^(-1)*(-1*C)`. 

7. Sparse solver opotions in cpp - use **Spectra**  
url: [https://spectralib.org/]  
  
   Spectra and Eigen3 in cpp : Spectra requires Eigen 3.3.7. check your eigen's major version before use it:  
`	std::cout<<"eigen version.:"<<EIGEN_WORLD_VERSION<<","<<EIGEN_MAJOR_VERSION  << EIGEN_MINOR_VERSION<<"\n";`

