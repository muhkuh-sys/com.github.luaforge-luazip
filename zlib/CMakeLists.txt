cmake_minimum_required(VERSION 3.2.3)

PROJECT("zlib")

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
LIST(APPEND PRJ_CMAKE_ARGS "-DCMAKE_INSTALL_PREFIX=''")


ExternalProject_Add(TARGET_zlib
                    PREFIX ${CMAKE_CURRENT_BINARY_DIR}/zlib-1.2.8
                    URL ${CMAKE_CURRENT_SOURCE_DIR}/zlib-1.2.8.tar.gz
                    URL_HASH SHA1=a4d316c404ff54ca545ea71a27af7dbc29817088
                    CMAKE_ARGS ${PRJ_CMAKE_ARGS}
                    INSTALL_COMMAND make install DESTDIR=${CMAKE_CURRENT_BINARY_DIR}/install
)

SET(ZLIB_LIBRARY      ${CMAKE_CURRENT_BINARY_DIR}/install/lib/libzlibstatic.a   CACHE INTERNAL "The complete path to the zlib library.")
SET(ZLIB_INCLUDE_DIR  ${CMAKE_CURRENT_BINARY_DIR}/install/include               CACHE INTERNAL "The include folder for the zlib library.")

