from consolemenu import *
from consolemenu.items import *
import types
import math

assembler_speeds = {1: 0.5, 2: 1, 3: 1.25}
belt_item_s = {"yellow": 15, "red": 30, "blue": 45}
all_items = {"iron_plate", "copper_plate", "green_circuit", "red_circuit", "blue_circuit", "steel", "coal", "brick",
             "stone", "plastic", "sulfur", "acid", "oil", "gear", "yellow_inserter", "yellow_belt", "red_science",
             "green_science", "black_science", "grenade", "yellow_ammo", "red_ammo", "wall", "pipe", "engine",
             "blue_science", "electric_furnace", "red_module", "iron_stick", "rail", "purple_science", "battery",
             "electric_engine", "robot_frame", "low_density_structure", "yellow_science", "accumulator", "radar",
             "solar", "white_science", "lubricant", "rocket_fuel", "copper_wire"}

bus_items = ["iron_plate", "copper_plate", "green_circuit", "red_circuit", "blue_circuit", "steel", "coal", "brick",
             "stone", "plastic", "sulfur", "acid", "oil", "lubricant", "rocket_fuel", "battery"]

red_r = {"time": 5, "copper_plate": 1, "gear": 1}
green_r = {"time": 6, "yellow_inserter": 1, "yellow_belt": 1}
gear_r = {"time": 0.5, "iron_plate": 2}
yellow_ins_r = {"time": 0.5, "green_circuit": 1, "gear": 1, "iron_plate": 1}
yellow_belt_r = {"time": 0.25, "gear": 0.5, "iron_plate": 0.5}

grenade_r = {"time": 8, "coal": 10, "iron_plate": 5} # grenade
yellow_ammo_r = {"time": 1, "iron_plate": 4}
red_ammo_r = {"time": 3, "copper_plate": 5, "yellow_ammo": 1, "steel": 1}
wall_r = {"time": 0.5, "brick": 5}
black_r = {"time": 11.5, "grenade": 0.5, "red_ammo": 0.5, "wall": 1}

pipe_r = {"time": 0.5, "iron_plate": 1}
engine_r = {"time": 10, "gear": 1, "pipe": 2, "steel": 1}
blue_r = {"time": 12, "red_circuit": (3 / 2), "engine": 1, "sulfur": 0.5}

el_furnace_r = {"time": 5, "red_circuit": 5, "steel": 10, "brick": 10}
red_module_r = {"time": 15, "red_circuit": 5, "green_circuit": 5}
iron_stick_r = {"time": 0.25, "iron_plate": 0.5}
rail_r = {"time": 0.25, "iron_stick": 0.5, "steel": 0.5, "stone": 0.5}
purple_r = {"time": 7, "electric_furnace": (1 / 3), "red_module": (1 / 3), "rail": 10}

battery_r = {"time": 4, "copper_plate": 1, "iron_plate": 1, "acid": 20}
el_engine_r = {"time": 10, "green_circuit": 2, "engine": 1, "lubricant": 15}
robot_frame_r = {"time": 20, "battery": 2, "electric_engine": 1, "green_circuit": 3, "steel": 1}
lds_r = {"time": 20, "copper_plate": 20, "plastic": 5, "steel": 2}
yellow_r = {"time": 7, "robot_frame": (1 / 3), "low_density_structure": 1, "blue_circuit": (2 / 3)}

accumulator_r = {"time": 10, "battery": 5, "iron_plate": 2}
radar_r = {"time": 0.5, "green_circuit": 5, "gear": 5, "iron_plate": 10}
solar_r = {"time": 10, "copper_plate": 5, "green_circuit": 15, "steel": 5}
white_r = {"time": (5 / 1000), "accumulator": (1 / 10), "low_density_structure": (1 / 10), "blue_circuit": (1 / 10),
           "radar": (5 / 1000), "rocket_fuel": (1 / 20), "solar": (1 / 10)}

copper_wire_r = {"time": 0.25, "copper_plate": 0.5}
g_circuit_r = {"time": 0.5, "copper_wire": 3, "iron_plate": 1}
r_circuit_r = {"time": 6, "copper_wire": 4, "green_circuit": 2, "plastic": 2}
b_circuit_r = {"time": 10, "red_circuit": 2, "green_circuit": 20, "acid": 5}

get_recipe = {"red_science": red_r, "gear": gear_r, "green_science": green_r, "yellow_inserter": yellow_ins_r,
              "yellow_belt": yellow_belt_r, "grenade": grenade_r, "yellow_ammo": yellow_ammo_r, "red_ammo": red_ammo_r,
              "wall": wall_r, "black_science": black_r, "pipe": pipe_r, "engine": engine_r, "blue_science": blue_r,
              "electric_furnace": el_furnace_r, "red_module": red_module_r, "iron_stick": iron_stick_r, "rail": rail_r,
              "purple_science": purple_r, "battery": battery_r, "electric_engine": el_engine_r,
              "robot_frame": robot_frame_r, "low_density_structure": lds_r, "yellow_science": yellow_r,
              "accumulator": accumulator_r, "radar": radar_r, "solar": solar_r, "white_science": white_r,
              "copper_wire": copper_wire_r, "green_circuit": g_circuit_r, "red_circuit": r_circuit_r,
              "blue_circuit": b_circuit_r
              }


class Assembler:
    def __init__(self, product_id, assembler_level=1):
        self.product_id = product_id
        self.assembler_level = assembler_level


class Cluster:
    def __init__(self, name, output, belt_color="yellow"):
        self.name = name
        self.output = output
        self.assemblers = []
        self.belt_speed = belt_item_s[belt_color]
        self.resource_draw = dict.fromkeys(bus_items, 0)

    def add_draw(self, resource_id, units_s):
        self.resource_draw[resource_id] += units_s

    def add_assembler(self, resource_id, assembler_level=1):
        self.assemblers.append(Assembler(resource_id, assembler_level))

    def __str__(self):
        s = "\n{} Cluster".format(self.name) + "\nOutput: {:.2f}/s {}".format(self.output, self.name) + "\nInputs: "
        for resource in self.resource_draw.keys():
            if self.resource_draw[resource] > 0:
                s += "{:.2f}/s {}, ".format(self.resource_draw[resource], resource)

        curr_prod = ""
        count = 0
        level = 0
        s += "\nAssemblers: "
        for assembler in self.assemblers:
            if assembler.product_id != curr_prod and count != 0:
                s += "{}@lvl{} {}, ".format(count, level, curr_prod)
                count = 0

            count += 1
            level = assembler.assembler_level
            curr_prod = assembler.product_id

        s += "{}@lvl{} {}, ".format(count, level, curr_prod)
        return s


class Factory:

    def __init__(self, assembler_level=3, belt_color="blue"):
        self.assembler_level = assembler_level
        self.craft_speed = assembler_speeds[assembler_level]
        self.belt_speed = belt_item_s[belt_color]
        self.clusters = []

        self.power = 0

    def add_cluster(self, units_m, bussed, target_item):

        if isinstance(units_m, types.FunctionType):
            target_item = target_item()
            units_m = int(units_m())
            bussed = bussed()

        if target_item not in get_recipe:
            print("{} recipe not known - cluster discarded".format(target_item))
            return

        assembly_time = {target_item: get_recipe[target_item]["time"]}

        units_s = units_m / 60

        def calculate_draw(target, quantity, cluster):
            if target not in get_recipe:
                print("{} recipe not known - cluster discarded".format(target))
                return None

            recipe = get_recipe[target]

            for item_name in recipe.keys():
                if item_name == "time":
                    pass
                elif item_name in bussed:
                    cluster.add_draw(item_name, recipe[item_name] * units_s * quantity)
                else:
                    cluster = calculate_draw(item_name, recipe[item_name] * quantity, cluster)
                    if cluster is None:
                        return None
                    assembly_time[item_name] = get_recipe[item_name]["time"] * recipe[item_name]

            return cluster

        new_cluster = calculate_draw(target_item, 1, Cluster(target_item, units_s))

        if new_cluster is not None:
            for name in assembly_time:
                assm_req = math.ceil(((assembly_time[name] * units_s) / self.craft_speed))
                for i in range(assm_req):
                    new_cluster.assemblers.append(Assembler(name, self.assembler_level))
            self.clusters.append(new_cluster)

    def print_report(self):
        total_draw = [0] * len(bus_items)
        for cluster in self.clusters:
            for i in range(len(cluster.resource_draw)):
                total_draw[i] += cluster.resource_draw[bus_items[i]]
            print(cluster)

        print("\n--Total Draw--")
        for i in range(len(total_draw)):
            if total_draw[i] > 0:
                print("{:.2f}/s {}".format(total_draw[i], bus_items[i]))


def prompt_item():
    while True:
        item = input("\nwhich item to produce?"
                     "\n - '[item name]' to select"
                     "\n - 'all' to show available"
                     "\n  >> ")

        if item == 'all':
            print("\nAll items:")
            for i in all_items:
                print(i)
        elif item in all_items:
            return item
        else:
            print("{} not in all items".format(item))
            continue


def prompt_amount():
    while True:
        amount = input("\nhow many items per minute?"
                       "\n  >> ")
        if amount.isnumeric():
            return amount
        else:
            print("please provide a numeric value")
            continue


def prompt_bussed():
    bussed = []
    while True:
        response = input("\nwhich items are being bussed in?"
                         "\n - '[item name]' to add"
                         "\n - 'all' to see all items"
                         "\n - 'list' to see current selection"
                         "\n - 'done' to confirm"
                         "\n  >> ").lower()

        if response == 'done':
            return bussed
        elif response == 'all':
            print("\nAll bussed items:")
            for i in bus_items:
                print(i)
        elif response == 'list':
            print("\nAll selections:")
            for i in bussed:
                print(i)
        elif response not in bus_items:
            print("{} not in bus items".format(response))
            continue
        elif response in all_items and (response not in bussed):
            bussed.append(response)
        else:
            print("{} not in all items".format(response))
            continue
    return bussed


if __name__ == "__main__":
    done = False
    factory = Factory()
    main_menu = ConsoleMenu("Factory Calculator")
    prod_item = FunctionItem("Add Production", factory.add_cluster, [prompt_amount, prompt_bussed, prompt_item])
    print_item = FunctionItem("Print Report", factory.print_report, [])
    main_menu.append_item(prod_item)
    main_menu.append_item(print_item)




    main_menu.show()

