
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_HOME_DIRECTORY}/bin/)

file(GLOB_RECURSE ASSIGNMENT_SOURCES RELATIVE ${CMAKE_SOURCE_DIR} "src/*.cc")
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

if(WIN32) 
add_custom_command(OUTPUT ${CMAKE_HOME_DIRECTORY}/.git/hooks/pre-push COMMAND copy ARGS \"githooks\\pre-push\" \".git\\hooks\" WORKING_DIRECTORY ${CMAKE_HOME_DIRECTORY})
add_custom_command(OUTPUT ${CMAKE_HOME_DIRECTORY}/.git/hooks/pre-commit COMMAND copy ARGS \"githooks\\pre-commit\" \".git\\hooks\" WORKING_DIRECTORY ${CMAKE_HOME_DIRECTORY})
add_custom_command(OUTPUT ${CMAKE_HOME_DIRECTORY}/.git/hooks/project.py COMMAND copy ARGS \".githooks\\project.py\" \".git\\hooks\" WORKING_DIRECTORY ${CMAKE_HOME_DIRECTORY})
add_custom_target(requests OUTPUT ${CMAKE_HOME_DIRECTORY}/.git/hooks/requests COMMAND xcopy ARGS \"githooks\\requests\" \".git\\hooks\\requests\" /i /y /q /E /H /K WORKING_DIRECTORY ${CMAKE_HOME_DIRECTORY})
else()
add_custom_command(OUTPUT ${CMAKE_HOME_DIRECTORY}/.git/hooks/pre-push COMMAND cp ARGS githooks/pre-push .git/hooks WORKING_DIRECTORY ${CMAKE_HOME_DIRECTORY})
add_custom_command(OUTPUT ${CMAKE_HOME_DIRECTORY}/.git/hooks/pre-commit COMMAND cp ARGS githooks/pre-commit .git/hooks WORKING_DIRECTORY ${CMAKE_HOME_DIRECTORY})
add_custom_command(OUTPUT ${CMAKE_HOME_DIRECTORY}/.git/hooks/project.py COMMAND cp ARGS .githooks/project.py .git/hooks WORKING_DIRECTORY ${CMAKE_HOME_DIRECTORY})
add_custom_target(requests OUTPUT ${CMAKE_HOME_DIRECTORY}/.git/hooks/requests COMMAND cp ARGS -R githooks/requests .git/hooks WORKING_DIRECTORY ${CMAKE_HOME_DIRECTORY})
endif()

add_custom_target(sync-the-fork COMMAND csv13-lib/scripts/syncthefork.py WORKING_DIRECTORY ${CMAKE_HOME_DIRECTORY})
add_custom_target(update-submodules COMMAND csv13-lib/scripts/updatesubmodules.py WORKING_DIRECTORY ${CMAKE_HOME_DIRECTORY})
add_custom_target(pre-push-script ALL DEPENDS ${CMAKE_HOME_DIRECTORY}/.git/hooks/pre-push)
add_custom_target(pre-commit-script ALL DEPENDS ${CMAKE_HOME_DIRECTORY}/.git/hooks/pre-commit)
add_custom_target(project-config ALL DEPENDS ${CMAKE_HOME_DIRECTORY}/.git/hooks/project.py)

add_dependencies(${EXEC_NAME}_GTest pre-push-script pre-commit-script project-config)
add_dependencies(${EXEC_NAME} pre-push-script pre-commit-script project-config)
