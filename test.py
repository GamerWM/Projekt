from simulator import Simulator
import plot

sim1 = Simulator(10, 10, -10, 50)
sim2 = Simulator(30, 10, -10, 50)

road = [[0, 750], [243, 483], [703, 483], [931, 745]]

sim1.simulate(road)
sim2.simulate(road)


plot.plot([sim1, sim2])