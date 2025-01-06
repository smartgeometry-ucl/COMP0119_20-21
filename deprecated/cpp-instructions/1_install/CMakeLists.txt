cmake_minimum_required(VERSION 3.1)
project(hello_world)

# exe name 
set(EXE_NAME ${PROJECT_NAME}_bin)

# add xxx.cpp file  
file(GLOB SRCFILES src/*.cpp)
add_executable(${EXE_NAME} ${SRCFILES}) 

