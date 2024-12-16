'''
Author: @ydzat
Date: 2024-12-13 23:16:20
LastEditors: @ydzat
LastEditTime: 2024-12-16 01:56:33
Description: 
'''
from data_manager import DataManager
from optimizer import Optimizer


def main():
    # Load data and rules
    data_manager = DataManager("./data/weapons.json", "./data/rules.json")
    data_manager.load_data()
    data_manager.load_rules()

    # Initialize optimizer
    weapon_type = "smg"
    weapon_name = "vector"

    optimizer = Optimizer(data_manager, weapon_type, weapon_name)
    optimizer.setup_model()

    # 添加用户指定的约束
    optimizer.add_constraints([
        #{"attribute": "mag", "operator": "=", "value": "uzi_45"},
        {"attribute": "Handling", "operator": ">=", "value": 50},
        {"attribute": "Stability", "operator": ">=", "value": 50},
        #{"attribute": "rear_grip", "operator": "=", "value": "invasion_rear_grip"}
        #{"attribute": "rear_grip", "operator": "=", "value": "ar_heavy_tower_grip"}
        #{"attribute": "barrel", "operator": "=", "value": "ar_specops_integrally_suppressed_combo"}

    ])

    # Apply rules
    optimizer.apply_rules()

    # Set objective function
    weights = {
        'Damage': 0.5,
        'Range': 0.5,
        'Control': 1.5,
        'Handling': 1.5,
        'Stability': 1.5,
        'Accuracy': 1,
        'fire_rate': 1,
        'capacity': 2,
        'muzzle_velocity': 1
    }
    optimizer.set_objective(weights)

    # Solve the optimization problem
    optimizer.optimize()

    # Output results
    results = optimizer.get_results()
    if results["status"] == "Optimal solution found.":
        print("Optimal Configuration:")
        for part, item in results["parts"].items():
            print(f"  {part}: {item}")
        print("\nFinal Attributes:")
        for attr, value in results["attributes"].items():
            print(f"  {attr}: {value:.2f}")
    else:
        print(results["status"])


if __name__ == "__main__":
    main()
