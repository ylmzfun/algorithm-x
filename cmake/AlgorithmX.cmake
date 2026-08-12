# 项目通用的 CMake 辅助模块。
# 用法：在根 CMakeLists.txt 中 include(cmake/AlgorithmX.cmake)。

include(GoogleTest)  # gtest_discover_tests

# 对目标应用统一的编译警告（GCC / Clang）。
function(algorithm_x_apply_warnings target)
    if(MSVC)
        target_compile_options(${target} PRIVATE /W4 /permissive-)
    else()
        target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic)
    endif()
endfunction()

# 注册一个 gtest 测试套件。
# 用法：algorithm_x_add_test_suite(<target> <src1> <src2> ...)
# 通过 gtest_discover_tests 把每个 TEST 注册进 CTest（粒度到单个用例）。
function(algorithm_x_add_test_suite target)
    add_executable(${target} ${ARGN})
    target_link_libraries(${target} PRIVATE algorithm_x GTest::gtest GTest::gtest_main)
    algorithm_x_apply_warnings(${target})
    gtest_discover_tests(${target}
        DISCOVERY_TIMEOUT 60
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})
endfunction()
