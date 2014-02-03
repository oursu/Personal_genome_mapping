# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E remove -f

# The program to use to edit the cache.
CMAKE_EDIT_COMMAND = /usr/local/bin/ccmake

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /media/fusion10/work/chromatinVariation/src/ase_cpp

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release

# Include any dependencies generated for this target.
include test/CMakeFiles/TestRna.dir/depend.make

# Include the progress variables for this target.
include test/CMakeFiles/TestRna.dir/progress.make

# Include the compile flags for this target's objects.
include test/CMakeFiles/TestRna.dir/flags.make

test/CMakeFiles/TestRna.dir/TestRna.cpp.o: test/CMakeFiles/TestRna.dir/flags.make
test/CMakeFiles/TestRna.dir/TestRna.cpp.o: ../../test/TestRna.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object test/CMakeFiles/TestRna.dir/TestRna.cpp.o"
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/test && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/TestRna.dir/TestRna.cpp.o -c /media/fusion10/work/chromatinVariation/src/ase_cpp/test/TestRna.cpp

test/CMakeFiles/TestRna.dir/TestRna.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/TestRna.dir/TestRna.cpp.i"
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/test && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /media/fusion10/work/chromatinVariation/src/ase_cpp/test/TestRna.cpp > CMakeFiles/TestRna.dir/TestRna.cpp.i

test/CMakeFiles/TestRna.dir/TestRna.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/TestRna.dir/TestRna.cpp.s"
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/test && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /media/fusion10/work/chromatinVariation/src/ase_cpp/test/TestRna.cpp -o CMakeFiles/TestRna.dir/TestRna.cpp.s

test/CMakeFiles/TestRna.dir/TestRna.cpp.o.requires:
.PHONY : test/CMakeFiles/TestRna.dir/TestRna.cpp.o.requires

test/CMakeFiles/TestRna.dir/TestRna.cpp.o.provides: test/CMakeFiles/TestRna.dir/TestRna.cpp.o.requires
	$(MAKE) -f test/CMakeFiles/TestRna.dir/build.make test/CMakeFiles/TestRna.dir/TestRna.cpp.o.provides.build
.PHONY : test/CMakeFiles/TestRna.dir/TestRna.cpp.o.provides

test/CMakeFiles/TestRna.dir/TestRna.cpp.o.provides.build: test/CMakeFiles/TestRna.dir/TestRna.cpp.o

# Object files for target TestRna
TestRna_OBJECTS = \
"CMakeFiles/TestRna.dir/TestRna.cpp.o"

# External object files for target TestRna
TestRna_EXTERNAL_OBJECTS =

test/TestRna: test/CMakeFiles/TestRna.dir/TestRna.cpp.o
test/TestRna: test/CMakeFiles/TestRna.dir/build.make
test/TestRna: deps/swak/src/libswak.a
test/TestRna: src/libgene.a
test/TestRna: deps/swak/src/libswak.a
test/TestRna: deps/swak/deps/yaml-cpp/libyaml-cpp.a
test/TestRna: test/CMakeFiles/TestRna.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX executable TestRna"
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/TestRna.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
test/CMakeFiles/TestRna.dir/build: test/TestRna
.PHONY : test/CMakeFiles/TestRna.dir/build

test/CMakeFiles/TestRna.dir/requires: test/CMakeFiles/TestRna.dir/TestRna.cpp.o.requires
.PHONY : test/CMakeFiles/TestRna.dir/requires

test/CMakeFiles/TestRna.dir/clean:
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/test && $(CMAKE_COMMAND) -P CMakeFiles/TestRna.dir/cmake_clean.cmake
.PHONY : test/CMakeFiles/TestRna.dir/clean

test/CMakeFiles/TestRna.dir/depend:
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /media/fusion10/work/chromatinVariation/src/ase_cpp /media/fusion10/work/chromatinVariation/src/ase_cpp/test /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/test /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/test/CMakeFiles/TestRna.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : test/CMakeFiles/TestRna.dir/depend

