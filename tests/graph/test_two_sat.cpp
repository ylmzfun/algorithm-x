#include "graph/two_sat.h"
#include "gtest/gtest.h"
using namespace algorithm_x::graph;
namespace {
TEST(TwoSAT, Sat) { TwoSAT ts(2); ts.add_clause(0,false,1,true); EXPECT_TRUE(ts.solve().size()>0); }
TEST(TwoSAT, Unsat) { TwoSAT ts(1); ts.add_clause(0,false,0,false); ts.add_clause(0,true,0,true); EXPECT_TRUE(ts.solve().empty()); }
}  // namespace
