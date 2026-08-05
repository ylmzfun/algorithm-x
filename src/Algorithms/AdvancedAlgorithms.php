<?php

namespace DataStructures\Algorithms;

/**
 * AdvancedAlgorithms - 高级启发式优化算法集合
 *
 * 包含：
 * - 模拟退火 (Simulated Annealing)
 * - 遗传算法 (Genetic Algorithm)
 * - 粒子群优化 (Particle Swarm Optimization)
 * - 简单神经网络 (Simple Neural Network)
 */
class AdvancedAlgorithms
{
    // ==================== 模拟退火 ====================

    /**
     * 模拟退火算法
     *
     * 模拟物理退火过程，以一定概率接受更差的解来跳出局部最优。
     *
     * 业务场景：
     * 1. 集成电路布局布线
     * 2. 物流路径规划 (VRP)
     * 3. 任务调度优化
     * 4. 图像分割
     *
     * @param callable $initialState 返回初始解的函数
     * @param callable $energy 能量函数 f(state) => float (越小越好)
     * @param callable $neighbor 邻域生成 f(state) => newState
     * @param float $T0 初始温度
     * @param float $Tmin 最低温度
     * @param float $alpha 降温系数 (0.8~0.99)
     * @param int $iterPerT 每个温度下的迭代次数
     * @return array ['state' => bestState, 'energy' => bestEnergy]
     */
    public static function simulatedAnnealing(
        callable $initialState,
        callable $energy,
        callable $neighbor,
        float $T0 = 1000.0,
        float $Tmin = 0.001,
        float $alpha = 0.95,
        int $iterPerT = 100
    ): array {
        $state = $initialState();
        $bestState = $state;
        $currentEnergy = $energy($state);
        $bestEnergy = $currentEnergy;

        $T = $T0;
        while ($T > $Tmin) {
            for ($i = 0; $i < $iterPerT; $i++) {
                $newState = $neighbor($state);
                $newEnergy = $energy($newState);
                $delta = $newEnergy - $currentEnergy;

                if ($delta < 0 || exp(-$delta / $T) > mt_rand() / mt_getrandmax()) {
                    $state = $newState;
                    $currentEnergy = $newEnergy;

                    if ($currentEnergy < $bestEnergy) {
                        $bestState = $state;
                        $bestEnergy = $currentEnergy;
                    }
                }
            }
            $T *= $alpha;
        }

        return ['state' => $bestState, 'energy' => $bestEnergy];
    }

    // ==================== 遗传算法 ====================

    /**
     * 遗传算法
     *
     * 业务场景：
     * 1. 特征选择
     * 2. 神经网络结构搜索
     * 3. 调度优化
     * 4. 投资组合优化
     *
     * @param int $popSize 种群大小
     * @param int $geneLength 基因长度
     * @param callable $fitness 适应度函数 f(gene[]) => float
     * @param int $generations 代数
     * @param float $crossoverRate 交叉率
     * @param float $mutationRate 变异率
     * @return array ['bestGene' => [], 'bestFitness' => float, 'history' => []]
     */
    public static function geneticAlgorithm(
        int $popSize,
        int $geneLength,
        callable $fitness,
        int $generations = 100,
        float $crossoverRate = 0.8,
        float $mutationRate = 0.01
    ): array {
        // 初始化种群（随机二进制基因）
        $population = [];
        for ($i = 0; $i < $popSize; $i++) {
            $gene = [];
            for ($j = 0; $j < $geneLength; $j++) {
                $gene[$j] = random_int(0, 1);
            }
            $population[] = $gene;
        }

        $bestGene = null;
        $bestFitness = PHP_FLOAT_MIN;
        $history = [];

        for ($gen = 0; $gen < $generations; $gen++) {
            // 计算适应度
            $fitnesses = [];
            foreach ($population as $i => $gene) {
                $f = $fitness($gene);
                $fitnesses[$i] = $f;
                if ($f > $bestFitness) {
                    $bestFitness = $f;
                    $bestGene = $gene;
                }
            }
            $history[] = $bestFitness;

            // 锦标赛选择
            $newPopulation = [];
            while (count($newPopulation) < $popSize) {
                $parent1 = self::tournamentSelect($population, $fitnesses);
                $parent2 = self::tournamentSelect($population, $fitnesses);

                // 交叉
                if (mt_rand() / mt_getrandmax() < $crossoverRate) {
                    $crossoverPoint = random_int(1, $geneLength - 1);
                    $child1 = array_merge(
                        array_slice($parent1, 0, $crossoverPoint),
                        array_slice($parent2, $crossoverPoint)
                    );
                    $child2 = array_merge(
                        array_slice($parent2, 0, $crossoverPoint),
                        array_slice($parent1, $crossoverPoint)
                    );
                } else {
                    $child1 = $parent1;
                    $child2 = $parent2;
                }

                // 变异
                for ($j = 0; $j < $geneLength; $j++) {
                    if (mt_rand() / mt_getrandmax() < $mutationRate) {
                        $child1[$j] = 1 - $child1[$j];
                    }
                    if (mt_rand() / mt_getrandmax() < $mutationRate) {
                        $child2[$j] = 1 - $child2[$j];
                    }
                }

                $newPopulation[] = $child1;
                if (count($newPopulation) < $popSize) {
                    $newPopulation[] = $child2;
                }
            }

            $population = $newPopulation;
        }

        return [
            'bestGene' => $bestGene,
            'bestFitness' => $bestFitness,
            'history' => $history,
        ];
    }

    private static function tournamentSelect(array $population, array $fitnesses, int $tournamentSize = 3): array
    {
        $bestIdx = null;
        $bestFit = PHP_FLOAT_MIN;

        for ($i = 0; $i < $tournamentSize; $i++) {
            $idx = random_int(0, count($population) - 1);
            if ($fitnesses[$idx] > $bestFit) {
                $bestFit = $fitnesses[$idx];
                $bestIdx = $idx;
            }
        }

        return $population[$bestIdx];
    }

    // ==================== 粒子群优化 ====================

    /**
     * 粒子群优化算法 (PSO)
     *
     * 业务场景：
     * 1. 神经网络权重优化
     * 2. 函数极值求解
     * 3. 天线阵列设计
     * 4. 电力系统优化
     *
     * @param int $numParticles 粒子数
     * @param int $dimensions 维度
     * @param callable $objective 目标函数 f(position[]) => float（求最小值）
     * @param array $bounds 每维的边界 [[min, max], [min, max], ...]
     * @param int $iterations 迭代次数
     * @return array ['position' => [], 'value' => float, 'history' => []]
     */
    public static function particleSwarmOptimization(
        int $numParticles,
        int $dimensions,
        callable $objective,
        array $bounds,
        int $iterations = 100
    ): array {
        $w = 0.7;   // 惯性权重
        $c1 = 1.5;  // 认知系数
        $c2 = 1.5;  // 社会系数

        // 初始化粒子
        $positions = [];
        $velocities = [];
        $personalBestPos = [];
        $personalBestVal = [];

        $globalBestPos = [];
        $globalBestVal = PHP_FLOAT_MAX;

        for ($i = 0; $i < $numParticles; $i++) {
            for ($d = 0; $d < $dimensions; $d++) {
                $lo = $bounds[$d][0];
                $hi = $bounds[$d][1];
                $positions[$i][$d] = $lo + mt_rand() / mt_getrandmax() * ($hi - $lo);
                $velocities[$i][$d] = (mt_rand() / mt_getrandmax() - 0.5) * ($hi - $lo) * 0.1;
            }

            $val = $objective($positions[$i]);
            $personalBestPos[$i] = $positions[$i];
            $personalBestVal[$i] = $val;

            if ($val < $globalBestVal) {
                $globalBestVal = $val;
                $globalBestPos = $positions[$i];
            }
        }

        $history = [$globalBestVal];

        for ($iter = 0; $iter < $iterations; $iter++) {
            for ($i = 0; $i < $numParticles; $i++) {
                for ($d = 0; $d < $dimensions; $d++) {
                    $r1 = mt_rand() / mt_getrandmax();
                    $r2 = mt_rand() / mt_getrandmax();

                    $velocities[$i][$d] = $w * $velocities[$i][$d]
                        + $c1 * $r1 * ($personalBestPos[$i][$d] - $positions[$i][$d])
                        + $c2 * $r2 * ($globalBestPos[$d] - $positions[$i][$d]);

                    // 边界约束
                    $lo = $bounds[$d][0];
                    $hi = $bounds[$d][1];
                    $velocities[$i][$d] = max(-($hi - $lo) * 0.2, min(($hi - $lo) * 0.2, $velocities[$i][$d]));

                    $positions[$i][$d] += $velocities[$i][$d];
                    $positions[$i][$d] = max($lo, min($hi, $positions[$i][$d]));
                }

                $val = $objective($positions[$i]);

                if ($val < $personalBestVal[$i]) {
                    $personalBestVal[$i] = $val;
                    $personalBestPos[$i] = $positions[$i];

                    if ($val < $globalBestVal) {
                        $globalBestVal = $val;
                        $globalBestPos = $positions[$i];
                    }
                }
            }

            $history[] = $globalBestVal;
        }

        return [
            'position' => $globalBestPos,
            'value' => $globalBestVal,
            'history' => $history,
        ];
    }

    // ==================== 简单神经网络 ====================

    /**
     * 前馈神经网络（单隐藏层）
     *
     * 使用随机梯度下降训练，适用于二分类或回归问题。
     *
     * 业务场景：
     * 1. 简单分类任务
     * 2. 函数逼近
     * 3. 模式识别入门
     *
     * @param array $X 输入数据 [sample][feature]
     * @param array $y 标签 [sample]（二分类：0或1，回归：连续值）
     * @param int $hiddenSize 隐藏层神经元数
     * @param float $learningRate
     * @param int $epochs
     * @return NeuralNetwork
     */
    public static function createNeuralNetwork(
        array $X,
        array $y,
        int $hiddenSize = 10,
        float $learningRate = 0.01,
        int $epochs = 1000
    ): NeuralNetwork {
        $nn = new NeuralNetwork($hiddenSize, $learningRate);
        $nn->train($X, $y, $epochs);
        return $nn;
    }
}

/**
 * 简单前馈神经网络
 */
class NeuralNetwork
{
    private int $inputSize;
    private int $hiddenSize;
    private float $learningRate;
    private array $W1;
    private array $b1;
    private array $W2;
    private array $b2;

    public function __construct(int $hiddenSize, float $learningRate)
    {
        $this->hiddenSize = $hiddenSize;
        $this->learningRate = $learningRate;
    }

    private function sigmoid(float $x): float
    {
        return 1.0 / (1.0 + exp(-$x));
    }

    private function sigmoidDerivative(float $x): float
    {
        return $x * (1.0 - $x);
    }

    public function train(array $X, array $y, int $epochs): void
    {
        $this->inputSize = count($X[0]);
        $samples = count($X);

        // Xavier 初始化
        $scale1 = sqrt(2.0 / $this->inputSize);
        $scale2 = sqrt(1.0 / $this->hiddenSize);

        for ($i = 0; $i < $this->inputSize; $i++) {
            for ($j = 0; $j < $this->hiddenSize; $j++) {
                $this->W1[$i][$j] = (mt_rand() / mt_getrandmax() * 2 - 1) * $scale1;
            }
        }
        for ($j = 0; $j < $this->hiddenSize; $j++) {
            $this->b1[$j] = 0;
            $this->W2[$j] = (mt_rand() / mt_getrandmax() * 2 - 1) * $scale2;
        }
        $this->b2 = 0;

        for ($epoch = 0; $epoch < $epochs; $epoch++) {
            $totalLoss = 0;

            for ($s = 0; $s < $samples; $s++) {
                // Forward pass
                $z1 = [];
                $a1 = [];
                for ($j = 0; $j < $this->hiddenSize; $j++) {
                    $z1[$j] = $this->b1[$j];
                    for ($i = 0; $i < $this->inputSize; $i++) {
                        $z1[$j] += $X[$s][$i] * $this->W1[$i][$j];
                    }
                    $a1[$j] = $this->sigmoid($z1[$j]);
                }

                $z2 = $this->b2;
                for ($j = 0; $j < $this->hiddenSize; $j++) {
                    $z2 += $a1[$j] * $this->W2[$j];
                }
                $a2 = $this->sigmoid($z2);
                $output = $a2;

                // Loss (MSE)
                $error = $y[$s] - $output;
                $totalLoss += $error * $error;

                // Backward pass
                $delta2 = $error * $this->sigmoidDerivative($output);

                $delta1 = [];
                for ($j = 0; $j < $this->hiddenSize; $j++) {
                    $delta1[$j] = $delta2 * $this->W2[$j] * $this->sigmoidDerivative($a1[$j]);
                }

                // Update weights
                for ($j = 0; $j < $this->hiddenSize; $j++) {
                    $this->W2[$j] += $this->learningRate * $delta2 * $a1[$j];
                    for ($i = 0; $i < $this->inputSize; $i++) {
                        $this->W1[$i][$j] += $this->learningRate * $delta1[$j] * $X[$s][$i];
                    }
                    $this->b1[$j] += $this->learningRate * $delta1[$j];
                }
                $this->b2 += $this->learningRate * $delta2;
            }
        }
    }

    /**
     * 预测单个样本
     */
    public function predict(array $x): float
    {
        $z1 = [];
        $a1 = [];
        for ($j = 0; $j < $this->hiddenSize; $j++) {
            $z1[$j] = $this->b1[$j];
            for ($i = 0; $i < $this->inputSize; $i++) {
                $z1[$j] += $x[$i] * $this->W1[$i][$j];
            }
            $a1[$j] = $this->sigmoid($z1[$j]);
        }

        $z2 = $this->b2;
        for ($j = 0; $j < $this->hiddenSize; $j++) {
            $z2 += $a1[$j] * $this->W2[$j];
        }

        return $this->sigmoid($z2);
    }

    /**
     * 批量预测
     */
    public function predictBatch(array $X): array
    {
        return array_map([$this, 'predict'], $X);
    }
}
