# Orders Dynamic Simulation

This repository implements a dynamic simulation of order processing and inventory management using Python and Dash. The simulation models order flows, inventory depletion, replenishment, and prioritization with real-time visualizations.

## Core Components

### Order Class

Each order consists of:
- Three materials (`M1`, `M2`, `M3`) with randomly assigned quantities
- A unique ID
- Time in system (initially set to 2)
- Dynamic priority value

Orders are generated with a constrained random distribution:
```python
def generate_random_items(self):
    x1 = random.randint(0, 100) + 1
    x2 = random.randint(0, 100 - x1) + 1
    x3 = 100 - x1 - x2 + 1
    
    # randomly shuffle x1, x2, x3
    items = [x1, x2, x3]
    random.shuffle(items)
    self.items["M1"], self.items["M2"], self.items["M3"] = items
```

This ensures that the total quantity always sums to 100+3 units, while distributing them randomly across the three materials.

### Storage Class

The storage system manages:
- Inventory levels for each material
- Active orders
- System event logs
- Demand history

Initial storage setup:
- M1: 200 units with 20-hour lifespan each
- M2: 300 units with 50-hour lifespan each  
- M3: 500 units with 100-hour lifespan each

## Mathematical Model

### Priority Calculation

The priority of an order is calculated using a weighted formula:
```python
priority = (M1 * 3 + M2 * 2 + M3) * np.log10(time + 2)
```

This formula has two key components:

1. **Material Weighting**: `M1 * 3 + M2 * 2 + M3`
   - M1 is weighted highest (3x)
   - M2 has medium weight (2x)
   - M3 has base weight (1x)
   
2. **Time Factor**: `np.log10(time + 2)`
   - Logarithmic scaling ensures priority grows with time but at a decreasing rate
   - The +2 offset ensures positive values from the start (since log10(1) = 0)
   - This prevents starvation of older orders by gradually increasing their priority

The system always processes the highest priority order at each simulation step, creating a dynamic scheduling mechanism that balances material importance with waiting time.

### Inventory Management

The storage system uses a time-based inventory model:

1. **Storage Representation**:
   - Each unit in storage has a remaining lifetime counter
   - Example: `M1: [20, 20, 20, ...]` represents 3 units with 20 hours remaining
   
2. **Time Progression**:
   - At each time increment, all counters decrease by 1
   - `[20, 20, 20]` → `[19, 19, 19]`
   
3. **Replenishment Logic**:
   - If inventory count falls below 5 units for any material, replenishment occurs
   - M1: Adds 100 units with 20-hour lifespan
   - M2: Adds 100 units with 50-hour lifespan
   - M3: Adds 100 units with 100-hour lifespan

4. **Order Processing**:
   - When an order is satisfied, inventory is reduced by the order quantities
   - Implementation uses array slicing to efficiently remove inventory:
   ```python
   self.storage[material] = self.storage[material][quantity:]
   ```

### Demand Generation

At each time step, the system randomly generates 0-3 new orders:
```python
def generate_n_orders(self):
    n = np.random.randint(0, 4) 
    for i in range(n):
        self.add_order(Order(f"{self.time}-{len(self.orders)+1}"))
    return True
```

This creates variable demand patterns that stress-test the inventory management system.

## Simulation Cycle

Each simulation step follows this sequence:

1. **Time Increment**
   - Increase simulation time counter
   - Age all inventory units (decrease time remaining)
   - Update order priorities
   
2. **Order Generation**
   - Create random new orders (0-3)
   
3. **Inventory Check**
   - Check if any material is below threshold (5 units)
   - Replenish if necessary
   
4. **Order Processing**
   - Find highest priority order
   - Ensure sufficient inventory (replenish if needed)
   - Remove order from queue
   - Decrease inventory
   
5. **Data Collection**
   - Update logs
   - Track demand and supply patterns

## Visualization

The Dash web application provides several real-time visualizations:

- **Demand Trends**: Line charts tracking demand patterns over time
- **Inventory Levels**: Visualizing current stock and historical trends 
- **Time to Stockout**: Bar chart showing estimated hours until inventory depletion
- **System Log**: Running display of system events

## Key Features

- **Dynamic Priority System**: Orders gain importance with age, preventing starvation
- **Material Weighting**: Different materials have different priority weights
- **Time-Based Inventory**: Units age over time, simulating perishable goods
- **Reactive Replenishment**: System orders new stock only when needed
- **Stochastic Demand**: Random order generation creates realistic variability

## Running the Simulation

1. Install the required packages:
```bash
pip install dash dash-bootstrap-components plotly pandas numpy
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to http://localhost:8080

## Conclusion

This simulation provides a simplified but insightful model of order fulfillment dynamics with time-sensitive inventory. The priority-based ordering system demonstrates how mathematical models can optimize resource allocation in supply chain management.
