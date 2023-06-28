cmake_minimum_required(VERSION 3.16)

# CMake and Boost version was chosen based on Ubuntu 20.04.6 LTS (Focal Fossa) repo

project(
  binclust
  VERSION 0.1.0
  LANGUAGES CXX
)

# Using C++20, may cause compatability issue in future works/integration
set(CMAKE_CXX_STANDARD 20)
set(CXX_STANDARD_REQUIRED YES)
set(CXX_EXTENSIONS NO)

# For clangd
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# OPTIMIZE exe
include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-march=native" COMPILER_SUPPORTS_MARCH_NATIVE)
if(COMPILER_SUPPORTS_MARCH_NATIVE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()

# Warnings
if(MSVC)
  add_compile_options(/W4)
else()
  add_compile_options(-Wall -Wextra -pedantic)
endif()

find_package(Threads REQUIRED)
find_package(igraph 0.10.4 REQUIRED)

# find igraph
# set(igraph_DIR "${CMAKE_CURRENT_SOURCE_DIR}/lib/igraph/lib/cmake/igraph")
# set(igraph_DEBUG ON)
# find_package(igraph 0.10.4 REQUIRED)
# if(igraph_FOUND)
#   message(status "igraph found")
# else()
#   message(status "igraph not found")
# endif()

#executables
# include_directories()
include_directories(${CMAKE_CURRENT_SOURCE_DIR})
link_libraries(igraph::igraph Threads::Threads)

add_executable(CmdRunner "src/CmdRunner.cpp")