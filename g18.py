'''
Author: @ydzat
Date: 2024-12-13 16:08:49
LastEditors: @ydzat
LastEditTime: 2024-12-13 17:21:47
Description: 
'''
import os
import gurobipy as gp
from gurobipy import multidict

attributes = {
    'Damage': 14,
    'Range': 10,
    'Control': 30,
    'Handling': 62,
    'Stability': 43,
    'Accuracy': 67,

    'fire_rate': 1172,
    'capacity': 17,
    'muzzle_velocity': 400
}

parts = {
    'lower_rail': ['practical_weapon_light', 'olight_baldr_pro_r_multi_function_flashlight'],
    'muzzle': ['smg_echo_suppressor', 'practical_pistol_flash_hider', 'purifica_pistol_suppressor', 'elite_pistol_muzzle_brake'],
    'barrel': ['g18_impact_long_barrel'],
    'optic': ['osight_red_dot', 'combat_red_dot_sight', 'xro_quick_response_sight', 'mini_red_dot_sight', 'panoramic_red_dot_sight'],
    'rear_grip': ['xk_competition_rear_grip', 'xk_anti-slip_rear_girp', 'xk_rubber_coated_rear_grip'],
    'mag': ['g-series_pistol_33_round_mag']
}

effects = {
    'practical_weapon_light': [0, 0, 0, -5, 0, -8, 0, 0, 0],
    'olight_baldr_pro_r_multi_function_flashlight': [0, 0, 0, -3, 0, -5, 0, 0, 0],
    'smg_echo_suppressor': [0, 2, 7, -6, -2, -8, 0, 0, 60], 
    'practical_pistol_flash_hider': [0,0,3,0,0,0, 0, 0, 0], 
    'purifica_pistol_suppressor':[0,0,0,-6,-2,0, 0, 0, 0], 
    'elite_pistol_muzzle_brake':[0,0,9,-3,0,0, 0, 0, 0],
    'g18_impact_long_barrel':[0,2,7,-7,4,-12, 0, 0, 60],
    'osight_red_dot':[0,0,0,0,0,0, 0, 0, 0], 
    'combat_red_dot_sight':[0,0,0,0,0,0, 0, 0, 0], 
    'xro_quick_response_sight':[0,0,0,0,0,0, 0, 0, 0], 
    'mini_red_dot_sight':[0,0,0,0,0,0, 0, 0, 0], 
    'panoramic_red_dot_sight':[0,0,0,0,0,0, 0, 0, 0],
    'xk_competition_rear_grip':[0,0,4,2,0,0, 0, 0, 0], 
    'xk_anti-slip_rear_girp':[0,0,2,4,0,0, 0, 0, 0], 
    'xk_rubber_coated_rear_grip':[0,0,4,2,0,0, 0, 0, 0],
    'g-series_pistol_33_round_mag':[0,0,-3,-6,0,-8, 0, 16, 0]
}


model = gp.Model("g18")

# 为每个插槽和配件创建二进制变量
choices = {}
for part, items in parts.items():
    choices[part] = {}
    for item in items:
        choices[part][item] = model.addVar(vtype=gp.GRB.BINARY, name=f"{part}_{item}")

# 添加约束：每个部件最多选择一个配件
for part, items in parts.items():
    model.addConstr(sum(choices[part][item] for item in items) <= 1, name=f"choose_one_{part}")

# 计算总属性值
attribute_keys = list(attributes.keys())
total_attributes = {key: attributes[key] for key in attribute_keys}

# 根据选择的配件计算属性增益
for part, items in parts.items():
    for i, key in enumerate(attribute_keys):
        total_attributes[key] += sum(choices[part][item] * effects[item][i] for item in items)

# 目标函数：最大化capacity和Stability，同时尽可能平衡其他属性
weights = {
    'Damage': 0.5,
    'Range': 0.5,
    'Control': 1,
    'Handling': 1,
    'Stability': 2,  # 更高权重
    'Accuracy': 1,
    'fire_rate': 1,
    'capacity': 3,   # 更高权重
    'muzzle_velocity': 1
}

objective = gp.quicksum(weights[key] * total_attributes[key] for key in attribute_keys)
model.setObjective(objective, gp.GRB.MAXIMIZE)

# 求解模型
model.optimize()

# 输出结果
if model.Status == gp.GRB.OPTIMAL:
    print("Optimal solution found:")
    for part, items in parts.items():
        for item in items:
            if choices[part][item].x > 0.5:  # 判断是否选择
                print(f"Selected {part}: {item}")
    print("Attributes:")
    for key in attribute_keys:
        print(f"{key}: {total_attributes[key].getValue()}")
else:
    print("No optimal solution found.")