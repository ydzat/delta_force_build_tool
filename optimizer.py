import gurobipy as gp
from gurobipy import GRB

class Optimizer:
    def __init__(self, data_manager, weapon_type, weapon_name):
        """
        Initialize the optimizer with weapon data and rules.
        :param data_manager: An instance of the DataManager class.
        :param weapon_type: Type of the weapon (e.g., 'rifle', 'pistol').
        :param weapon_name: Name of the weapon (e.g., 'car15', 'g18').
        """
        self.weapon_type = weapon_type
        self.weapon_data = data_manager.get_weapon_data(weapon_type, weapon_name)
        self.rules = data_manager.get_weapon_rules(weapon_type, weapon_name)
        if not self.weapon_data:
            raise ValueError(f"Weapon {weapon_name} not found in type {weapon_type}.")

        self.model = gp.Model(weapon_name)
        self.choices = {}
        self.total_attributes = {}
        self.attribute_keys = list(self.weapon_data["attributes"].keys())
        self.normalized_attributes = {}

    def setup_model(self):
        """Setup the optimization model with variables and constraints."""
        parts = self.weapon_data["parts"]

        # Create binary decision variables for parts
        for part, items in parts.items():
            self.choices[part] = {}
            for item, effects in items.items():
                self.choices[part][item] = self.model.addVar(vtype=GRB.BINARY, name=f"{part}_{item}")

        # Each part can have at most one attachment selected
        for part, items in parts.items():
            self.model.addConstr(
                sum(self.choices[part][item] for item in items) <= 1, name=f"choose_one_{part}"
            )

        # Initialize total attributes with base values
        self.total_attributes = {
            key: self.weapon_data["attributes"][key] for key in self.attribute_keys
        }

        # Add effects of chosen parts to total attributes
        for part, items in parts.items():
            for item, effects in items.items():
                for i, key in enumerate(self.attribute_keys):
                    self.total_attributes[key] += self.choices[part][item] * effects[i]

    def normalize_attributes(self):
        """Normalize attributes to ensure consistent weighting."""
        normalized_attributes = {}
        for key in self.attribute_keys:
            values = [
                self.weapon_data["attributes"][key]
            ]  # Start with base attribute values

            # Include contributions from parts
            for part, items in self.weapon_data["parts"].items():
                for item, effects in items.items():
                    values.append(effects[self.attribute_keys.index(key)])  # Add effect value
            
            min_val = min(values)
            max_val = max(values)

            # Avoid division by zero
            range_val = max_val - min_val if max_val != min_val else 1
            
            normalized_attributes[key] = (self.total_attributes[key] - min_val) / range_val

        self.normalized_attributes = normalized_attributes

    def apply_rules(self):
        """Apply dependency, conflict, and default disabled rules to the model."""
        if "dependencies" in self.rules:
            self._apply_dependencies(self.rules["dependencies"])
        if "conflicts" in self.rules:
            self._apply_conflicts(self.rules["conflicts"])

    def _apply_dependencies(self, dependencies):
        """
        Apply dependency rules using Big-M constraints for multiple dependencies,
        and closure constraints for single dependencies.
        :param dependencies: A dictionary defining dependencies and allowed parts.
        """
        M = 1e6  # Big-M constant

        for part, dependency in dependencies.items():
            for candidate, allowed_slots in dependency.items():
                candidate_var = self.choices[part][candidate]  # Current part variable

                for slot in allowed_slots:
                    total_dependencies = sum(1 for c in dependency.values() if slot in c)

                    for item in self.weapon_data["parts"][slot].keys():
                        slot_var = self.choices[slot][item]

                        if total_dependencies > 1:
                            # Use Big-M for multiple dependencies
                            self.model.addConstr(
                                slot_var <= candidate_var + M * (1 - candidate_var),
                                name=f"bigM_dependency_{part}_{candidate}_enables_{slot}_{item}"
                            )
                        else:
                            # Direct constraints for single dependencies
                            self.model.addConstr(
                                slot_var <= candidate_var,
                                name=f"direct_dependency_{part}_{candidate}_controls_{slot}_{item}"
                            )

    def _apply_conflicts(self, conflicts):
        """
        Apply conflict rules using Big-M constraints.
        :param conflicts: A dictionary defining conflicts.
                        If a key is selected, its associated parts cannot be selected.
        """
        M = 1e6  # A sufficiently large constant for the big-M method
        for part, conflict_parts in conflicts.items():
            for candidate, conflict_slots in conflict_parts.items():
                candidate_var = self.choices[part][candidate]

                for slot in conflict_slots:
                    for item in self.weapon_data["parts"][slot].keys():
                        slot_var = self.choices[slot][item]

                        # Add Big-M constraints
                        self.model.addConstr(
                            slot_var <= M * (1 - candidate_var),
                            name=f"bigM_conflict_{part}_{candidate}_disables_{slot}_{item}"
                        )

    def set_objective(self, weights):
        """
        Set the objective function for optimization.
        :param weights: A dictionary with attributes as keys and weights as values.
        """
        self.normalize_attributes()  # Normalize attributes before setting objective
        objective = gp.quicksum(
            weights[key] * self.normalized_attributes[key] for key in self.attribute_keys
        )
        self.model.setObjective(objective, GRB.MAXIMIZE)

    def optimize(self):
        """Solve the optimization problem."""
        self.model.optimize()

    def get_results(self):
        """
        Retrieve the results of the optimization in a structured format.
        :return: A dictionary with selected parts and final attributes.
        """
        if self.model.Status != GRB.OPTIMAL:
            return {"status": "No optimal solution found."}

        selected_parts = {
            part: [item for item, var in items.items() if var.X > 0.5]
            for part, items in self.choices.items()
        }
        final_attributes = {key: self.total_attributes[key].getValue() for key in self.attribute_keys}

        return {
            "parts": {k: v[0] if v else None for k, v in selected_parts.items()},
            "attributes": final_attributes,
            "status": "Optimal solution found."
        }

    def add_constraints(self, constraints):
        """
        Add custom constraints to the model.
        :param constraints: A list of constraint dictionaries, each with:
                            - 'attribute': The attribute or part to constrain (e.g., "Damage", "mag").
                            - 'operator': The operator for the constraint ("=", ">=", "<=").
                            - 'value': The value or item for the constraint.
        """
        for constraint in constraints:
            attribute = constraint["attribute"]
            operator = constraint["operator"]
            value = constraint["value"]

            if attribute in self.choices:
                for item in self.choices[attribute]:
                    if item == value:
                        var = self.choices[attribute][item]
                        if operator == "=":
                            self.model.addConstr(var == 1, name=f"constraint_{attribute}_{item}_eq_1")
                        elif operator == "<=":
                            self.model.addConstr(var <= 1, name=f"constraint_{attribute}_{item}_lte_1")
                        elif operator == ">=":
                            self.model.addConstr(var >= 1, name=f"constraint_{attribute}_{item}_gte_1")
            elif attribute in self.total_attributes:
                attr_value = self.total_attributes[attribute]
                if operator == "=":
                    self.model.addConstr(attr_value == value, name=f"constraint_{attribute}_eq_{value}")
                elif operator == "<=":
                    self.model.addConstr(attr_value <= value, name=f"constraint_{attribute}_lte_{value}")
                elif operator == ">=":
                    self.model.addConstr(attr_value >= value, name=f"constraint_{attribute}_gte_{value}")
            else:
                raise ValueError(f"Invalid attribute or part specified in constraints: {attribute}")
