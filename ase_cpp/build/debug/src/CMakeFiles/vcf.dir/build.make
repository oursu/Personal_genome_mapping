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
CMAKE_BINARY_DIR = /media/fusion10/work/chromatinVariation/src/ase_cpp/build/debug

# Include any dependencies generated for this target.
include src/CMakeFiles/vcf.dir/depend.make

# Include the progress variables for this target.
include src/CMakeFiles/vcf.dir/progress.make

# Include the compile flags for this target's objects.
include src/CMakeFiles/vcf.dir/flags.make

src/CMakeFiles/vcf.dir/VcfUtil.cpp.o: src/CMakeFiles/vcf.dir/flags.make
src/CMakeFiles/vcf.dir/VcfUtil.cpp.o: ../../src/VcfUtil.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /media/fusion10/work/chromatinVariation/src/ase_cpp/build/debug/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object src/CMakeFiles/vcf.dir/VcfUtil.cpp.o"
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/debug/src && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/vcf.dir/VcfUtil.cpp.o -c /media/fusion10/work/chromatinVariation/src/ase_cpp/src/VcfUtil.cpp

src/CMakeFiles/vcf.dir/VcfUtil.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/vcf.dir/VcfUtil.cpp.i"
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/debug/src && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /media/fusion10/work/chromatinVariation/src/ase_cpp/src/VcfUtil.cpp > CMakeFiles/vcf.dir/VcfUtil.cpp.i

src/CMakeFiles/vcf.dir/VcfUtil.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/vcf.dir/VcfUtil.cpp.s"
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/debug/src && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /media/fusion10/work/chromatinVariation/src/ase_cpp/src/VcfUtil.cpp -o CMakeFiles/vcf.dir/VcfUtil.cpp.s

src/CMakeFiles/vcf.dir/VcfUtil.cpp.o.requires:
.PHONY : src/CMakeFiles/vcf.dir/VcfUtil.cpp.o.requires

src/CMakeFiles/vcf.dir/VcfUtil.cpp.o.provides: src/CMakeFiles/vcf.dir/VcfUtil.cpp.o.requires
	$(MAKE) -f src/CMakeFiles/vcf.dir/build.make src/CMakeFiles/vcf.dir/VcfUtil.cpp.o.provides.build
.PHONY : src/CMakeFiles/vcf.dir/VcfUtil.cpp.o.provides

src/CMakeFiles/vcf.dir/VcfUtil.cpp.o.provides.build: src/CMakeFiles/vcf.dir/VcfUtil.cpp.o

# Object files for target vcf
vcf_OBJECTS = \
"CMakeFiles/vcf.dir/VcfUtil.cpp.o"

# External object files for target vcf
vcf_EXTERNAL_OBJECTS =

src/libvcf.a: src/CMakeFiles/vcf.dir/VcfUtil.cpp.o
src/libvcf.a: src/CMakeFiles/vcf.dir/build.make
src/libvcf.a: src/CMakeFiles/vcf.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX static library libvcf.a"
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/debug/src && $(CMAKE_COMMAND) -P CMakeFiles/vcf.dir/cmake_clean_target.cmake
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/debug/src && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/vcf.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/CMakeFiles/vcf.dir/build: src/libvcf.a
.PHONY : src/CMakeFiles/vcf.dir/build

src/CMakeFiles/vcf.dir/requires: src/CMakeFiles/vcf.dir/VcfUtil.cpp.o.requires
.PHONY : src/CMakeFiles/vcf.dir/requires

src/CMakeFiles/vcf.dir/clean:
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/debug/src && $(CMAKE_COMMAND) -P CMakeFiles/vcf.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/vcf.dir/clean

src/CMakeFiles/vcf.dir/depend:
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /media/fusion10/work/chromatinVariation/src/ase_cpp /media/fusion10/work/chromatinVariation/src/ase_cpp/src /media/fusion10/work/chromatinVariation/src/ase_cpp/build/debug /media/fusion10/work/chromatinVariation/src/ase_cpp/build/debug/src /media/fusion10/work/chromatinVariation/src/ase_cpp/build/debug/src/CMakeFiles/vcf.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/CMakeFiles/vcf.dir/depend

