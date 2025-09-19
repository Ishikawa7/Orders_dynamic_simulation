import numpy as np
import random

# defining Order class
class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.items = {
            "M1": 0,
            "M2": 0,
            "M3": 0,
        }
        self.generate_random_items()
        self.time = 2
        self.priority = 0
        self.priority = self.calculate_priority()

    def __repr__(self):
        return f"Order({self.order_id}, {self.items}, {self.priority}, {self.time})"

    def calculate_priority(self):
        self.priority = (self.items["M1"] * 3 + self.items["M2"] * 2 + self.items["M3"]) * np.log10(self.time + 2)

    def generate_random_items(self):
        x1 = random.randint(0, 100+1) + 1
        x2 = random.randint(0, 100 - x1+2) + 1
        x3 = 100 - x1 - x2 + 3

        # randomly shuffle x1, x2, x3
        items = [x1, x2, x3]
        random.shuffle(items)
        self.items["M1"], self.items["M2"], self.items["M3"] = items

# define storage class
class Storage:
    def __init__(self):
        self.storage = {
            "M1": [20 for _ in range(200)],
            "M2": [50 for _ in range(300)],
            "M3": [100 for _ in range(500)],
        }
        self.storage_count = {
            "M1": [200],
            "M2": [300],
            "M3": [500],
        }
        self.orders = []
        self.time = 0
        self.log = []
        self.demand = {
            "M1": [],
            "M2": [],
            "M3": [],
        }

    def add_order(self, order):
        self.orders.append(order)
        self.log.append("Added order: " + str(order))
        for material, quantity in order.items.items():
            self.demand[material].append(quantity)
        # keep only last 100 demand entries
        for material in self.demand:
            if len(self.demand[material]) > 100:
                self.demand[material] = self.demand[material][-100:]
        # keep only last 100 log entries
        if len(self.log) > 100:
            self.log = self.log[-100:]
        # keep only last 100 orders
        if len(self.orders) > 100:
            self.orders = self.orders[-100:]

    def increment_time(self):
        self.time += 1
        self.generate_n_orders()
        if self.time % 24 == 0:
            self.time = 0  # reset time every 24 hours
        for order in self.orders:
            order.time += 1
            order.calculate_priority()
        for material in self.storage:
            self.storage[material] = [x - 1 for x in self.storage[material]]
        # check if any material is below 5, if yes replenish it
        for material in self.storage:
            if len(self.storage[material]) < 5:
                self.replenish_material(material)

    def get_highest_priority_order(self):
        if not self.orders:
            return None
        return max(self.orders, key=lambda o: o.priority)

    def remove_order(self, order):
        self.log.append("Removed order: " + str(order))
        self.storage_count['M1'].append(self.storage_count["M1"][-1])
        self.storage_count['M2'].append(self.storage_count["M2"][-1])
        self.storage_count['M3'].append(self.storage_count["M3"][-1])
        for material, quantity in order.items.items():
            self.storage[material] = self.storage[material][quantity:]
            self.storage_count[material][-1] -= quantity
        self.orders.remove(order)

    def replenish_material(self, material):
        material_time = {"M1": 20, "M2": 50, "M3": 100}
        material_quantity = {"M1": 100, "M2": 100, "M3": 100}
        self.storage_count['M1'].append(self.storage_count["M1"][-1])
        self.storage_count['M2'].append(self.storage_count["M2"][-1])
        self.storage_count['M3'].append(self.storage_count["M3"][-1])
        if material in self.storage:
            self.storage[material].extend([material_time[material] for _ in range(material_quantity[material])])
            self.storage_count[material][-1] += material_quantity[material]
            self.log.append(f"Replenished {material} by {material_quantity[material]} units.")
            self.increment_time()

    def satisfy_order(self, order):
        top_priority_order = self.get_highest_priority_order()
        if top_priority_order != None:
            for material, quantity in top_priority_order.items.items():
                if len(self.storage[material]) < quantity:
                    self.replenish_material(material)
        self.remove_order(order)
        self.log.append("Satisfied order: " + str(order))
        self.increment_time()
        return True

    def generate_n_orders(self):
        n = np.random.randint(0, 4) 
        for i in range(n):
            self.add_order(Order(str(self.time)))
        return True
    
    def run_simulation_step(self, new_orders=[]):
        self.increment_time()
        for order in new_orders:
            self.add_order(order)
        top_priority_order = self.get_highest_priority_order()
        if top_priority_order:
            self.satisfy_order(top_priority_order)
        else:
            self.log.append("No orders to process.")