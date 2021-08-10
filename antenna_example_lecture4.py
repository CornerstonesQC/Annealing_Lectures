# Copyright [yyyy] [name of copyright owner]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Import networkx for graph tools
import networkx as nx

# Import matplotlib.pyplot to draw graphs on screen
import matplotlib

matplotlib.use("agg")
import matplotlib.pyplot as plt

# Import the Ocean tools we're going to use
import dimod
from dwave.system import DWaveSampler, EmbeddingComposite
import dwave.inspector as inspector


def visualize_results(S):
    # Visualize the results
    k = G.subgraph(S)
    notS = list(set(G.nodes()) - set(S))
    othersubgraph = G.subgraph(notS)
    pos = nx.spring_layout(G)
    plt.figure()

    # Save original problem graph
    original_name = "antenna_plot_original.png"
    nx.draw_networkx(G, pos=pos, with_labels=True)
    plt.savefig(original_name, bbox_inches='tight')

    # Save solution graph
    # Note: red nodes are in the set, blue nodes are not
    solution_name = "antenna_plot_solution.png"
    nx.draw_networkx(k, pos=pos, with_labels=True, node_color='r', font_color='k')
    nx.draw_networkx(othersubgraph, pos=pos, with_labels=True, node_color='b', font_color='w')
    plt.savefig(solution_name, bbox_inches='tight')

    print("Your plots are saved to {} and {}".format(original_name, solution_name))


if __name__ == "__main__":
    # 1. Define sampler
    sampler = EmbeddingComposite(DWaveSampler())

    # 2. Define problem
    gamma = 2

    # Create empty graph
    G = nx.Graph()

    # Add edges to graph - this also adds the nodes
    G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6), (6, 7)])

    # Create a BQM object
    bqm = dimod.BQM('BINARY')

    # Add linear biases
    bqm.add_variables_from({node: -1 for node in G.nodes})

    # Add quadratic biases
    bqm.add_interactions_from({(u, v): gamma for u, v in G.edges})

    # 3. Submit problem and parameters to the solver
    sampleset = sampler.sample(bqm, num_reads=50)

    # 4. Evaluate the solution
    sample = next(iter(sampleset))
    subset = [node for node in sample if sample[node] > 0]

    print(sampleset)
    print('Maximum independent set size found is', len(subset))
    visualize_results(subset)

