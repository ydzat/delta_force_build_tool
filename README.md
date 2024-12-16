<!--
 * @Author: @ydzat
 * @Date: 2024-12-13 17:21:20
 * @LastEditors: @ydzat
 * @LastEditTime: 2024-12-16 02:03:13
 * @Description: 
-->
# Delta Force (International Server) loadout tool
Automatically calculate the best loadout. (Just now only for battlefield)

# require
python 3
gurobi

# current support guns
```
### Pistol
    g18
### SMG
    uzi
    bizon
    smg45
    vector
### Rifle
    car15
```


# how to use
You can manually modify the weights in `main.py`

run:
`python main.py`

If you want to customize the requirements, make the following changes in `main.py`:

```
# In the Initialize optimizer section, you need to modify it to the weapon you want to calculate, type is the weapon type, and name is the name (mainly based on the name of the English version of the game).
# NOTE! Before calculation, please make sure weapons.json and rules.json contain the weapons you want to calculate.

# Add the corresponding requirements in optimizer.add_constraints. 
# In file has given the currently supported examples.
# {"attribute": "specified component", "operator": "can be =, >=, <=", "value": <data or component name>}

# Weight part: 
# You can enter this weight yourself. The larger the value, the greater the weight.
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
```

# Changelog
Now the program can run normally. 

# Further development
The general framework of the program has been built and the core code has been implemented. Now, you only need to enter the weapon data and the corresponding constraints in `./data/weapons.json` and `./data/rules.json` to start the calculation.


