cmake_minimum_required(VERSION 3.20)
project(algorithm_x VERSION 0.1.0 LANGUAGES CXX C)

set(CMAKE_C_STANDARD 17)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Sanitizers for debug builds
option(ENABLE_ASAN "Enable AddressSanitizer" ON)
option(ENABLE_UBSAN "Enable UndefinedBehaviorSanitizer" ON)

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    if(ENABLE_ASAN)
        add_compile_options(-fsanitize=address -fno-omit-frame-pointer)
        add_link_options(-fsanitize=address)
    endif()
    if(ENABLE_UBSAN)
        add_compile_options(-fsanitize=undefined)
        add_link_options(-fsanitize=undefined)
    endif()
endif()

# Common compile options
add_compile_options(-Wall -Wextra -Wpedantic)

# Google Test (system install via Homebrew)
find_package(GTest REQUIRED)

enable_testing()

# Library target
add_library(algorithm_x INTERFACE)
target_include_directories(algorithm_x INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/include)

# Subdirectories
add_subdirectory(tests)
add_subdirectory(examples)
