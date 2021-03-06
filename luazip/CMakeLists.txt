cmake_minimum_required(VERSION 3.2.3)

PROJECT("luazip")

INCLUDE(ExternalProject)

SET(VERSION_EXTERNAL "1.2.3")
SET(VERSION_PACKAGE  "1")
SET(PROJECT_VERSION  "${VERSION_EXTERNAL}.${VERSION_PACKAGE}")

# Get the VCS version for the jonchki configuration.
INCLUDE(${CMAKE_HOME_DIRECTORY}/cmake/version.cmake)

# Filter the jonchki configuration.
CONFIGURE_FILE(installer/lua${BUILDCFG_LUA_VERSION}/luazip.xml
               ${CMAKE_CURRENT_BINARY_DIR}/lua${BUILDCFG_LUA_VERSION}-luazip-${PROJECT_VERSION}.xml
               @ONLY)


#----------------------------------------------------------------------------
#
# Build the project.
#
IF((${BUILDCFG_ONLY_JONCHKI_CFG} STREQUAL "OFF"))
	# Select the LUA version.
	INCLUDE(${CMAKE_HOME_DIRECTORY}/cmake/muhkuh_lua.cmake)

	SET(PRJ_CMAKE_ARGS "")
	LIST(APPEND PRJ_CMAKE_ARGS "-DCMAKE_C_FLAGS=${CMAKE_C_FLAGS}")
	LIST(APPEND PRJ_CMAKE_ARGS "-DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME}")
	LIST(APPEND PRJ_CMAKE_ARGS "-DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}")
	LIST(APPEND PRJ_CMAKE_ARGS "-DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}")
	IF(${CMAKE_SYSTEM_NAME} STREQUAL "Windows")
		LIST(APPEND PRJ_CMAKE_ARGS "-DCMAKE_RC_COMPILER=${CMAKE_RC_COMPILER}")
	ENDIF(${CMAKE_SYSTEM_NAME} STREQUAL "Windows")
	LIST(APPEND PRJ_CMAKE_ARGS "-DLUA_LIBRARIES=${LUA_LIBRARIES}")
	LIST(APPEND PRJ_CMAKE_ARGS "-DLUA_INCLUDE_DIR=${LUA_INCLUDE_DIR}")
	LIST(APPEND PRJ_CMAKE_ARGS "-Dnet.zlib-zlib_DIR=${CMAKE_BINARY_DIR}/build_requirements/jonchki/install/dev/cmake")
	LIST(APPEND PRJ_CMAKE_ARGS "-DZZIPLIB_LIBRARY=${ZZIPLIB_LIBRARY}")
	LIST(APPEND PRJ_CMAKE_ARGS "-DZZIPLIB_INCLUDE_DIR=${ZZIPLIB_INCLUDE_DIR}")
	LIST(APPEND PRJ_CMAKE_ARGS "-DCMAKE_INSTALL_PREFIX=''")


	ExternalProject_Add(TARGET_luazip
	                    PREFIX ${CMAKE_CURRENT_BINARY_DIR}/luazip-${VERSION_EXTERNAL}
	                    URL ${CMAKE_CURRENT_SOURCE_DIR}/luazip-1_2_3.tar.gz
	                    URL_HASH SHA1=ba682a03675b4927f4e52cddad891bf3a1cdf1f6
	                    PATCH_COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/templates ${CMAKE_CURRENT_BINARY_DIR}/luazip-${VERSION_EXTERNAL}/src/TARGET_luazip
	                    CMAKE_ARGS ${PRJ_CMAKE_ARGS}
	                    TEST_COMMAND make test
	                    INSTALL_COMMAND make install DESTDIR=${CMAKE_CURRENT_BINARY_DIR}/rock
	)

	# Write a version file.
	FILE(WRITE ${CMAKE_CURRENT_BINARY_DIR}/install/com.github.luaforge-luazip.version "SET(com.github.luaforge-luazip_VERSION ${VERSION_EXTERNAL}.${VERSION_PACKAGE})")
ENDIF((${BUILDCFG_ONLY_JONCHKI_CFG} STREQUAL "OFF"))
