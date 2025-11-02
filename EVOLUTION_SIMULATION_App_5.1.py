import random
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(layout="wide")
st.sidebar.title("Evolution Simulation Controls")
st.sidebar.markdown("### Evolution Simulation")
if st.sidebar.button("🔄 Regenerate Data"):
    st.rerun()

population_size = st.sidebar.slider("Population size", 5, 80, 15)
generations = st.sidebar.slider("Generations", 10, 300, 120)
mutation_rate = st.sidebar.slider("Mutation rate", 0.0, 1.0, 0.2, 0.01)
fitness_type = st.sidebar.selectbox("Fitness function", ["slow", "fast"])

CHANGE_GEN = 30
INITIAL_ENV = 50
NEW_ENV = 80

population = [random.randint(1, 100) for _ in range(population_size)]
all_points = []
for gen in range(1, generations + 1):
    env = INITIAL_ENV if gen <= CHANGE_GEN else NEW_ENV
    fitnesses = []
    for trait in population:
        if fitness_type == "slow":
            fitness = 1 / (1 + abs(env - trait))
        else:
            fitness = (env - abs(env - trait)) / env
            fitness = max(fitness, 0)
        fitnesses.append(fitness)
    if sum(fitnesses) == 0:
        fitnesses = [1.0] * len(fitnesses)
    parents = random.choices(population, weights=fitnesses, k=population_size)
    new_pop = []
    for parent in parents:
        if random.random() < mutation_rate:
            child = parent + random.randint(-5, 5)
        else:
            child = parent
        child = max(1, min(100, int(child)))
        new_pop.append(child)
    population = new_pop
    all_points.extend([(gen, trait) for trait in population])

fig, ax = plt.subplots(figsize=(10, 6))
if all_points:
    xs, ys = zip(*all_points)
    ax.scatter(xs, ys, s=18, alpha=0.75, color='blue', label='Individuals')

left_x = list(range(0, min(CHANGE_GEN, generations) + 1))
left_y = [INITIAL_ENV] * len(left_x)
ax.plot(left_x, left_y, 'r--', linewidth=2)

if generations >= CHANGE_GEN:
    ax.plot([CHANGE_GEN, CHANGE_GEN], [INITIAL_ENV, NEW_ENV], 'r--', linewidth=2)
    right_x = list(range(CHANGE_GEN, generations + 1))
    right_y = [NEW_ENV] * len(right_x)
    ax.plot(right_x, right_y, 'r--', linewidth=2, label='Ideal Trait')

ax.set_xlim(0, generations)
ax.set_ylim(0, 100)
ax.set_xlabel("Generation")
ax.set_ylabel("Trait Value")
ax.set_title("Evolution Simulation")
ax.legend(loc='upper left')
st.pyplot(fig)
