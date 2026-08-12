cmake_minimum_required(VERSION 3.20)

project(algorithm_x
    VERSION 1.3.0
    DESCRIPTION "C/C++ algorithm learning repository (header-only)"
    HOMEPAGE_URL "https://github.com/ylmzfun/algorithm-cc"
    LANGUAGES C CXX)

# ---- 构建选项 ----
option(BUILD_TESTS    "构建单元测试（依赖 GTest，由 vcpkg 提供）" ON)
option(BUILD_EXAMPLES "构建示例程序（依赖 fmt/spdlog/nlohmann-json/eigen3）" ON)
option(ALGORITHM_X_ENABLE_SANITIZERS "Debug 构建启用 ASan/UBSan" ON)

# ---- 语言标准 ----
set(CMAKE_C_STANDARD 17)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# ---- Sanitizers（仅 Debug 构建）----
if(ALGORITHM_X_ENABLE_SANITIZERS AND CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_compile_options(-fsanitize=address,undefined -fno-omit-frame-pointer)
    add_link_options(-fsanitize=address,undefined)
endif()

include(cmake/AlgorithmX.cmake)

# ---- 核心库（header-only INTERFACE 库）----
add_library(algorithm_x INTERFACE)
add_library(algorithm_x::algorithm_x ALIAS algorithm_x)
target_include_directories(algorithm_x INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)
target_compile_features(algorithm_x INTERFACE cxx_std_20)

# ---- 安装 / 导出：支持 find_package(algorithm_x) ----
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

install(TARGETS algorithm_x EXPORT algorithm_xTargets)
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    FILES_MATCHING PATTERN "*.h")
install(EXPORT algorithm_xTargets
    FILE algorithm_xTargets.cmake
    NAMESPACE algorithm_x::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/algorithm_x)

write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/algorithm_xConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion)

configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/algorithm_xConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/algorithm_xConfig.cmake"
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/algorithm_x)

install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/algorithm_xConfig.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/algorithm_xConfigVersion.cmake"
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/algorithm_x)

# ---- 测试 / 示例 ----
enable_testing()
if(BUILD_TESTS)
    add_subdirectory(tests)
endif()
if(BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
