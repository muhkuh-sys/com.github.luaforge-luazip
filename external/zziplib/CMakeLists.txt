cmake_minimum_required(VERSION 3.2.3)

PROJECT("zziplib")

INCLUDE(ExternalProject)


#----------------------------------------------------------------------------
#
# Build the project.
#

SET(PRJ_CMAKE_ARGS "")
LIST(APPEND PRJ_CMAKE_ARGS "-DCMAKE_C_FLAGS=${CMAKE_C_FLAGS}")
LIST(APPEND PRJ_CMAKE_ARGS "-DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME}")
LIST(APPEND PRJ_CMAKE_ARGS "-DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}")
IF(${CMAKE_SYSTEM_NAME} STREQUAL "Windows")
	LIST(APPEND PRJ_CMAKE_ARGS "-DCMAKE_RC_COMPILER=${CMAKE_RC_COMPILER}")
ENDIF(${CMAKE_SYSTEM_NAME} STREQUAL "Windows")
LIST(APPEND PRJ_CMAKE_ARGS "-Dnet.zlib-zlib_DIR=${CMAKE_BINARY_DIR}/build_requirements/jonchki/install/dev/cmake")
LIST(APPEND PRJ_CMAKE_ARGS "-DCMAKE_INSTALL_PREFIX=''")


ExternalProject_Add(TARGET_zziplib
                    PREFIX ${CMAKE_CURRENT_BINARY_DIR}/zziplib-0.13.62
                    URL ${CMAKE_CURRENT_SOURCE_DIR}/zziplib-0.13.62.tar.bz2
                    URL_HASH SHA1=cf8b642abd9db618324a1b98cc71492a007cd687
                    PATCH_COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/templates ${CMAKE_CURRENT_BINARY_DIR}/zziplib-0.13.62/src/TARGET_zziplib
                    CMAKE_ARGS ${PRJ_CMAKE_ARGS}
                    INSTALL_COMMAND make install DESTDIR=${CMAKE_CURRENT_BINARY_DIR}/install
)

SET(ZZIPLIB_LIBRARY      ${CMAKE_CURRENT_BINARY_DIR}/install/lib/libzziplib.a  CACHE INTERNAL "The complete path to the library.")
SET(ZZIPLIB_INCLUDE_DIR  ${CMAKE_CURRENT_BINARY_DIR}/install/include           CACHE INTERNAL "The include folder for the library.")
