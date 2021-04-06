from consolemenu import *
from consolemenu.items import *
import types
import math

# todo recalculate 60spm.
# todo add chemical recipes
# todo add smelting recipes
# todo add drill speeds
# todo add multi-output recipes
# todo add multi-product clusters

assembler_speeds = {"assembly_1": 0.5, "assembly_2": 1, "assembly_3": 1.25, "chemical_plant": 1, "refinery": 1, "silo": 2}
belt_item_s = {"yellow": 15, "red": 30, "blue": 45}
all_items = {"iron_plate", "copper_plate", "green_circuit", "red_circuit", "blue_circuit", "steel", "coal", "brick",
             "stone", "plastic", "sulfur", "acid", "oil", "gear", "yellow_inserter", "yellow_belt", "red_science",
             "green_science", "black_science", "grenade", "yellow_ammo", "red_ammo", "wall", "pipe", "engine",
             "blue_science", "electric_furnace", "red_module", "iron_stick", "rail", "purple_science", "battery",
             "electric_engine", "robot_frame", "low_density_structure", "yellow_science", "accumulator", "radar",
             "solar", "white_science", "lubricant", "rocket_fuel", "copper_wire", "petroleum"}

bus_items = ["iron_plate", "copper_plate", "green_circuit", "red_circuit", "blue_circuit", "steel", "coal", "brick",
             "stone", "plastic", "sulfur", "acid", "oil", "lubricant", "rocket_fuel", "battery", "petroleum"]

red_r = {"time": 5, "machine": "assembly", "copper_plate": 1, "gear": 1}
green_r = {"time": 6, "machine": "assembly", "yellow_inserter": 1, "yellow_belt": 1}
gear_r = {"time": 0.5, "machine": "assembly", "iron_plate": 2}
yellow_ins_r = {"time": 0.5, "machine": "assembly", "green_circuit": 1, "gear": 1, "iron_plate": 1}
yellow_belt_r = {"time": 0.25, "machine": "assembly", "gear": 0.5, "iron_plate": 0.5}

grenade_r = {"time": 8, "machine": "assembly", "coal": 10, "iron_plate": 5} # grenade
yellow_ammo_r = {"time": 1, "machine": "assembly", "iron_plate": 4}
red_ammo_r = {"time": 3, "machine": "assembly", "copper_plate": 5, "yellow_ammo": 1, "steel": 1}
wall_r = {"time": 0.5, "machine": "assembly", "brick": 5}
black_r = {"time": 11.5, "machine": "assembly", "grenade": 0.5, "red_ammo": 0.5, "wall": 1}

pipe_r = {"time": 0.5, "machine": "assembly", "iron_plate": 1}
engine_r = {"time": 10, "machine": "assembly", "gear": 1, "pipe": 2, "steel": 1}
blue_r = {"time": 12, "machine": "assembly", "red_circuit": (3 / 2), "engine": 1, "sulfur": 0.5}

el_furnace_r = {"time": 5, "machine": "assembly", "red_circuit": 5, "steel": 10, "brick": 10}
red_module_r = {"time": 15, "machine": "assembly", "red_circuit": 5, "green_circuit": 5}
iron_stick_r = {"time": 0.25, "machine": "assembly", "iron_plate": 0.5}
rail_r = {"time": 0.25, "machine": "assembly", "iron_stick": 0.5, "steel": 0.5, "stone": 0.5}
purple_r = {"time": 7, "machine": "assembly", "electric_furnace": (1 / 3), "red_module": (1 / 3), "rail": 10}

battery_r = {"time": 4, "machine": "assembly", "copper_plate": 1, "iron_plate": 1, "acid": 20}
el_engine_r = {"time": 10, "machine": "assembly", "green_circuit": 2, "engine": 1, "lubricant": 15}
robot_frame_r = {"time": 20, "machine": "assembly", "battery": 2, "electric_engine": 1, "green_circuit": 3, "steel": 1}
lds_r = {"time": 20, "machine": "assembly", "copper_plate": 20, "plastic": 5, "steel": 2}
yellow_r = {"time": 7, "machine": "assembly", "robot_frame": (1 / 3), "low_density_structure": 1, "blue_circuit": (2 / 3)}

accumulator_r = {"time": 10, "machine": "assembly", "battery": 5, "iron_plate": 2}
radar_r = {"time": 0.5, "machine": "assembly", "green_circuit": 5, "gear": 5, "iron_plate": 10}
solar_r = {"time": 10, "machine": "assembly", "copper_plate": 5, "green_circuit": 15, "steel": 5}
white_r = {"time": (5 / 1000), "machine": "assembly", "accumulator": (1 / 10), "low_density_structure": (1 / 10), "blue_circuit": (1 / 10),
           "radar": (5 / 1000), "rocket_fuel": (1 / 20), "solar": (1 / 10)}
# todo white_r should be satellite

copper_wire_r = {"time": 0.25, "machine": "assembly", "copper_plate": 0.5}
g_circuit_r = {"time": 0.5, "machine": "assembly", "copper_wire": 3, "iron_plate": 1}
r_circuit_r = {"time": 6, "machine": "assembly", "copper_wire": 4, "green_circuit": 2, "plastic": 2}
b_circuit_r = {"time": 10, "machine": "assembly", "red_circuit": 2, "green_circuit": 20, "acid": 5}

plastic_r = {"time": 0.5, "machine": "chemical_plant", "coal": 0.5, "petroleum": 10}

get_recipe = {"red_science": red_r, "gear": gear_r, "green_science": green_r, "yellow_inserter": yellow_ins_r,
              "yellow_belt": yellow_belt_r, "grenade": grenade_r, "yellow_ammo": yellow_ammo_r, "red_ammo": red_ammo_r,
              "wall": wall_r, "black_science": black_r, "pipe": pipe_r, "engine": engine_r, "blue_science": blue_r,
              "electric_furnace": el_furnace_r, "red_module": red_module_r, "iron_stick": iron_stick_r, "rail": rail_r,
              "purple_science": purple_r, "battery": battery_r, "electric_engine": el_engine_r,
              "robot_frame": robot_frame_r, "low_density_structure": lds_r, "yellow_science": yellow_r,
              "accumulator": accumulator_r, "radar": radar_r, "solar": solar_r, "white_science": white_r,
              "copper_wire": copper_wire_r, "green_circuit": g_circuit_r, "red_circuit": r_circuit_r,
              "blue_circuit": b_circuit_r, "plastic": plastic_r
              }





class Assembler:
    def __init__(self, product_id, assembler):
        self.product_id = product_id
        self.assembler = assembler


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
        machine = ""
        s += "\nAssemblers: "
        for assembler in self.assemblers:
            if assembler.product_id != curr_prod and count != 0:
                s += "{}@{} {}, ".format(count, machine, curr_prod)
                count = 0

            count += 1
            machine = assembler.assembler
            curr_prod = assembler.product_id

        s += "{}@{} {}, ".format(count, machine, curr_prod)
        return s


class Factory:

    def __init__(self, assembler_level="assembly_3", belt_color="blue"):
        self.assembler_level = assembler_level
        self.craft_speed = assembler_speeds[assembler_level]
        self.belt_speed = belt_item_s[belt_color]
        self.clusters = []

        self.power = 0

    def set_assembler(self, assembler_level):
        if isinstance(assembler_level, types.FunctionType):
            assembler_level = assembler_level()

        self.assembler_level = assembler_level

    def machine_translate(self, machine_name):
        if machine_name == "assembly":
            return self.assembler_level
        else:
            return machine_name

    def add_cluster(self, units_m, bussed, target_item):

        if isinstance(units_m, types.FunctionType):
            target_item = target_item()
            units_m = int(units_m())
            bussed = bussed()

        if target_item not in get_recipe:
            print("{} recipe not known - cluster discarded2".format(target_item))
            return

        units_s = units_m / 60

        def calculate_draw(target, quantity, cluster):
            if target not in get_recipe:
                print("{} recipe not known - cluster discarded1".format(target))
                return None
            time_cost = get_recipe[target]["time"]
            item_quantity = quantity
            craft_machine = self.machine_translate(get_recipe[target]["machine"])
            speed = assembler_speeds[craft_machine]
            assembler_cost = math.ceil((time_cost * item_quantity * cluster.output) / speed)
            for a in range(assembler_cost):
                cluster.assemblers.append(Assembler(target, craft_machine))

            recipe = get_recipe[target]

            for item_name in recipe.keys():
                if item_name == "time":
                    pass
                elif item_name == "machine":
                    pass
                elif item_name in bussed:
                    cluster.add_draw(item_name, recipe[item_name] * cluster.output * quantity)
                else:
                    cluster = calculate_draw(item_name, recipe[item_name] * quantity, cluster)
                    if cluster is None:
                        return None

            return cluster

        new_cluster = calculate_draw(target_item, 1, Cluster(target_item, units_s))

        if new_cluster is not None:
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


def prompt_level():
    while True:
        level = input("what assembler level (1, 2, 3)?")
        if level.isdecimal():
            level_num = int(level)
            if level_num == 1:
                return "assembly_1"
            elif level_num == 2:
                return "assembly_2"
            elif level_num == 3:
                return "assembly_3"
            else:
                print("1, 2, or 3 only")
                continue
        else:
            print("Only accepts numbers (1, 2, 3)")
            continue


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
    tech_item = FunctionItem("Set Assembler Level", factory.set_assembler, [prompt_level])
    main_menu.append_item(prod_item)
    main_menu.append_item(tech_item)
    main_menu.append_item(print_item)




    main_menu.show()

