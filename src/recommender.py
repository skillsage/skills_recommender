import json


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


def recommend(skills: list[str], take: int = 20):
    f = open("new_factors.json")
    factors = json.load(f)
    pairs = open("case_pair.json")
    case_pair = json.load(pairs)
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

    result =  list(
        map(
            lambda x: x["skill"],
            sorted(pair_list, key=lambda x: x["average"], reverse=True),
        )
    )

    clean = list(filter(lambda x: x not in skills, result))[:take]
    return list(map(lambda x : case_pair[x],clean))

# skills
# lower, cased
# lowercase, Correct Case

# skill_factors
# skill, factors: {asdasd: 23, asdasd: 34534}

print(recommend(["reactjs", "javascript", "css"]))