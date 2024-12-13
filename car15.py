'''
Author: @ydzat
Date: 2024-12-13 16:07:32
LastEditors: @ydzat
LastEditTime: 2024-12-13 17:15:49
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
    'lower_rail': ['car15_bound_flashlight'],
    'muzzle': ['poseidon_flash_hider', 
               'sandstorm_vertical_compensator', 
               'bastion_horizontal_compensator',
               'slient_suppressor',
               'blazing_fire_suppessor',
               'whisper_tactical_suppressor',
               'titanium_contest_muzzle_brake',
               'm7_practical_suppressor',
               'advanced_multi_caliber_suppressor',
               'spiral_fire_flash_hider',
               'steel_muzzle_brake',
               'practical_suppressor',
               'ops_suppressor',
               'birdcage_flash_hider',
               'practical_flash_hider'],
    'barrel': ['g18_impact_long_barrel'],
    'optic': ['osight_red_dot', 'combat_red_dot_sight', 'xro_quick_response_sight', 'mini_red_dot_sight', 'panoramic_red_dot_sight'],
    'rear_grip': ['xk_competition_rear_grip', 'xk_anti-slip_rear_girp', 'xk_rubber_coated_rear_grip'],
    'mag': ['g-series_pistol_33_round_mag']
}
