import csv
import json
import recommender
# def read_file():
#   df = pd.read_csv("./skill2vec_50K.csv")
#   for index,row in df.take(2).iterrows():
#     print(row.tolist())

def read_file():
    dataset = []
    case_pair = dict()
    with open("./skill2vec_50K.csv", "r") as file:
        data = csv.reader(file)
        # take = 1_000
        for rows in data:
            # print("take = ", take)
            # take = take - 1
            # if take == 0:
            #     break;
            cleaned =  list(filter(lambda x: x is not None and x.strip() != "", rows))
            item = []
            for row in cleaned[1:]:
                if row.lower() not in case_pair:
                    case_pair[row.lower()] = row
                item.append(row.lower())
            dataset.append(item)
    return dataset, case_pair

def pair_data(data: list[list[str]]):
    # factor
    # pairing
    skill_factors = dict()
    ## {str : {str: number}}

    # [ [a,b,c, d], [e,f,g,h] ]
    for row in data:
        # [a,b,c,d]
        # {a : {b:1, c:1,d:1}}
        for skill in row:
            if skill not in skill_factors:
                skill_factors[skill] = dict()
            for key in row:
                if key != skill:
                    if key not in skill_factors[skill]:
                        skill_factors[skill][key] = 1
                    else:
                        skill_factors[skill][key] += 1 

    return skill_factors
                        


def run():
    data, case_pair = read_file()
    result = pair_data(data)
    # print(result)
    with open("./new_factors.json", "w") as fp:
        json.dump(result, fp)
    
    with open("./case_pair.json", "w") as pair_file:
        json.dump(case_pair, pair_file)

run()