# 单元测试：每个模块一个套件。
# algorithm_x_add_test_suite 由 cmake/AlgorithmX.cmake 提供，
# 自动处理链接、警告与 CTest 注册（gtest_discover_tests，粒度到单个 TEST）。

find_package(GTest REQUIRED)  # 由 vcpkg 提供

algorithm_x_add_test_suite(test_ds
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
    ds/test_adjacency_matrix.cpp
    ds/test_forward_star.cpp
)

algorithm_x_add_test_suite(test_algo
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
    algo/test_branch_and_bound.cpp
    algo/test_decrease_conquer.cpp
    algo/test_approximation.cpp
)

algorithm_x_add_test_suite(test_graph
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

algorithm_x_add_test_suite(test_string
    string/test_string_match.cpp
    string/test_manacher.cpp
    string/test_aho_corasick.cpp
    string/test_edit_distance.cpp
    string/test_boyer_moore.cpp
    string/test_suffix_array.cpp
    string/test_sam.cpp
    string/test_min_representation.cpp
)

algorithm_x_add_test_suite(test_math
    math/test_prime.cpp
    math/test_modint.cpp
    math/test_matrix.cpp
    math/test_game_theory.cpp
    math/test_fft.cpp
    math/test_combinatorics.cpp
    math/test_linear_algebra.cpp
    math/test_principles.cpp
    math/test_stirling.cpp
    math/test_probability.cpp
    math/test_generating_function.cpp
)

algorithm_x_add_test_suite(test_geom
    geom/test_point.cpp
    geom/test_convex_hull.cpp
    geom/test_intersection.cpp
    geom/test_sweep_line.cpp
    geom/test_half_plane.cpp
)

algorithm_x_add_test_suite(test_dp
    dp/test_knapsack.cpp
    dp/test_lis.cpp
    dp/test_common.cpp
    dp/test_advanced_dp.cpp
    dp/test_optimization.cpp
    dp/test_probability_dp.cpp
    dp/test_quadrangle.cpp
    dp/test_slope_opt.cpp
    dp/test_plug_dp.cpp
    dp/test_ds_opt_dp.cpp
)

algorithm_x_add_test_suite(test_ai
    ai/test_search.cpp
    ai/test_evolution.cpp
    ai/test_ml.cpp
    ai/test_more_ai.cpp
    ai/test_rl.cpp
    ai/test_naive_bayes.cpp
    ai/test_decision_tree.cpp
    ai/test_minimax.cpp
    ai/test_mdp.cpp
    ai/test_rl_advanced.cpp
    ai/test_differential_evolution.cpp
    ai/test_csp.cpp
)

algorithm_x_add_test_suite(test_concurrent
    concurrent/test_thread_pool.cpp
    concurrent/test_lock_free_queue.cpp
    concurrent/test_sync.cpp
    concurrent/test_lock_free_stack.cpp
    concurrent/test_dining.cpp
    concurrent/test_concurrent_hash_table.cpp
    concurrent/test_rcu.cpp
)

algorithm_x_add_test_suite(test_distributed
    distributed/test_consistent_hash.cpp
    distributed/test_distributed_lock.cpp
    distributed/test_gossip.cpp
    distributed/test_vector_clock.cpp
    distributed/test_consensus.cpp
    distributed/test_two_phase_commit.cpp
    distributed/test_map_reduce.cpp
    distributed/test_crdt.cpp
)

algorithm_x_add_test_suite(test_advanced
    advanced/test_rmq_lca.cpp
    advanced/test_mo_algorithm.cpp
    advanced/test_persistent.cpp
    advanced/test_inversions.cpp
    advanced/test_cdq.cpp
    advanced/test_amortized.cpp
    advanced/test_link_cut_tree.cpp
    advanced/test_tree_in_tree.cpp
    advanced/test_complexity.cpp
    advanced/test_online_algorithm.cpp
)

algorithm_x_add_test_suite(test_perf
    perf/test_cache.cpp
    perf/test_memory_pool.cpp
    perf/test_concepts.cpp
)
