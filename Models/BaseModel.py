
class BaseModel:
    def __init__(self, nteams, costs, entera, **kwargs) :
        assert costs.shape == (nteams, nteams, nteams-1), "Incorrect dimensions"
        self.model = None
        self.nteams = nteams
        self.nrounds = nteams -1
        self.costs = costs

        self._build(entera)

    def _build(self, entera):
        raise NotImplementedError("La clase derivada debe implementar el metodo _build")

    def optimize(self):
        self.model.optimize()
        #self.model.printStatistics()

    def get_objval(self):
        return self.model.getObjVal()

    def free(self):
        self.model.freeProb()

    def get_nonzero_vars(self):
        raise NotImplementedError("La clase derivada debe implementar el metodo get_nonzero_vars")
