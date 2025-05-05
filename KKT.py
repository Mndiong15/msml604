#!/usr/bin/env python3
import time
import os
import numpy as np
import matplotlib.pyplot as plt

def project_to_simplex(y, s):
    """
    Projects y onto the simplex {x | sum(x)=s, x>=0}
    Reference: Wang & Carreira-Perpiñán (2013)
    """
    n = y.size
    u = np.sort(y)[::-1]
    css = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, n+1) > (css - s))[0][-1]
    theta = (css[rho] - s) / (rho + 1)
    return np.maximum(y - theta, 0)

if __name__ == "__main__":
    # —— 参数设置
    lam0   = 0.1       # 基础惩罚强度
    eps    = 1e-6      # 防止除以零
    W = H  = 784
    ssp    = 8
    n_min  = 1
    Npix   = W * H
    Ntotal = Npix * ssp
    budget = Ntotal - Npix * n_min

    # —— 读取方差
    v = np.loadtxt('variance.txt').ravel()
    if v.size != Npix:
        raise ValueError(f"variance.txt 长度应为 {Npix}, 实际 {v.size}")

    # —— 差异化惩罚系数 λ_i
    lam_i = lam0 * (v.mean() / (v + eps))

    # —— 定义 KKT 解的 m_i 闭式：m_i = max( sqrt(v_i/(lam_i - γ)) - 1, 0 )
    def compute_sum_m(gamma):
        denom = lam_i - gamma
        valid = denom > 0
        m = np.zeros_like(v)
        m_valid = np.sqrt(v[valid] / denom[valid]) - 1
        m[valid] = np.maximum(m_valid, 0.0)
        return m.sum()

    # —— 二分法求 γ
    low, high = -1e3, lam_i.min() - 1e-12
    if compute_sum_m(low) > budget:
        raise RuntimeError("预算太小")
    if compute_sum_m(high) < budget:
        raise RuntimeError("预算太大")

    start_root = time.time()
    for _ in range(60):
        mid = (low + high) / 2
        s = compute_sum_m(mid)
        if s > budget:
            high = mid
        else:
            low = mid
    gamma = (low + high) / 2
    print(f"KKT solve time: {time.time() - start_root:.3f}s, γ = {gamma:.6e}")

    # —— 计算最终 m 和 n
    denom = lam_i - gamma
    m = np.zeros_like(v)
    valid = denom > 0
    m_valid = np.sqrt(v[valid] / denom[valid]) - 1
    m[valid] = np.maximum(m_valid, 0.0)
    n = m + n_min

    # —— 四舍五入取整
    floors = np.floor(n)
    remainders = n - floors
    k = int(Ntotal - floors.sum())
    idx = np.argsort(-remainders)
    n_int = floors.astype(int)
    n_int[idx[:k]] += 1

    # —— 调试输出
    print("n_int shape:", n_int.shape)
    print("sum(n_int):", n_int.sum())
    print("min(n_int), max(n_int):", n_int.min(), n_int.max())
    unique, counts = np.unique(n_int, return_counts=True)
    print("unique n_int values & counts (前10):", list(zip(unique, counts))[:10])

    # —— 保存结果
    out_file = 'optimal_n_kkt.txt'
    np.savetxt(out_file, n_int, fmt='%d')
    print(f"完成！已生成 {out_file}, 前五个值: {n_int[:5]}")

    # —— 绘制直方图，x 轴限制在 [1, 100]
    plt.figure()
    plt.hist(n_int, bins=50, range=(1, 100))
    plt.xlim(1, 100)
    plt.xlabel('Sample Allocation n_i')
    plt.ylabel('Number of Pixels')
    plt.title('Histogram of Sample Allocation per Pixel')
    plt.tight_layout()
    plt.show()