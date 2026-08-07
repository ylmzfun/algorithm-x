add_executable(test_ds
    ds/test_dynamic_array.cpp
    ds/test_linked_list.cpp
    ds/test_stack.cpp
    ds/test_queue.cpp
    ds/test_priority_queue.cpp
    ds/test_binary_tree.cpp
    ds/test_avl_tree.cpp
    ds/test_binary_heap.cpp
    ds/test_segment_tree.cpp
    ds/test_trie.cpp
    ds/test_union_find.cpp
    ds/test_hash_table.cpp
    ds/test_lru_cache.cpp
    ds/test_graph.cpp
    ds/test_fenwick_tree.cpp
    ds/test_skip_list.cpp
    ds/test_huffman.cpp
    ds/test_bloom_filter.cpp
    ds/test_b_tree.cpp
    ds/test_red_black_tree.cpp
    ds/test_fibonacci_heap.cpp
    ds/test_lfu_cache.cpp
)
target_link_libraries(test_ds PRIVATE algorithm_x GTest::gtest GTest::gtest_main)
add_test(NAME ds COMMAND test_ds)

add_executable(test_algo
    algo/test_sort.cpp
    algo/test_search.cpp
    algo/test_two_pointers.cpp
    algo/test_bit.cpp
    algo/test_divide_conquer.cpp
    algo/test_greedy.cpp
    algo/test_backtracking.cpp
    algo/test_randomized.cpp
    algo/test_more_algo.cpp
    algo/test_external_sort.cpp
    algo/test_interpolation_search.cpp
)
target_link_libraries(test_algo PRIVATE algorithm_x GTest::gtest GTest::gtest_main)
add_test(NAME algo COMMAND test_algo)

add_executable(test_graph
    graph/test_shortest_path.cpp
    graph/test_mst.cpp
    graph/test_connectivity.cpp
    graph/test_network_flow.cpp
    graph/test_euler.cpp
    graph/test_kosaraju.cpp
    graph/test_spfa.cpp
    graph/test_min_cut.cpp
    graph/test_johnson.cpp
    graph/test_two_sat.cpp
    graph/test_hamiltonian.cpp
    graph/test_biconnected.cpp
    graph/test_min_cost_flow.cpp
    graph/test_km.cpp
)
target_link_libraries(test_graph PRIVATE algorithm_x GTest::gtest GTest::gtest_main)
add_test(NAME graph COMMAND test_graph)

add_executable(test_string
    string/test_string_match.cpp
    string/test_manacher.cpp
    string/test_aho_corasick.cpp
    string/test_edit_distance.cpp
    string/test_boyer_moore.cpp
    string/test_suffix_array.cpp
    string/test_sam.cpp
    string/test_min_representation.cpp
)
target_link_libraries(test_string PRIVATE algorithm_x GTest::gtest GTest::gtest_main)
add_test(NAME string COMMAND test_string)

add_executable(test_math
    math/test_prime.cpp
    math/test_modint.cpp
    math/test_matrix.cpp
    math/test_game_theory.cpp
    math/test_fft.cpp
    math/test_combinatorics.cpp
    math/test_linear_algebra.cpp
)
target_link_libraries(test_math PRIVATE algorithm_x GTest::gtest GTest::gtest_main)
add_test(NAME math COMMAND test_math)

add_executable(test_geom
    geom/test_point.cpp
    geom/test_convex_hull.cpp
    geom/test_intersection.cpp
    geom/test_sweep_line.cpp
    
)
target_link_libraries(test_geom PRIVATE algorithm_x GTest::gtest GTest::gtest_main)
add_test(NAME geom COMMAND test_geom)

add_executable(test_dp
    dp/test_knapsack.cpp
    dp/test_lis.cpp
    dp/test_common.cpp
    dp/test_advanced_dp.cpp
    dp/test_optimization.cpp
    dp/test_probability_dp.cpp
    dp/test_quadrangle.cpp
)
target_link_libraries(test_dp PRIVATE algorithm_x GTest::gtest GTest::gtest_main)
add_test(NAME dp COMMAND test_dp)

add_executable(test_ai
    ai/test_search.cpp
    ai/test_evolution.cpp
    ai/test_ml.cpp
    ai/test_more_ai.cpp
    ai/test_rl.cpp
    ai/test_naive_bayes.cpp
    ai/test_decision_tree.cpp
    ai/test_minimax.cpp
)
target_link_libraries(test_ai PRIVATE algorithm_x GTest::gtest GTest::gtest_main)
add_test(NAME ai COMMAND test_ai)

add_executable(test_concurrent
    concurrent/test_thread_pool.cpp
    concurrent/test_lock_free_queue.cpp
    concurrent/test_sync.cpp
    concurrent/test_lock_free_stack.cpp
    concurrent/test_dining.cpp
    concurrent/test_concurrent_hash_table.cpp
)
target_link_libraries(test_concurrent PRIVATE algorithm_x GTest::gtest GTest::gtest_main)
add_test(NAME concurrent COMMAND test_concurrent)

add_executable(test_distributed
    distributed/test_consistent_hash.cpp
    
)
target_link_libraries(test_distributed PRIVATE algorithm_x GTest::gtest GTest::gtest_main)
add_test(NAME distributed COMMAND test_distributed)

add_executable(test_advanced
    advanced/test_rmq_lca.cpp
    advanced/test_mo_algorithm.cpp
    advanced/test_persistent.cpp
    advanced/test_inversions.cpp
    advanced/test_cdq.cpp
    advanced/test_amortized.cpp
)
target_link_libraries(test_advanced PRIVATE algorithm_x GTest::gtest GTest::gtest_main)
add_test(NAME advanced COMMAND test_advanced)

add_executable(test_perf
    perf/test_cache.cpp
    perf/test_memory_pool.cpp
)
target_link_libraries(test_perf PRIVATE algorithm_x GTest::gtest GTest::gtest_main)
add_test(NAME perf COMMAND test_perf)
