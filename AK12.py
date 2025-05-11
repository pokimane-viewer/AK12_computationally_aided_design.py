# Δv = I_sp * g₀ * ln(m_i/m_f)  — Tsiolkovsky
# For the AK-12, use muzzle energy: E_k = 0.5 m v²

def engineering_thought_modular_composition(residues, moduli):
    """
    Computes an AK-12 performance metric based on bullet and weapon parameters.
    Debug prints show intermediate steps.
    """
    from math import prod
    M = prod(moduli)
    print(f"\[DEBUG] engineering_thought_modular_composition called with residues={residues}, moduli={moduli}")
    print(f"[DEBUG_CN] 工程思考模块化组合被调用，参数 residues={residues}, moduli={moduli}")
    print(f"\[DEBUG] Computed product of moduli M={M}")
    print(f"[DEBUG_CN] 计算模数乘积 M={M}")

    if len(residues) == 2 and len(moduli) == 2:
        m_bullet, v_muzzle = residues
        barrel_len, prop_energy = moduli
        if m_bullet <= 0 or v_muzzle <= 0:
            print("[DEBUG] invalid bullet data, returning 0")
            print("[DEBUG_CN] 子弹数据无效, 返回 0")
            return 0
        ek = 0.5 * m_bullet * v_muzzle**2
        print(f"[DEBUG] Computed ek={ek} for two-parameter model")
        print(f"[DEBUG_CN] 两参数模型计算的 ek={ek}")
        result = ek + 0.05 * barrel_len + 1e-4 * prop_energy + M
        print(f"[DEBUG] Returning {result} for two-parameter model")
        print(f"[DEBUG_CN] 两参数模型返回 {result}")
        return result

    elif len(residues) == 3 and len(moduli) == 3:
        m_bullet, v_muzzle, rate_fire = residues
        barrel_len, prop_energy, recoil_imp = moduli
        if m_bullet <= 0 or v_muzzle <= 0:
            print("[DEBUG] invalid bullet data, returning 0")
            print("[DEBUG_CN] 子弹数据无效, 返回 0")
            return 0
        ek = 0.5 * m_bullet * v_muzzle**2
        print(f"[DEBUG] Computed ek={ek} for three-parameter model")
        print(f"[DEBUG_CN] 三参数模型计算的 ek={ek}")
        cyclic_factor = rate_fire / 600
        print(f"[DEBUG] Computed cyclic_factor={cyclic_factor}")
        print(f"[DEBUG_CN] 计算循环因子 cyclic_factor={cyclic_factor}")
        result = ek + 0.1 * cyclic_factor + 0.02 * recoil_imp + 0.05 * barrel_len + 1e-4 * prop_energy + M
        print(f"[DEBUG] Returning {result} for three-parameter model")
        print(f"[DEBUG_CN] 三参数模型返回 {result}")
        return result

    print("[DEBUG] No matching conditions, returning 0")
    print("[DEBUG_CN] 无匹配条件，返回 0")
    return 0

def tsiolkovsky_delta_v(i_sp, g0, m_initial, m_final):
    from math import log
    return i_sp * g0 * log(m_initial / m_final)

def muzzle_energy(m, v):
    return 0.5 * m * v**2

def optimize_ak12(bullet_mass, muzzle_velocities, rates_fire, barrel_lens, prop_energies, recoil_imps):
    best_score = -1
    best_params = None
    for v_m in muzzle_velocities:
        for rf in rates_fire:
            for bl in barrel_lens:
                for pe in prop_energies:
                    for ri in recoil_imps:
                        score = engineering_thought_modular_composition(
                            (bullet_mass, v_m, rf),
                            (bl, pe, ri)
                        )
                        if score > best_score:
                            best_score = score
                            best_params = (v_m, rf, bl, pe, ri)
    return best_score, best_params

if __name__ == "__main__":
    dv = tsiolkovsky_delta_v(300, 9.81, 5, 3)
    ek = muzzle_energy(0.008, 880)
    score, params = optimize_ak12(
        bullet_mass=0.008,
        muzzle_velocities=[700, 800, 880],
        rates_fire=[600, 650],
        barrel_lens=[0.415, 0.5],
        prop_energies=[1800, 2000],
        recoil_imps=[1.5, 1.8]
    )
    print("Tsiolkovsky Δv:", dv)
    print("Sample muzzle energy:", ek)
    print("Optimized AK-12 score:", score)
    print("Optimized parameters:", params)
