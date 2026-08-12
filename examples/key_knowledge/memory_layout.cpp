#include <cstdint>
#include <cstring>
#include <iostream>
#include <memory>

// C/C++ 关键知识示例 —— 内存模型：存储区、对齐、字节序。
// 对应 README 第 13 章「C/C++ 关键知识 · 内存模型」。
namespace {

struct Aligned16 {
    alignas(16) char buf[8];
};

}  // namespace

int main() {
    std::cout << "== 存储区（地址通常满足：静态 < 堆 < 栈）==\n";
    static int g_static = 42;                  // 静态存储期，程序启动时分配
    int g_stack = 7;                           // 栈（自动存储期）
    auto g_heap = std::make_unique<int>(99);   // 堆（new / malloc）
    std::cout << "  static @ " << static_cast<const void*>(&g_static) << "\n"
              << "  stack  @ " << static_cast<const void*>(&g_stack) << "\n"
              << "  heap   @ " << static_cast<const void*>(g_heap.get()) << "\n";

    std::cout << "== 对齐（alignof）==\n";
    std::cout << "  alignof(int)=" << alignof(int)
              << " alignof(double)=" << alignof(double)
              << " alignof(Aligned16)=" << alignof(Aligned16) << "\n";

    std::cout << "== 字节序（0x0102 的首字节）==\n";
    std::uint16_t v = 0x0102;
    std::uint8_t bytes[2];
    std::memcpy(bytes, &v, sizeof(v));
    std::cout << "  byte0=0x" << std::hex << static_cast<int>(bytes[0])
              << " byte1=0x" << static_cast<int>(bytes[1]) << std::dec
              << (bytes[0] == 0x02 ? " (little-endian)" : " (big-endian)") << "\n";
    return 0;
}
