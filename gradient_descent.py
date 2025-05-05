#!/usr/bin/env python3
import time
import os
import numpy as np

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

    # —— 差异化惩罚系数
    lam_i = lam0 * (v.mean() / (v + eps))

    # —— 初始化 m = n - n_min
    m = np.full(Npix, budget / Npix)

    # —— 投影梯度下降（计时）
    lr, max_iter = 1.0, 1000
    start_time = time.time()
    for it in range(max_iter):
        grad = -v / (m + n_min)**2 + lam_i
        m -= lr * grad
        m = project_to_simplex(m, budget)
    end_time = time.time()
    print(f"Optimization time: {end_time - start_time:.2f} seconds")

    # —— 合成 n
    n = m + n_min

    # —— 四舍五入取整 (largest‐remainder 方法，保持 sum(n_int)==Ntotal)
    floors = np.floor(n)
    remainders = n - floors
    k = int(Ntotal - floors.sum())
    idx = np.argsort(-remainders)
    n_int = floors.astype(int)
    n_int[idx[:k]] += 1

    # —— 验证和并保存
    assert n_int.sum() == Ntotal, "Sum constraint violated!"
    out_file = 'optimal_n_diff_penalty_int.txt'
    np.savetxt(out_file, n_int, fmt='%d')
    print(f"完成！已生成 {out_file}, sum = {n_int.sum()}, 前五个值: {n_int[:5]}")