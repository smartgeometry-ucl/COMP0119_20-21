
## Polyscope

[Polyscope](https://polyscope.run) is an alternative viewer that integrates well with libigl and all other libraries.

Check out this example:

```
git clone --recurse-submodules https://github.com/nmwsharp/libigl-polyscope-project-template.git
cd libigl-polyscope-project-template
mkdir build
cd build
cmake ..
make -j4

./bin/libIGL-polyscope-example ../bunnyhead.obj

./bin/libIGL-polyscope-example ../spot.obj
```

---

If the compilation crashes change line 78 for file `src/main.cpp`:
```
b(1) = bnd(round(bnd.size() / 2));
```
to
```
b(1) = bnd((int)round(bnd.size() / 2));
```
