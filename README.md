# LennardJones
Simulation of Lennard-Jones gas. The gas of N atoms is considered. The atoms interact via Van der Waals interaction (repel on short distances, attract on long distances; vanish quite fast). To remove the boundary effects we assume Periodic Boundary Conditions.

Tricks used to make everything faster:
* Leapfrom algorithm (good numerical behaviour)
* Neighbor list (calculating force only in the viscinity of the given particle)
* CUDA: using graphic cards (potential for parallelization)

Program was written in 2013. In 2018 it was roughly cleaned-up and uploaded on gitHub.
It needs a little more of cleaning.
