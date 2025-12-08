import numpy as np
import random
import matplotlib.pyplot as plt

POP_SIZE = 50
GENERATIONS = 80
TOURNAMENT_SIZE = 3

CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.25
MUTATION_STD = 0.5

MIN_KP = 0.0
MAX_KP = 20.0

DT = 0.02          # 50 Hz
SIM_STEPS = 500    # duração (10 segundos)
SETPOINT = 20.0    # cm desejados
ALPHA_EFFORT = 1e-4  # penalidade de esforço PWM


# Substituir pelo modelo
def modelo_identificado(pwm):
    a = 0.02  # cm por unidade PWM
    b = 1.0
    return a * pwm + b

def simular_resposta(kp):
    pos = 0.0     # posição inicial
    tau = 0.1     # constante de tempo aproximada
    alpha = DT / (tau + DT)

    cost = 0.0

    for _ in range(SIM_STEPS):
        erro = SETPOINT - pos

        pwm = kp * erro
        pwm = max(0, min(255, pwm))  # saturação

        # posição estacionária segundo o modelo identificado
        pos_ss = modelo_identificado(pwm)

        # dinâmica de 1ª ordem aproximada
        pos += alpha * (pos_ss - pos)

        # custo: erro + penalidade de esforço
        cost += abs(erro) * DT
        cost += ALPHA_EFFORT * (pwm ** 2) * DT

    return cost

## (fitness = 1/(1+cost))
def evaluate_fitness(kp):
    cost = simular_resposta(kp)
    return 1.0 / (1.0 + cost)

def tournament_selection(pop, fitness):
    competitors = random.sample(list(range(len(pop))), TOURNAMENT_SIZE)
    best = max(competitors, key=lambda i: fitness[i])
    return pop[best]


def crossover(p1, p2):
    if random.random() > CROSSOVER_RATE:
        return p1, p2

    alpha = random.random()
    c1 = alpha * p1 + (1 - alpha) * p2
    c2 = alpha * p2 + (1 - alpha) * p1

    return c1, c2

def mutate(kp):
    if random.random() < MUTATION_RATE:
        kp += random.gauss(0, MUTATION_STD)

    return max(MIN_KP, min(MAX_KP, kp))

def run_ga():
    # população inicial
    population = [random.uniform(MIN_KP, MAX_KP) for _ in range(POP_SIZE)]

    best_kp = population[0]
    best_fit = evaluate_fitness(best_kp)

    history_best = []
    history_mean = []

    for gen in range(GENERATIONS):
        fitness = [evaluate_fitness(kp) for kp in population]

        # guardar o melhor da geração
        gen_best_idx = np.argmax(fitness)
        gen_best_fit = fitness[gen_best_idx]
        gen_best_kp = population[gen_best_idx]

        if gen_best_fit > best_fit:
            best_fit = gen_best_fit
            best_kp = gen_best_kp

        history_best.append(gen_best_fit)
        history_mean.append(np.mean(fitness))

        # elitismo
        new_pop = [best_kp]

        # gerar nova população
        while len(new_pop) < POP_SIZE:
            p1 = tournament_selection(population, fitness)
            p2 = tournament_selection(population, fitness)

            c1, c2 = crossover(p1, p2)
            c1 = mutate(c1)
            c2 = mutate(c2)

            new_pop.append(c1)
            if len(new_pop) < POP_SIZE:
                new_pop.append(c2)

        population = new_pop

        print(f"Geração {gen:3d} | melhor Kp = {gen_best_kp:.4f} | fitness = {gen_best_fit:.6f}")

    return best_kp, history_best, history_mean

if __name__ == "__main__":
    best_kp, best_hist, mean_hist = run_ga()

    print("\nMelhor Kp encontrado:", best_kp)

    # Plot da evolução do fitness
    plt.plot(best_hist, label="Melhor fitness")
    plt.plot(mean_hist, label="Fitness médio")
    plt.xlabel("Geração")
    plt.ylabel("Fitness")
    plt.legend()
    plt.grid()
    plt.show()
