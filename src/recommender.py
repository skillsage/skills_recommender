import json
import psycopg2 as pg

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
    postgres_url = "postgresql://localhost:5432/skill_sage?user=admin&password=admin"
    conn = pg.connect(postgres_url)
    conn.autocommit = True
    cur =  conn.cursor()    

    fq = f"""
    SELECT skill, factor from skill_factors WHERE skill IN %s LIMIT 1;
    """
    cur.execute(fq, (tuple(skills),))
    factor_records = cur.fetchall()
    factors : dict[str, dict[str, int]] = dict()
    for item in factor_records:
        if item is not None:
            factors[item[0]] = item[1]
        
    pairs = dict()
    for skill in skills:
        if skill not in factors:
            continue
        for k, v in factors[skill].items():
            # key = skill, value = factor
            if k not in pairs:
                pairs[k] = node()
                pairs[k].add(v)
            else:
                pairs[k].add(v)
    

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
    pq = f"""
        SELECT name FROM skills WHERE lower IN %s;
    """
    cur.execute(pq, (tuple(clean),))
    pair_records = cur.fetchall()
    return list(map(lambda x: x[0] ,pair_records))

print(recommend(["javascript", "html", "jquery", "csss"]))