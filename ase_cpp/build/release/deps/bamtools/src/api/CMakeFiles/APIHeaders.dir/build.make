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

# Utility rule file for APIHeaders.

# Include the progress variables for this target.
include deps/bamtools/src/api/CMakeFiles/APIHeaders.dir/progress.make

deps/bamtools/src/api/CMakeFiles/APIHeaders:
	$(CMAKE_COMMAND) -E cmake_progress_report /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Exporting APIHeaders"

APIHeaders: deps/bamtools/src/api/CMakeFiles/APIHeaders
APIHeaders: deps/bamtools/src/api/CMakeFiles/APIHeaders.dir/build.make
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/api_global.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/api_global.h
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/BamAlignment.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/BamAlignment.h
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/BamAux.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/BamAux.h
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/BamConstants.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/BamConstants.h
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/BamIndex.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/BamIndex.h
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/BamMultiReader.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/BamMultiReader.h
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/BamReader.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/BamReader.h
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/BamWriter.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/BamWriter.h
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/SamConstants.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/SamConstants.h
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/SamHeader.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/SamHeader.h
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/SamProgram.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/SamProgram.h
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/SamProgramChain.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/SamProgramChain.h
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/SamReadGroup.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/SamReadGroup.h
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/SamReadGroupDictionary.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/SamReadGroupDictionary.h
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/SamSequence.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/SamSequence.h
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && /usr/local/bin/cmake -E copy_if_different /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api/SamSequenceDictionary.h /media/fusion10/work/chromatinVariation/src/ase_cpp/include/api/SamSequenceDictionary.h
.PHONY : APIHeaders

# Rule to build all files generated by this target.
deps/bamtools/src/api/CMakeFiles/APIHeaders.dir/build: APIHeaders
.PHONY : deps/bamtools/src/api/CMakeFiles/APIHeaders.dir/build

deps/bamtools/src/api/CMakeFiles/APIHeaders.dir/clean:
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api && $(CMAKE_COMMAND) -P CMakeFiles/APIHeaders.dir/cmake_clean.cmake
.PHONY : deps/bamtools/src/api/CMakeFiles/APIHeaders.dir/clean

deps/bamtools/src/api/CMakeFiles/APIHeaders.dir/depend:
	cd /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /media/fusion10/work/chromatinVariation/src/ase_cpp /media/fusion10/work/chromatinVariation/src/ase_cpp/deps/bamtools/src/api /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api /media/fusion10/work/chromatinVariation/src/ase_cpp/build/release/deps/bamtools/src/api/CMakeFiles/APIHeaders.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : deps/bamtools/src/api/CMakeFiles/APIHeaders.dir/depend
