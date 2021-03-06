cmake_minimum_required (VERSION 2.6)

project (RnaTools)

# Set default build type
set (CMAKE_BUILD_TYPE, Release)

set (CMAKE_CURRENT_BINARY_DIR, builds)

# ==================== UTILITY FUNCTIONS ==================== 

# ==================== FLAGS ==================== 

#set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -D_FILE_OFFSET_BITS=64 -fopenmp -Wall -Wextra -Wno-sign-compare -static")
#set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CMAKE_C_FLAGS} -Wno-deprecated -static")
set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -D_FILE_OFFSET_BITS=64 -Wall -Wextra -Wno-sign-compare")
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CMAKE_C_FLAGS} -Wno-deprecated")

set (CMAKE_C_FLAGS_RELEASE "-O2")
set (CMAKE_CXX_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE}")

set (CMAKE_C_FLAGS_DEBUG "-g -DDEBUG=1 -O0")
set (CMAKE_CXX_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG}")

# ==================== External libraries =======

# If compiling dependencies from source, comment these out
set (bamtools_INCLUDE_DIR ${RnaTools_SOURCE_DIR}/include ${RnaTools_SOURCE_DIR}/include/api ${RnaTools_SOURCE_DIR}/include/shared)
set (bamtools_LIBRARY -L${RnaTools_SOURCE_DIR}/lib -lbamtools -lz)

# ==================== CHECKS ==================== 

# verify that we have openmp
#INCLUDE(CheckCCompilerFlag)
# Make sure the C compile can take -fopenmp as a flag
#CHECK_C_COMPILER_FLAG(-fopenmp HAVE_OPENMP)

# ==================== PROJECT DIRECTORIES ==================== 

add_subdirectory(deps/swak)
add_subdirectory(deps/vcftools)
# If source is included, uncomment this
add_subdirectory(deps/bamtools)
add_subdirectory(src)
add_subdirectory(test)
