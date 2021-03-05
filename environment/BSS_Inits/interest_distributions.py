from environment.BSS_Inits.matrix_creation import MatrixCreator
import pickle as pkl

'''

:author: Matthew Schofield
:version: 1.10.2021
'''

class InterestDistributions:

    def __init__(self):
        self.matrix_creator = MatrixCreator()

    def generate(self, system_size, specification):
        interest_distribution_output = [[] for _ in range(24)]
        for k in specification.keys():
            indices = k.split("-")
            start_ind = int(indices[0])
            end_ind = int(indices[1])
            spec = specification[k]
            for i in range(start_ind, end_ind):
                if spec == "Gauss":
                    interest_distribution_output[i] = self.matrix_creator.makeGaussianMatrix(system_size, 1)
                elif spec == "Inv Gauss":
                    interest_distribution_output[i] = self.matrix_creator.makeInvGaussianMatrix(system_size, 1)
                elif spec == "Uniform":
                    interest_distribution_output[i] = self.matrix_creator.makeUniformMatrix(system_size)
        normalized_matrices = [self.matrix_creator.normalizeMatrix(system_size, distrib) for distrib in interest_distribution_output]
        return [self.matrix_creator.flatten(system_size, distrib) for distrib in normalized_matrices]

    def generate_from_pkls(self, system_size, specifications):
        interest_distribution_output = [[] for _ in range(24)]
        for i, file in enumerate(specifications):
            distrib = pkl.load(open(file, 'rb'))
            interest_distribution_output[i] = distrib

        normalized_matrices = [self.matrix_creator.normalizeMatrix(system_size, distrib) for distrib in interest_distribution_output]
        return [self.matrix_creator.flatten(system_size, distrib) for distrib in normalized_matrices]





