'''
Author: @ydzat
Date: 2024-12-13 16:07:32
LastEditors: @ydzat
LastEditTime: 2024-12-13 19:15:55
Description: 
'''
import os
import gurobipy as gp
from gurobipy import multidict

attributes = {
    'Damage': 25,
    'Range': 30,
    'Control': 50,
    'Handling': 58,
    'Stability': 55,
    'Accuracy': 53,

    'fire_rate': 632,
    'capacity': 20,
    'muzzle_velocity': 550
}

parts = {
    'lower_rail': {
        'car15_bound_flashlight': [0, 0, 0, -3, 0, 0, 0, 0, 0]
    },
    'muzzle': {
        'poseidon_flash_hider': [0, 0, 6, -1, 0, 0, 0, 0, 0],
        'sandstorm_vertical_compensator': [0, 0, 9, -2, 0, 0, 0, 0, 0],
        'bastion_horizontal_compensator': [0, 0, 9, -2, 0, 0, 0, 0, 0],
        'slient_suppressor': [0, 4, 6, -8, -4, 0, -82, 0, 66],
        'blazing_fire_suppessor': [0, 0, 6, -1, 0, 0, 0, 0, 0],
        'whisper_tactical_suppressor': [0, 3, 5, -3, -3, 0, 0, 0, 50],
        'titanium_contest_muzzle_brake': [0, 0, 9, -2, 0, 0, 0, 0, 0],
        'm7_practical_suppressor': [0, 0, 8, -6, 0, 0, 0, 0, 0],
        'advanced_multi_caliber_suppressor': [0, 0, 5, -3, 0, 0, 0, 0, 0],
        'spiral_fire_flash_hider': [0, 0, 4, 0, 1, 0, 0, 0, 0],
        'steel_muzzle_brake': [0, 0, 6, 0, -1, 0, 0, 0, 0],
        'practical_suppressor': [0, 0, 0, 0, 0, 0, 0, 0, 0],
        'ops_suppressor': [0, 0, 8, -5, -3, 0, 0, 0, 0],
        'birdcage_flash_hider': [0, 0, 3, 0, 1, 0, 0, 0, 0],
        'practical_flash_hider': [0, 0, 2, 0, 2, 0, 0, 0, 0]
    },
    'barrel': {
        'ar_specops_integrally_suppressed_combo': [0, 3, 12, -3, -4, 0, 0, 0, 50],
        'ar_raid_short_barrel_combo': [0, 0, 4, 6, -6, 8, 0, 0, 0],
        'ar_trench_standard_barrel_combo': [0, 2, 5, 0, 0, 0, 0, 0, 33],
        'ar_gabriel_long_barrel_combo': [0, 5, 7, -7, 4, -12, 0, 0, 83],
        'ar_standard_barrel_combo': [0, 0, 2, 6, -6, 8, 0, 0, 0],
        'ar_carbon_fiber_barrel_combo': [0, 3, 6, -5, 3, -12, 0, 0, 50]
    },
    'optic': {
        'HAMR_Combined_Scope':[0,0,0,-6,0,0,0,0,0],
        '1P-29_russian_3x_scope':[0,0,0,-4,0,0,0,0,0],
        'lpvo_scope':[0,0,0,-6,0,0,0,0,0],
        'viewpoint_3x_scope':[0,0,0,-4,0,0,0,0,0],
        'recon_1.5/5_adjustable_scope':[0,0,0,-8,3,0,0,0,0],
        '3/7_adjustable_scope':[0,0,0,-8,3,0,0,0,0],
        'm157_fire_control_optical_system':[0,0,0,-6,0,0,0,0,0],
        'insight_3/7_sniper_scope':[0,0,0,-8,0,0,0,0,0],
        'acog_precision_6x_scope':[0,0,0,-2,0,0,0,0,0],
        'osight_red_dot':[0,0,0,0,0,0,0,0,0],
        'cobra_accuracy_sight':[0,0,0,0,0,0,0,0,0],
        'okp_7_reflex_sight':[0,0,0,0,0,0,0,0,0],
        'xcog_assault_3.5x_scope':[0,0,0,-4,0,0,0,0,0],
        'combat_red_dot_sight':[0,0,0,0,0,0,0,0,0],
        'mini_red_dot_sight':[0,0,0,0,0,0,0,0,0],
        'xro_quick_response_sight':[0,0,0,0,0,0,0,0,0],
        'multi_purpose_tactical_riser':[0,0,-1,1,0,0,0,0,0],
        'micro_sight_riser':[0,0,-1,1,0,0,0,0,0],
        'panoramic_red_dot_sight':[0,0,0,0,0,0,0,0,0],
        'ap5000_reflex_sight':[0,0,0,0,0,0,0,0,0],
        'holographic_sight_type_ii':[0,0,0,0,0,0,0,0,0],
        'reflex_sight':[0,0,0,0,0,0,0,0,0],
        'russian_accuracy_2x_scope':[0,0,0,0,0,0,0,0,0],
        'holographic_sight':[0,0,0,0,0,0,0,0,0]
    },
    'rear_grip': {
        'ar_heavy_tower_grip': [0,0,1,1,1,1,0,0,0],
        'invasion_rear_grip': [0,0,3,3,0,0,0,0,0],
        'phantom_rear_grip': [0,0,3,7,-4,0,0,0,0],
        'hurricane_d1_rear_grip': [0,0,0,4,0,0,0,0,0],
        'marksman_d2_rear_grip': [0,0,0,0,4,0,0,0,0],
        'm7_stable_rear_grip': [0,0,3,1,0,0,0,0,0],
        '416_practical_rear_grip': [0,0,0,2,2,0,0,0,0]
    },
    'mag': {
        'm4_45': [0,0,-1,-5,-2,-8,0,25,0],
        'm4_60': [0,0,-3,-9,-4,0,0,40,0],
        '556_30_Aluminum': [0,0,0,0,0,0,0,10,0],
        '556_30_Polymer': [0,0,0,6,0,0,0,10,0]
    },
    'mag_mount': {
        'badger': [0,0,0,1,0,0,0,0,0]
    },
    'stock': {
        'ur_spec_ops_tactical': [0,0,6,-4,4,0,0,0,0],
        'shadow_buffer_tube': [0,0,2,10,-6,0,0,0,0],
        'elite_light': [0,0,3,3,0,0,0,0,0],
        '416_stable': [0,0,4,-6,8,0,0,0,0],
        'invasion_core': [0,0,6,0,0,0,0,0,0],
        '416_light': [0,0,6,6,-6,0,0,0,0],
        'cardinal_stable': [0,0,6,0,0,0,0,0,0],
        'skeleton_sniper': [0,0,-4,8,6,-16,0,0,0],
        'practical_light': [0,0,0,4,0,0,0,0,0],
        'practical_tactical': [0,0,4,0,0,0,0,0,0],
        'practical_stable': [0,0,2,0,2,0,0,0,0],
        'm4_recoil_buffer_tube': [0,0,-7,12,-4,12,0,0,0]
    },
    'right_rail':{
        'flare_tactical_flashlight': [0,0,0,-1,0,0,0,0,0],
        '* laser-light combo': [0,0,0,-4,0,0,0,0,0],
        'olight_baldr_pro_r_multi_function_flashlight': [0,0,0,-5,0,-8,0,0,0],
        'olight_odin_s': [0,0,0,-1,0,0,0,0,0],
        'olight_warrior_3s': [0,0,0,-4,-4,0,0,0,0],
        'practical_weapon_light': [0,0,0,-1,0,0,0,0,0],
        'modular_handguard_panel': [0,0,1,-2,1,0,0,0,0],
        'hornet_handguard': [0,0,0,0,0,4,0,0,0],
        'dd_python_handguard': [0,0,0,1,0,0,0,0,0],
        'kc_hound_handguard': [0,0,0,0,1,0,0,0,0],
        'ranger_handguard': [0,0,1,0,0,0,0,0,0]
    },
    'left_rail':{
        'flare_tactical_flashlight': [0,0,0,-1,0,0,0,0,0],
        '* laser-light combo': [0,0,0,-4,0,0,0,0,0],
        'olight_baldr_pro_r_multi_function_flashlight': [0,0,0,-5,0,-8,0,0,0],
        'olight_odin_s': [0,0,0,-1,0,0,0,0,0],
        'olight_warrior_3s': [0,0,0,-4,-4,0,0,0,0],
        'practical_weapon_light': [0,0,0,-1,0,0,0,0,0],
        'modular_handguard_panel': [0,0,1,-2,1,0,0,0,0],
        'hornet_handguard': [0,0,0,0,0,4,0,0,0],
        'dd_python_handguard': [0,0,0,1,0,0,0,0,0],
        'kc_hound_handguard': [0,0,0,0,1,0,0,0,0],
        'ranger_handguard': [0,0,1,0,0,0,0,0,0]
    },
    'upper_rail':{
        'flare_tactical_flashlight': [0,0,0,-1,0,0,0,0,0],
        '* laser-light combo': [0,0,0,-4,0,0,0,0,0],
        'olight_baldr_pro_r_multi_function_flashlight': [0,0,0,-5,0,-8,0,0,0],
        'olight_odin_s': [0,0,0,-1,0,0,0,0,0],
        'olight_warrior_3s': [0,0,0,-4,-4,0,0,0,0],
        'practical_weapon_light': [0,0,0,-1,0,0,0,0,0],
        'modular_handguard_panel': [0,0,1,-2,1,0,0,0,0],
        'hornet_handguard': [0,0,0,0,0,4,0,0,0],
        'dd_python_handguard': [0,0,0,1,0,0,0,0,0],
        'kc_hound_handguard': [0,0,0,0,1,0,0,0,0],
        'ranger_handguard': [0,0,1,0,0,0,0,0,0]
    },
    'rail_bipod':{
        'practical_bipod': [0,0,0,-4,0,0,0,0,0]
    },
    'left_patch':{
        'modular_handguard_panel': [0,0,1,-2,1,0,0,0,0],
        'hornet_handguard': [0,0,0,0,0,4,0,0,0],
        'dd_python_handguard': [0,0,0,1,0,0,0,0,0],
        'kc_hound_handguard': [0,0,0,0,1,0,0,0,0],
        'ranger_handguard': [0,0,1,0,0,0,0,0,0]
    },
    'right_patch':{
        'modular_handguard_panel': [0,0,1,-2,1,0,0,0,0],
        'hornet_handguard': [0,0,0,0,0,4,0,0,0],
        'dd_python_handguard': [0,0,0,1,0,0,0,0,0],
        'kc_hound_handguard': [0,0,0,0,1,0,0,0,0],
        'ranger_handguard': [0,0,1,0,0,0,0,0,0]
    },
    'upper_patch':{
        'modular_handguard_panel': [0,0,1,-2,1,0,0,0,0],
        'hornet_handguard': [0,0,0,0,0,4,0,0,0],
        'dd_python_handguard': [0,0,0,1,0,0,0,0,0],
        'kc_hound_handguard': [0,0,0,0,1,0,0,0,0],
        'ranger_handguard': [0,0,1,0,0,0,0,0,0]
    },
    'foregrip':{
        'rk_0_foregrip': [0,0,6,0,0,0,0,0,0],
        'k1_elite_bevel_foregrip':[0,0,6,0,0,0,0,0,0],
        'competition_hand_stop':[0,0,-2,5,0,12,0,0,0],
        'phase_combat_foregrip':[0,0,3,2,1,0,0,0,0],
        'tactical_vertical_foregrip':[0,0,0,6,0,0,0,0,0],
        'x25u_angled_combat_grip':[0,0,10,-3,-3,8,0,0,0],
        'resonant_ergonomic_grip':[0,0,7,-1,0,0,0,0,0],
        'collapsible_bipod_grip':[0,0,0,1,0,-12,0,0,0],
        'cr_prism_hand_stop':[0,0,6,0,0,0,0,0,0],
        'angled_hand_stop':[0,0,-2,8,0,0,0,0,0],
        'secret_order_bevel_foregrip': [0,0,7,-1,0,0,0,0,0],
        'phantom_vertical_foregrip': [0,0,0,8,-2,0,0,0,0],
        'daybreak_vertical_flashlight_grip': [0,0,6,-7,2,0,0,0,0],
        'dawn_angled_flashlight_grip': [0,0,8,-5,-2,0,0,0,0],
        'tactical_angled_foregrip': [0,0,4,2,0,0,0,0,0],
        'resonant_mkii_foregrip': [0,0,4,4,-2,0,0,0,0],
        'vfg_knight_foregrip': [0,0,0,4,0,0,0,0,0],
        'folding_grip':[0,0,0,1,5,0,0,0,0],
        'mini_hand_stop':[0,0,0,2,0,8,0,0,0],
        'practical_vertical_foregrip':[0,0,4,0,0,0,0,0,0],
        'zfsg_tactical_grip': [0,0,1,0,0,12,0,0,0]
    },
    'grip_mount':{
        'stable_grip_base': [0,0,2,-5,7,0,0,0,0],
        'balanced_grip_base': [0,0,1,1,1,4,0,0,0]    
    },
    'tactical_device':{
        'laser-light_combo': [0,0,0,-4,0,0,0,0,0],
    },
    'riser_optic':{
        '* sight':[0,0,0,0,0,0,0,0,0],
        'micro_sight_riser':[0,0,-1,1,0,0,0,0,0],
    },
    'stock_kit':{
        'resonant_2_integral_stock':[0,0,7,10,-6,4,0,0,0],
        'restricted_zone_integral_stock':[0,0,11,-6,7,0,0,0,0],
    }
}

model = gp.Model("car15")

# 为每个插槽和配件创建二进制变量
choices = {}
for part, items in parts.items():
    choices[part] = {}
    for item, effects in items.items():
        choices[part][item] = model.addVar(vtype=gp.GRB.BINARY, name=f"{part}_{item}")

# 添加约束：每个部件最多选择一个配件
for part, items in parts.items():
    model.addConstr(sum(choices[part][item] for item in items) <= 1, name=f"choose_one_{part}")

# 约束：如果barrel没有选择，那么left_rail/upper_rail/foregrip/grip_mount/left_patch/right_patch/upper_patch也不能选择，但是能选择lower_rail
barrel_selected = sum(choices['barrel'][item] for item in parts['barrel'])
dependent_parts = ['left_rail', 'upper_rail', 'foregrip', 'grip_mount', 'left_patch', 'right_patch', 'upper_patch']

for part in dependent_parts:
    model.addConstr(sum(choices[part][item] for item in parts[part]) <= barrel_selected, 
                    name=f"{part}_depends_on_barrel")

# 如果barrel中选择了ar_specops_integrally_suppressed_combo，那么不能选择muzzle/lower_rail，但是可以选择foregrip/rail_bipod/upper_rail/left_rail/upper_patch/left_patch/right_patch
# 获取 ar_specops_integrally_suppressed_combo 的选择变量
ar_specops_selected = choices['barrel']['ar_specops_integrally_suppressed_combo']

# 添加约束：如果选择了 ar_specops_integrally_suppressed_combo，则 muzzle 和 lower_rail 不可选
for item in parts['muzzle']:
    model.addConstr(choices['muzzle'][item] <= 1 - ar_specops_selected, 
                    name=f"muzzle_forbidden_with_ar_specops")

for item in parts['lower_rail']:
    model.addConstr(choices['lower_rail'][item] <= 1 - ar_specops_selected, 
                    name=f"lower_rail_forbidden_with_ar_specops")

# 如果barrel中选择了ar_raid_short_barrel_combo，那么不能选择lower_rail/upper_patch/left_patch/right_patch/rail_bipod/right_rail
# 获取 ar_raid_short_barrel_combo 的选择变量
ar_raid_selected = choices['barrel']['ar_raid_short_barrel_combo']

# 添加约束：如果选择了 ar_raid_short_barrel_combo，则受限部分的变量总和必须为 0
restricted_parts = ['lower_rail', 'upper_patch', 'left_patch', 'right_patch', 'rail_bipod', 'right_rail']

for part in restricted_parts:
    for item in parts[part]:
        model.addConstr(choices[part][item] <= 1 - ar_raid_selected, 
                        name=f"{part}_forbidden_with_ar_raid")

# 如果barrel中选择了ar_trench_standard_barrel_combo，那么不能选择lower_rail，但是可以选择foregrip/rail_bipod/upper_rail/left_rail/upper_patch/left_patch/right_patch
# 获取 ar_trench_standard_barrel_combo 的选择变量
ar_specops_selected = choices['barrel']['ar_trench_standard_barrel_combo']

# 添加约束：如果选择了 ar_trench_standard_barrel_combo，则 lower_rail 不可选
for item in parts['lower_rail']:
    model.addConstr(choices['lower_rail'][item] <= 1 - ar_specops_selected, 
                    name=f"lower_rail_forbidden_with_ar_specops")

# 如果barrel中选择了ar_gabriel_long_barrel_combo，那么不能选择lower_rail，但是可以选择foregrip/rail_bipod/upper_rail/left_rail/upper_patch/left_patch/right_patch
# 获取 ar_gabriel_long_barrel_combo 的选择变量
ar_gabriel_selected = choices['barrel']['ar_gabriel_long_barrel_combo']

# 添加约束：如果选择了 ar_gabriel_long_barrel_combo，则 lower_rail 不可选
for item in parts['lower_rail']:
    model.addConstr(choices['lower_rail'][item] <= 1 - ar_gabriel_selected, 
                    name=f"lower_rail_forbidden_with_ar_gabriel")

# 如果barrel中选择了ar_standard_barrel_combo，那么不能选择lower_rail，但是可以选择foregrip/rail_bipod/upper_rail/left_rail/upper_patch/left_patch/right_patch
# 获取 ar_standard_barrel_combo 的选择变量
ar_standard_selected = choices['barrel']['ar_standard_barrel_combo']

# 添加约束：如果选择了 ar_standard_barrel_combo，则 lower_rail 不可选
for item in parts['lower_rail']:
    model.addConstr(choices['lower_rail'][item] <= 1 - ar_standard_selected, 
                    name=f"lower_rail_forbidden_with_ar_standard")
    
# 如果barrel中选择了ar_carbon_fiber_barrel_combo，那么不能选择lower_rail，但是可以选择foregrip/rail_bipod/upper_rail/left_rail/upper_patch/left_patch/right_patch
# 获取 ar_carbon_fiber_barrel_combo 的选择变量
ar_carbon_fiber_selected = choices['barrel']['ar_carbon_fiber_barrel_combo']

# 添加约束：如果选择了 ar_carbon_fiber_barrel_combo，则 lower_rail 不可选
for item in parts['lower_rail']:
    model.addConstr(choices['lower_rail'][item] <= 1 - ar_carbon_fiber_selected, 
                    name=f"lower_rail_forbidden_with_ar_carbon_fiber")

# 如果mag中选择了m4_60，那么不能选择mag_mount
# 获取 m4_60 的选择变量
m4_60_selected = choices['mag']['m4_60']

# 添加约束：如果选择了 m4_60，则 mag_mount 不可选
for item in parts['mag_mount']:
    model.addConstr(choices['mag_mount'][item] <= 1 - m4_60_selected, 
                    name=f"mag_mount_forbidden_with_m4_60")

# 如果选择stock_kit中的任意部件，那么stock和rear_grip不能选择
# 获取 stock_kit 的选择变量
stock_kit_selected = sum(choices['stock_kit'][item] for item in parts['stock_kit'])

# 添加约束：如果选择了 stock_kit，则 stock 和 rear_grip 不可选
for part in ['stock', 'rear_grip']:
    for item in parts[part]:
        model.addConstr(choices[part][item] <= 1 - stock_kit_selected, 
                        name=f"{part}_forbidden_with_stock_kit")

# 除非在optic中选择了multi_purpose_tactical_riser，否则不能选择riser_optic和tantical_device
# 获取 multi_purpose_tactical_riser 的选择变量
multi_purpose_selected = choices['optic']['multi_purpose_tactical_riser']

# 添加约束：如果未选择 multi_purpose_tactical_riser，则 riser_optic 和 tactical_device 不可选
for part in ['riser_optic', 'tactical_device']:
    for item in parts[part]:
        model.addConstr(choices[part][item] <= multi_purpose_selected, 
                        name=f"{part}_forbidden_without_multi_purpose")

# 如果在rear_grip中选择了ar_heavy_tower_grip，那么grip_mount才能选择
# 获取 ar_heavy_tower_grip 的选择变量
ar_heavy_tower_selected = choices['rear_grip']['ar_heavy_tower_grip']

# 添加约束：如果选择了 ar_heavy_tower_grip，则 grip_mount 可选
for item in parts['grip_mount']:
    model.addConstr(choices['grip_mount'][item] <= ar_heavy_tower_selected, 
                    name=f"grip_mount_allowed_with_ar_heavy_tower")

# 指定使用mag: m4_45
model.addConstr(choices['mag']['m4_45'] == 1, name="use_mag_m4_45")


# 权重：我希望最大化Control和Stability，同时尽可能平衡其他属性，同时capacity尽可能高
weights = {
    'Damage': 0.5,
    'Range': 0.5,
    'Control': 2,
    'Handling': 1.5,
    'Stability': 1.5,
    'Accuracy': 1,
    'fire_rate': 1,
    'capacity': 1.25,
    'muzzle_velocity': 1
}

# 计算总属性值
attribute_keys = list(attributes.keys())
total_attributes = {key: attributes[key] for key in attribute_keys}

# 根据选择的部件计算属性增益
for part, items in parts.items():
    for item, effects in items.items():
        for i, key in enumerate(attribute_keys):
            total_attributes[key] += choices[part][item] * effects[i]

# 最终的handling不应小于50
model.addConstr(total_attributes['Handling'] >= 50, name="minimum_handling")
model.addConstr(total_attributes['Stability'] >= 50, name="minimum_handling")
model.update()


# 构建目标函数：权重加权求和
objective = gp.quicksum(weights[key] * total_attributes[key] for key in attribute_keys)
model.setObjective(objective, gp.GRB.MAXIMIZE)
#model.update()
# 求解模型
model.optimize()

# 输出结果
if model.Status == gp.GRB.OPTIMAL:
    print("Optimal solution found:")
    print("\nSelected parts:")
    for part, items in parts.items():
        for item in items:
            if choices[part][item].X > 0.5:  # 判断是否选择
                print(f"{part}: {item}")

    print("\nFinal attributes:")
    for key in attribute_keys:
        print(f"{key}: {total_attributes[key].getValue()}")
else:
    print("No optimal solution found.")























# effects = {
#     # lower_rail
#     'car15_bound_flashlight': [0,0,0,-3,0,0,0,0,0],
#     # muzzle
#     'poseidon_flash_hider': [0,0,6,-1,0,0,0,0,0], 
#     'sandstorm_vertical_compensator': [0,0,9,-2,0,0,0,0,0], 
#     'bastion_horizontal_compensator': [0,0,9,-2,0,0,0,0,0],
#     'slient_suppressor': [0,4,6,-8,-4,0,-82,0, 66],
#     'blazing_fire_suppessor': [0,0,6,-1,0,0,0,0,0],
#     'whisper_tactical_suppressor': [0,3,5,-3,-3,0,0,0,50],
#     'titanium_contest_muzzle_brake': [0,0,9,-2,0,0,0,0,0],
#     'm7_practical_suppressor': [0,0,8,-6,0,0,0,0,0],
#     'advanced_multi_caliber_suppressor': [0,0,5,-3,0,0,0,0,0],
#     'spiral_fire_flash_hider': [0,0,4,0,1,0,0,0,0],
#     'steel_muzzle_brake': [0,0,6,0,-1,0,0,0,0],
#     'practical_suppressor': [0,0,0,0,0,0,0,0,0],
#     'ops_suppressor': [0,0,8,-5,-3,0,0,0,0],
#     'birdcage_flash_hider': [0,0,3,0,1,0,0,0,0],
#     'practical_flash_hider': [0,0,2,0,2,0,0,0,0],
#     # barrel
#     'ar_specops_integrally_suppressed_combo': [0,3,12,-3,-4,0,0,0,50],
#     'ar_raid_short_barrel_combo': [0,0,4,6,-6,8,0,0,0],
#     'ar_trench_standard_barrel_combo': [0,2,5,0,0,0,0,0,33],
#     'ar_gabriel_long_barrel_combo':[0,5,7,-7,4,-12,0,0,83],
#     'ar_standard_barrel_combo': [0,0,2,6,-6,8,0,0,0],
#     'ar_carbon_fiber_barrel_combo': [0,3,6,-5,3,-12,0,0,50],
# }