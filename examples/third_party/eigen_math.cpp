#include <Eigen/Dense>
#include <iostream>

// 第三方库示例 —— Eigen 线性代数。
// 依赖：vcpkg install eigen3
int main() {
    std::cout << "== 矩阵构造（逗号初始化）==\n";
    Eigen::MatrixXd A(2, 2);
    A << 3, 1,
         1, 2;
    std::cout << "  A =\n" << A << "\n";

    std::cout << "== 解线性方程组 A·x = b ==\n";
    Eigen::VectorXd b(2);
    b << 9, 8;
    Eigen::VectorXd x = A.colPivHouseholderQr().solve(b);
    std::cout << "  x = " << x.transpose() << "\n";
    std::cout << "  验证 A·x = " << (A * x).transpose() << "\n";

    std::cout << "== 特征值（对称矩阵）==\n";
    Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> es(A);
    std::cout << "  特征值 = " << es.eigenvalues().transpose() << "\n";
    return 0;
}
