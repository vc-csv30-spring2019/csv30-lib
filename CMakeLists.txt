
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_HOME_DIRECTORY}/bin/)

file(GLOB_RECURSE ASSIGNMENT_SOURCES RELATIVE ${CMAKE_SOURCE_DIR} "src/*.cc" "src/*.cpp")
file(GLOB_RECURSE ASSIGNMENT_INCLUDES RELATIVE ${CMAKE_SOURCE_DIR} "include/*.h")
list(REMOVE_ITEM ASSIGNMENT_SOURCES "src/${SOURCE_PREFIX}_unittest.cc")

add_executable(${EXEC_NAME} ${ASSIGNMENT_SOURCES} ${ASSIGNMENT_INCLUDES})
include_directories(include/ csv13-lib/include)

if(WIN32) 
	set(PLATFORM "Win32")
	set(CMAKE_CXX_FLAGS_RELEASE "/MT")
	set(CMAKE_CXX_FLAGS_DEBUG "/MTd")
elseif(APPLE)
	set(PLATFORM "Darwin")
        link_libraries(gtestd gtest_maind pthread)
else()
	set(PLATFORM "Linux")
        link_libraries(gtestd gtest_maind pthread)
endif()


link_directories(csv13-lib/lib/${PLATFORM})
link_libraries(gtestd gtest_maind)
list(REMOVE_ITEM ASSIGNMENT_SOURCES "src/main.cc")
add_executable(${EXEC_NAME}_GTest src/${SOURCE_PREFIX}_unittest.cc ${ASSIGNMENT_SOURCES})

if(UNIX AND NOT DARWIN)
target_compile_options(${EXEC_NAME}_GTest PRIVATE -D_GLIBCXX_USE_CXX11_ABI=0)
target_link_libraries(${EXEC_NAME}_GTest -no-pie)
endif()
