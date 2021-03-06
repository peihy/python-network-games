 # -*- coding: utf-8 -*-
from Simulation.Simulations import *
from Agent.Agents import *
import pylab as plt
import itertools
from statistics import mean, median, mode, stdev

DRAW_SIM = True
DRAW_PS = DRAW_SIM
GRAPH_PS = True

draw_scale = 50
print_scale = draw_scale
graph_scale = print_scale

# One of these should always be 1
play_scale = 1
rewire_scale = 1

N = 20
T = 1000

if __name__ == "__main__":
	sim = SM(N=N)
	peoples = {}
	cc = ([],[])

	if GRAPH_PS:
		ps = {'AVG': ([],[])}

	if DRAW_PS:
		plt.figure('p-boxplots')
		plt.show(block=False)

	for t in xrange(T): #itertools.count(0):
		if t % play_scale == 0:
			sim.play(t=t)

		if t % rewire_scale == 0:
			sim.rewire(t=t)

		if DRAW_SIM and t % draw_scale == 0:
			if DRAW_PS:
				info = sim.get_info()
				pees = info['agent_information']['p']
				plt.figure('p-boxplots')
				plt.clf()
				(keys, values) = (pees.keys(), pees.values())
				keys.append('Whole-Population')
				values.append([reduce(lambda x,y: x+y,pees.values())])
				plt.boxplot(x=values, labels=keys, showmeans=True)
				
				plt.ylabel('p-values')
				plt.xlabel('Agent Types')
				
				plt.ylim([-.2,3])
				plt.draw()

			sim.draw(t=t)

		if  t % print_scale == 0:
			print t

		if t % graph_scale == 0:
			info = sim.get_info()
			counts = info['agent_information']['count']

			for (k, v) in counts.items():
				if k in peoples:
					peoples[k][1].append(counts[k])
					peoples[k][0].append(t)
				else:
					peoples[k] = ([t],[counts[k]])

			cc[0].append(t)
			cc[1].append(info['cc'])
			

			if GRAPH_PS:
				pees = info['agent_information']['p']
				avg_p = mean(reduce(lambda x,y: x+y,pees.values()))

				ps['AVG'][0].append(t)
				ps['AVG'][1].append(avg_p)
				
				for (k, v) in pees.items():
					if k in ps:
						ps[k][1].append(mean(v))
						ps[k][0].append(t)
					else:
						ps[k] = ([t],[mean(v)])

			# print info['agent_information']['count'], info['cc'],mean(reduce(lambda x,y: x+y,ps.values())),  str(t)


	plt.close("all")

	fig = plt.figure('Final Results')

	ax1 = fig.add_subplot(311 if GRAPH_PS else 211)
	for (k, v) in peoples.items():
		c = 'b' if k == 'C' else 'r' if k == 'D' else (random.random(), random.random(), random.random())
		ax1.plot(*v, color=c, label=k)
	ax1.legend(prop={'size':11})
	ax1.set_ylabel('Population')

	if GRAPH_PS:
		ax2 = fig.add_subplot(312)
		for (k, v) in ps.items():
			c = 'b' if k == 'C' else 'r' if k == 'D' else (random.random(), random.random(), random.random())
			ax2.plot(*v, color=c, label=k)
		ax2.legend(prop={'size':10})
		ax2.set_xlabel('time')
		ax2.set_ylabel('average-p')

	ax3 = fig.add_subplot(313 if GRAPH_PS else 212)	
	ax3.plot(*cc, color='k')
	ax3.set_xlabel('t')
	ax3.set_ylabel('Clustering Coefficient')
	
	plt.show(block=True)

