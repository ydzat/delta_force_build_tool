<!--
 * @Author: @ydzat
 * @Date: 2024-12-13 17:21:20
 * @LastEditors: @ydzat
 * @LastEditTime: 2024-12-18 02:41:31
 * @Description: 
-->
# Delta Force (International Server) loadout tool
Automatically calculate the best loadout. (Just now only for battlefield)

The solver was changed from gurobi to pulp, but the old gurobi files are still retained.

For general users, please use `main_cbc.py` to perform calculations.

# Require

python 3

~~gurobi~~

PuLP

# Current support guns
```
### pistol
    g18
### smg
    uzi
    bizon
    smg45
    vector
    vityaz
    mp5
    p90
    sr_3m
    mp7
### rifle
    car15
    ptr32
    qbz95_1
    akm
    ak12
    m16a4
    as_val
    aks74
    sg552
    m4a1
    ci19
    k416
    aug
    g3
    scar_h
    ash12
    m7
### lmg
    pkm
    m249
    m250
```


# How to use
You can manually modify the weights in `main_cbc.py`




run:
```
pip install pulp
python main_cbc.py
```

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

+ Complete data entry for smg

# Further development
The general framework of the program has been built and the core code has been implemented. Now, you only need to enter the weapon data and the corresponding constraints in `./data/weapons.json` and `./data/rules.json` to start the calculation.


