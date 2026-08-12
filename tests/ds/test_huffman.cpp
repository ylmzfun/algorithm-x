#include "ds/huffman.h"
#include <string>
#include "gtest/gtest.h"
using namespace algorithm_x::ds;
namespace {
TEST(Huffman, EncodeDecode) {
    HuffmanCoding hc; hc.build("aababcabcd");
    std::string text = "aababcabcd";
    auto encoded = hc.encode(text);
    auto decoded = hc.decode(encoded);
    EXPECT_EQ(decoded, text);
}
TEST(Huffman, SingleChar) {
    HuffmanCoding hc; hc.build("aaaa");
    auto enc = hc.encode("aaaa");
    EXPECT_EQ(hc.decode(enc), "aaaa");
}
}  // namespace
