# 示例程序 —— 对应 README 第 13 章「C/C++ 工程与性能」。
# 分组：关键知识 / 核心库（标准库）/ 优秀第三方库 / 综合使用案例。
# 第三方库示例依赖 vcpkg（fmt / spdlog / nlohmann-json / eigen3）。

# ---- C/C++ 关键知识（纯标准库）----
add_executable(ex_value_categories key_knowledge/value_categories.cpp)
add_executable(ex_raii_lifetime key_knowledge/raii_lifetime.cpp)
add_executable(ex_memory_layout key_knowledge/memory_layout.cpp)
add_executable(ex_modern_cpp20 key_knowledge/modern_cpp20.cpp)

# ---- 核心库（标准库全景）----
add_executable(ex_std_containers std_library/containers.cpp)
add_executable(ex_std_algorithms std_library/algorithms.cpp)
add_executable(ex_std_strings std_library/strings.cpp)
add_executable(ex_std_concurrency std_library/concurrency.cpp)
add_executable(ex_std_chrono_random std_library/chrono_random.cpp)

# ---- 优秀第三方库（vcpkg 安装，见根目录 CMake 配置）----
find_package(fmt CONFIG REQUIRED)
find_package(spdlog CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)
find_package(Eigen3 CONFIG REQUIRED)

add_executable(ex_fmt_spdlog third_party/fmt_spdlog.cpp)
target_link_libraries(ex_fmt_spdlog PRIVATE fmt::fmt spdlog::spdlog)

add_executable(ex_json_config third_party/json_config.cpp)
target_link_libraries(ex_json_config PRIVATE nlohmann_json::nlohmann_json)

add_executable(ex_eigen_math third_party/eigen_math.cpp)
target_link_libraries(ex_eigen_math PRIVATE Eigen3::Eigen)

# ---- 综合使用案例 ----
add_executable(ex_full_stack_demo third_party/full_stack_demo.cpp)
target_link_libraries(ex_full_stack_demo PRIVATE
    fmt::fmt spdlog::spdlog nlohmann_json::nlohmann_json Eigen3::Eigen)
