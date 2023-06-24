import json

f = open("skill_factors.json")
factors = json.load(f)
f.close()

test_skills = ["javascript", "js", "typescript", "angularjs"]


class node:
    factor = 0
    rep = 0

    def __init__(self):
        pass

    def add(self, ft):
        self.rep += 1
        self.factor += ft

    def average(self):
        return self.factor // self.rep

    def __repr__(self):
        return str(self.average())


def recommend(skills):
    pairs = dict()
    for skill in skills:
        if skill not in factors:
            pass
        for k, v in factors[skill].items():
            # key = skill, value = factor
            if k not in pairs:
                pairs[k] = node()
                pairs[k].add(v)
            else:
                pairs[k].add(v)
    # here
    # [{"sdsd": factor}]
    pair_list = list()
    for k, v in pairs.items():
        pair_list.append({"skill": k, "average": v.average()})

    return list(
        map(
            lambda x: x["skill"],
            sorted(pair_list, key=lambda x: x["average"], reverse=True),
        )
    )[0:20]


print(recommend(test_skills))