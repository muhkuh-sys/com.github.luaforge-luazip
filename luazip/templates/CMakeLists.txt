CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

PROJECT("luazip")

ENABLE_TESTING()
FIND_PACKAGE(PythonInterp REQUIRED)


FIND_PACKAGE(net.zlib-zlib REQUIRED CONFIG)
GET_TARGET_PROPERTY(ZLIB_LIBRARY net.zlib-zlib::zlibstatic LOCATION)
SET(ZLIB_INCLUDE_DIR "${net.zlib-zlib_INCLUDE_DIR}")


# Build the Lua modules.
ADD_LIBRARY(TARGET_luazip MODULE
            src/luazip.c)
TARGET_INCLUDE_DIRECTORIES(TARGET_luazip
                           PRIVATE ${LUA_INCLUDE_DIR} ${ZLIB_INCLUDE_DIR} ${ZZIPLIB_INCLUDE_DIR})
TARGET_LINK_LIBRARIES(TARGET_luazip ${LUA_LIBRARIES} ${ZZIPLIB_LIBRARY} ${ZLIB_LIBRARY})
SET_TARGET_PROPERTIES(TARGET_luazip PROPERTIES PREFIX "" OUTPUT_NAME "zip")


# On mingw link all compiler libraries static.
IF((${CMAKE_SYSTEM_NAME} STREQUAL "Windows") AND (${CMAKE_COMPILER_IS_GNUCC}))
	SET_PROPERTY(TARGET TARGET_luazip PROPERTY LINK_FLAGS "-static -static-libgcc -static-libstdc++")
ENDIF((${CMAKE_SYSTEM_NAME} STREQUAL "Windows") AND (${CMAKE_COMPILER_IS_GNUCC}))

# Install the LUA module.
INSTALL(TARGETS TARGET_luazip
        EXPORT EXPORT_package
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
        RUNTIME DESTINATION bin
        INCLUDES DESTINATION include)


# Add tests for this module.
IF((${CMAKE_SYSTEM_NAME} STREQUAL "Windows") AND (${CMAKE_COMPILER_IS_GNUCC}))
	# Here are the MinGW specific tests.
	ADD_TEST(NAME luafilesystem_MinGW_DLL_dependencies
	         COMMAND "${PYTHON_EXECUTABLE}" ${CMAKE_HOME_DIRECTORY}/cmake/tests/mingw_dll_dependencies.py -u lua5.1 -u lua5.2 -u lua5.3 $<TARGET_FILE:TARGET_luazip>)
ENDIF((${CMAKE_SYSTEM_NAME} STREQUAL "Windows") AND (${CMAKE_COMPILER_IS_GNUCC}))
