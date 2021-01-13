cmake_minimum_required(VERSION 3.1)
project(viewer)


# set the directory of cmake macro file 
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/../../../../cmake)

# set libigl's magic options 
option(LIBIGL_WITH_OPENGL            "Use OpenGL"         ON)
option(LIBIGL_WITH_OPENGL_GLFW       "Use GLFW"           ON)
option(LIBIGL_WITH_OPENGL_GLFW_IMGUI   "Use GLFW_IMGUI"  ON )


# Ask cmake to find LibIGL use FindLIBIGL.cmake in CMAKE_MODULE_PATH
find_package(LIBIGL REQUIRED ) 

# print message
message(CMAKE_CURRENT_SOURCE_DIR=${CMAKE_CURRENT_SOURCE_DIR} )
message(found_LibIGL_include_dir=${LIBIGL_INCLUDE_DIR} )

# collect *.cpp files 
file(GLOB SRCFILES src/*.cpp)

# set binary name 
set(EXE_NAME ${PROJECT_NAME}_bin)
# add binary 
add_executable(${EXE_NAME} ${SRCFILES})

# link library
target_link_libraries(${EXE_NAME} PUBLIC  
        igl::core 
        igl::opengl 
        igl::opengl_glfw 
        igl::opengl_glfw_imgui 
)

# add include directory - use nanoflann as an example
target_include_directories( ${EXE_NAME}  PUBLIC
                           ${CMAKE_CURRENT_SOURCE_DIR}/../../../../cpp_lib/nanoflann
                          )