"""
6.1010 Spring '23 Lab 4: Recipes
"""

import pickle
import sys

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def make_recipe_book(recipes):
    """
    Given recipes, a list containing compound and atomic food items, make and
    return a dictionary that maps each compound food item name to a list
    of all the ingredient lists associated with that name.
    """
    recipe_data = {}

    for i in recipes:
        if i[1] in recipe_data and i[0] != "atomic":
            recipe_data[i[1]].append(i[2])
        elif i[0]=="compound":
            recipe_data[i[1]] = [i[2]]
    return recipe_data


def make_atomic_costs(recipes):
    """
    Given a recipes list, make and return a dictionary mapping each atomic food item
    name to its cost.
    """
    recipe_data = {}

    for i in recipes:
        if i[0]=="atomic":
            recipe_data[i[1]] = i[2]

    return recipe_data


def lowest_cost(recipes, food_item, forbidden_foods = None):
    """
    Given a recipes list and the name of a food item, return the lowest cost of
    a full recipe for the given food item.
    """
    atomics = make_atomic_costs(recipes)
    compounds = make_recipe_book(recipes)
    if forbidden_foods is not None:
        for i in forbidden_foods:
            if i in atomics:
                atomics.pop(i)
            if i in compounds:
                compounds.pop(i)

    def lowcost(food):

        if food not in atomics and food not in compounds:
            return None
        elif food in atomics:
            return atomics[food]
        
        costs = []

        for i in compounds[food]:
            specific_cost = 0
            add_condition = True
            for j in i:
                amount = lowcost(j[0])
                if amount is None:
                    add_condition = False
                    break
                specific_cost+=(j[1]*amount)
            if add_condition:
                costs.append(specific_cost)
        if len(costs)==0:
            return None
        return min(costs)

    return lowcost(food_item)

def scale_recipe(flat_recipe, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    scaled = flat_recipe.copy()
    for i in scaled:
        scaled[i]*=n
    return scaled

def make_grocery_list(flat_recipes):
    """
    Given a list of flat_recipe dictionaries that map food items to quantities,
    return a new overall 'grocery list' dictionary that maps each ingredient name
    to the sum of its quantities across the given flat recipes.

    For example,
        make_grocery_list([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    combined = {}

    for i in flat_recipes:
        for j in i:
            if j not in combined:
                combined[j] = i[j]
            else:
                combined[j]+=i[j]
    return combined




def cheapest_flat_recipe(recipes, food_item, forbidden_foods = None):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    atomics = make_atomic_costs(recipes)
    compounds = make_recipe_book(recipes)

    if forbidden_foods is not None:
        for i in forbidden_foods:
            if i in atomics:
                atomics.pop(i)
            if i in compounds:
                compounds.pop(i)

    def cheapest(food):

        if food not in atomics and food not in compounds:
            return None
        elif food in atomics:
            return (atomics[food],{food:1})
        
        costs = []
        flats = {}
        for i in compounds[food]:
            specific_cost = 0
            groceries = {}
            add_condition = True
            for j in i:
                step = cheapest(j[0])
                if step is None:
                    add_condition = False
                    break

                specific_cost+=(j[1]*step[0])
                groceries = make_grocery_list([groceries, scale_recipe(step[1],j[1])])
            if add_condition:
                costs.append(specific_cost)
                flats[specific_cost] = groceries
        if len(costs)==0:
            return None
        return (min(costs),flats[min(costs)])

    result = cheapest(food_item)
    if result is None:
        return None
    else:
        return result[1]
    
def scaled_list(recipes, n):

    out = []
    for i in recipes:
        out.append(scale_recipe(i,n))
    return out


def ingredient_mixes(flat_recipes):
    """
    Given a list of lists of dictionaries, where each inner list represents all
    the flat recipes make a certain ingredient as part of a recipe, compute all
    combinations of the flat recipes.
    """
    result = []
    if len(flat_recipes)==0:
        return []
    elif len(flat_recipes)==1:
        return flat_recipes[0]
    for i in flat_recipes[0]:

        if len(flat_recipes)==2:
            for j in flat_recipes[1]:
                result.append(make_grocery_list([i,j]))
        
        else:

            for j in ingredient_mixes(flat_recipes[1:]):
                result.append(make_grocery_list([i,j]))
    return result

def prep_data(recipes, item):
    """
    takes in a dictionary of recipes and converts it to the
    format needed to use ingredient mixes
    """
    result = []
    for i in recipes[item]:
        temp = []
        for j in i:
            temp.append({j[0]:j[1]})
        result.append(temp)
    return result


def all_flat_recipes(recipes, food_item, forbidden_foods = None):
    """
    Given a list of recipes and the name of a food item, produce a list (in any
    order) of all possible flat recipes for that category.

    Returns an empty list if there are no possible recipes
    """
    atomics = make_atomic_costs(recipes)
    compounds = make_recipe_book(recipes)
    if forbidden_foods is not None:
        for i in forbidden_foods:
            if i in atomics:
                atomics.pop(i)
            if i in compounds:
                compounds.pop(i)

    def flats(food):

    #     if food not in atomics and food not in compounds:
    #         return None
    #     elif food in atomics:
    #         return [{food:1}]
        
    #     paths = []
    #     for i in compounds[food]:
    #         groceries = {}
    #         add_condition = True
    #         new_data = prep_data(i)
    #         new_data.pop(i) 
    #         for j in i:
    #             step = recipes[j[0]]
    #             if step is None:
    #                 add_condition = False
    #                 break

    #             temp = scaled_list(step, j[1])
    #             temp.append(groceries)
    #             groceries = make_grocery_list(temp)
    #         if add_condition:
                
    #             paths.append(groceries)
    #     if len(paths)==0:
    #         return None
    #     return (min(costs),flats[min(costs)])

    # result = recipes(food_item)
        if food not in atomics and food not in compounds:
            return []
        elif food in atomics:
            return [{food:1}]
        
        paths = [] # variable to hold all combinations
        for i in compounds[food]:

            # get variable to hold all of the flattened recipes
            # forma
            temp = []
            for j in i:

                # get combinations of ingredient at j
                # append to a list
                step = flats(j[0])
                if step is not None:
                    local_combo = scaled_list(step, j[1])
                    temp.append(local_combo)

            # then combine these comhinations
            for k in ingredient_mixes(temp):
                paths.append(k)

            # after u get those combinations
        # # out = ingredient_mixes(paths)
        # print(f"this is out {out}")
        return paths
    
    return flats(food_item)


if __name__ == "__main__":
    # load example recipes from section 3 of the write-up
    # with open("test_recipes/example_recipes.pickle", "rb") as f:
    #     example_recipes = pickle.load(f)
    # you are free to add additional testing code here!
    # recipe_data = make_recipe_book(example_recipes)
    # print(recipe_data["burger"])
    # atomic_data = make_atomic_costs(example_recipes)
    # cost = 0
    # for i in atomic_data:
    #     cost+=atomic_data[i]
    # print(cost)
    # count = 0
    # for i in recipe_data:
    #     if len(recipe_data[i])>1:
    #         count+=1
    # print(count)
    # cookie_recipes = [
    # ('compound', 'cookie sandwich', [('cookie', 2), ('ice cream scoop', 3)]),
    # ('compound', 'cookie', [('chocolate chips', 3)]),
    # ('compound', 'cookie', [('sugar', 10)]),
    # ('atomic', 'chocolate chips', 200),
    # ('atomic', 'sugar', 5),
    # ('compound', 'ice cream scoop', [('vanilla ice cream', 1)]),
    # ('compound', 'ice cream scoop', [('chocolate ice cream', 1)]),
    # ('atomic', 'vanilla ice cream', 20),
    # ('atomic', 'chocolate ice cream', 30),
    # ]
    # dairy_recipes = [
    # ('compound', 'milk', [('cow', 2), ('milking stool', 1)]),
    # ('compound', 'cheese', [('milk', 1), ('time', 1)]),
    # ('compound', 'cheese', [('cutting-edge laboratory', 11)]),
    # ('atomic', 'milking stool', 5),
    # ('atomic', 'cutting-edge laboratory', 1000),
    # ('atomic', 'time', 10000),
    # ('atomic', 'cow', 100),
    # ]
    # print(lowest_cost(dairy_recipes,"cheese"))
    # soup = {"carrots": 5, "celery": 3, "broth": 2, "noodles": 1, "chicken": 3, "salt": 10}
    # carrot_cake = {"carrots": 5, "flour": 8, "sugar": 10, "oil": 5, "eggs": 4, "salt": 3}
    # bread = {"flour": 10, "sugar": 3, "oil": 3, "yeast": 15, "salt": 5}
    # grocery_list = [soup, carrot_cake, bread]
    # print(make_grocery_list(grocery_list))
    # print(cheapest_flat_recipe(dairy_recipes,"cheese"))
    # test = prep_data(recipe_data, "burger")
    # print(test)
    pass
    
    