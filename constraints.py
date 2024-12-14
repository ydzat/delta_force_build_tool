'''
Author: @ydzat
Date: 2024-12-13 23:14:30
LastEditors: @ydzat
LastEditTime: 2024-12-13 23:15:09
Description: 
'''
class ConstraintManager:
    def __init__(self):
        self.constraints = []

    def add_constraint(self, constraint_function):
        """添加新的约束"""
        self.constraints.append(constraint_function)

    def apply_constraints(self, model, choices):
        """将所有约束应用到Gurobi模型"""
        for constraint in self.constraints:
            constraint(model, choices)

    def max_capacity_constraint(model, choices, max_value):
        """限制某个属性的最大值"""
        model.addConstr(total_attributes['capacity'] <= max_value)

    def must_use_part_constraint(model, choices, part_category, part_name):
        """强制使用某个部件"""
        model.addConstr(choices[part_category][part_name] == 1)
