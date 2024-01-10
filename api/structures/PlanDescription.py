from api.structures.InsuredItem import PlanKind


class PlanDescription:
    __plan_type: PlanKind = None
    __description: str = None
    __mean_cost: float = None  # monthly cost, scale with duration of subscription (monthly, quarterly, yearly payments)

    def __init__(self, data):
        self.__plan_type = PlanKind[data.get("plan_type")]
        self.__description = data.get('description')
        self.__mean_cost = data.get("mean_cost")

    def __iter__(self):
        yield "plan_type", self.__plan_type
        yield "description", self.__description
        yield "mean_cost", self.__mean_cost

    def get_plan_type(self):
        return self.__plan_type

    def get_description(self):
        return self.__description

    def get_mean_cost(self):  # TODO: auto scale with monthly, quarterly, yearly
        return self.__mean_cost
