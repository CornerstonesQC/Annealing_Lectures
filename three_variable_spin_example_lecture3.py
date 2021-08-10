# Copyright 2021 D-Wave Systems Inc.
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

import dimod
from dwave.system import DWaveSampler, EmbeddingComposite

# 1. Define sampler
sampler = EmbeddingComposite(DWaveSampler(solver={'topology__type': 'chimera'}))

# 2. Define problem: anti-ferromagnetic chain
#       E = a*b + b*c + c*a
bqm = dimod.BQM({}, {'ab': 1, 'bc': 1, 'ca': 1}, 0, 'SPIN')

# 3. Submit problem and parameters to the solver
sampleset = sampler.sample(bqm, num_reads=10)

# 4. Evaluate the solution
print(sampleset)