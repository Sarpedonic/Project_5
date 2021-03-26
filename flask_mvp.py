import numpy as np
import pandas as pd
import random

from flask import Flask
from flask import request
app = Flask(__name__)

shares = pd.read_csv("Shared_Compounds_Dense.csv")

@app.route('/')
def index():
    first_flavor = request.args.get("first_flavor","")
    if first_flavor:
        flavors = flavor_generator(first_flavor)
    else:
        flavors = ""
    return ("""<form action="" method="get">
                <input type="text" name="first_flavor">
                <input type="submit" value="flavor search">
              </form>"""
            + "Flavors: "
            + flavors
            )

def flavor_generator(first_flavor, num_flavors=5, flavor_space=shares):
    try:
        flavors = []
        flavors.append(first_flavor)
        n = num_flavors - 1
        current_flavor = first_flavor
        fail = 0
        while n > 0:
            new_flavor_index = random.choices(flavor_space.index,
                                              weights=flavor_space[current_flavor], k=1)
            new_flavor = flavor_space.iloc[new_flavor_index[0]][0]
            if new_flavor in flavors:
                fail += 1
                if fail > 1000:
                    print("Too much failure. Can't continue.")
                    break
                else:
                    current_flavor = first_flavor
                    continue
            else:
                flavors.append(new_flavor)
                current_flavor = new_flavor
                n -= 1
        return str(flavors)
    except KeyError:
        return "Input not valid."