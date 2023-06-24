import pandas as pd

import json


def _map(data, func):
    return list(map(func, data))


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def _filter(data, func):
    return list(filter(func, data))


def _dict_filter(data, func):
    return dict(filter(func, data))


def _clean_list(ls):
    return _filter(_map(ls, lambda x: x.strip()), lambda y: len(y) > 0)


def _contains(v, k):
    return v.find(k) != -1


def _split_and_clean(data: list):
    r = []
    for i in data:
        r.extend(_clean_list(clean_entry(i.strip())))
    return r


def clean_entry(skill: str):
    if len(skill.strip()) < 2:
        return []

    if len(skill.split("/ ")) == 2:
        return _split_and_clean(skill.split("/ "))

    # remove numbers

    if skill.isnumeric() or is_float(skill):
        return []

    ## - aws

    ## listview...........

    # HTML5; CSS; JSON; JQuery; AngularJS

    # "Big Data":Spark:"data warehouse":"data model":AWS

    if _contains(skill, '"'):
        new_str = skill.replace('"', "")

        return clean_entry(new_str)

    # Load/Testing Performance

    if _contains(skill, "/") and _contains(skill, " ") and len(skill.split(" ")) == 2:
        s1 = skill.split(" ")

        if _contains(s1[1], "/"):
            return _split_and_clean(s1)

        suffix = s1[1]
        return _split_and_clean(_map(s1[0].split("/"), lambda x: x + " " + suffix))

    remove_list = [
        "see below",
        "video",
        "use case",
        "etc",
        "sales",
        "project",
        "when",
    ]
    for r in remove_list:
        if r.strip() == skill.strip():
            return []

    ## handle dots
    if skill.endswith("."):
        return clean_entry(skill.rstrip("."))

    # ends
    ends = [" and", " or", " etc", "+"]
    for v in ends:
        if skill.endswith(v):
            return _split_and_clean(skill.rstrip(v))

    ## starts
    starts = ["and ", "or ", " -", "on "]
    for v in starts:
        if skill.startswith(v):
            return _split_and_clean(skill.lstrip(v))

    ## seperators
    seps = [
        ":",
        "(",
        ")",
        " - ",
        ",",
        ";",
        "/",
        "e.g.",
        "must have ",
        "&",
        "is a plus",
        "etc.",
        "*",
        " or ",
    ]
    for sep in seps:
        if _contains(skill, sep):
            return _split_and_clean(skill.split(sep))

    ## full replacements
    full_replace = [
        ["html5", "html"],
        [".net", "dotnet"],
    ]
    for r in full_replace:
        if skill == r[0]:
            return clean_entry(r[1])

    # remove for multiple "/"
    if len(skill.split("/")) > 2:
        return _split_and_clean(skill.split("/"))

    ## leturn list

    # C/C++

    if len(skill.split("/")) == 2:
        return _split_and_clean(skill.split("/"))

    if _contains(skill, "version "):
        chunk = skill.split("version ")

        f_letter = chunk[1][:1]

        if f_letter.isnumeric():
            return clean_entry(chunk[0])

    # ignore

    if len(skill) > 20:
        return []

    return [skill]


def pre_proccess(v):  # v -> list
    cleaned = list()

    for skill in v:  # i -> string
        # seperate by and

        tmp = clean_entry(skill.lower().strip())

        cleaned.extend(tmp)
    return cleaned

    # Minimum 3 years of build/release and configuration management,Experience with one or more of the following Operating Systems (Android, Windows Embedded, Linux, Window 7)

    # OOP - PHP -> clean the "-" check for space first so you don't affect data like "T-SQL"

    # Java (version 7,8) - contains numbers

    # International Coaching Federation (ICF)

    # "Big Data":Spark:"data warehouse":"data model":AWS

    # HTML5; CSS; JSON; JQuery; AngularJS


def run_with_data_set():
    df = pd.read_csv("./data/job-posts.csv")

    skills_data = df["skills"].values.tolist()
    skill_factors, skill_set = proccess_data(skills_data)

    with open("skill_factors.json", "w") as fp:
        json.dump(skill_factors, fp)

    def _clean_set(pairs):
        k, v = pairs
        return v > 0

    clean_set = _dict_filter(skill_set.items(), _clean_set)
    with open("skill_set_7.json", "w") as fp:
        json.dump(clean_set, fp)


def proccess_data(skills_data: list):
    pre_skills = _map(
        _filter(skills_data, lambda y: y != None or type(y) is str),
        lambda x: str(x).split(","),
    )

    clean_skills = _map(pre_skills, pre_proccess)

    skill_pairs = dict()
    skill_set = dict()

    for skills in clean_skills:
        # [list if skills]

        for x in skills:
            if x not in skill_set:
                skill_set[x] = 0
            else:
                skill_set[x] += 1

            if x not in skill_pairs:
                skill_pairs[x] = []

            for y in skills:
                if y != x:
                    skill_pairs[x].append(y)

    def _clean(pairs):
        k, value = pairs

        return len(value) > 0

    clean_pairs = dict(filter(_clean, skill_pairs.items()))

    skill_factors = dict()

    for key, values in clean_pairs.items():
        if key not in skill_factors:
            skill_factors[key] = dict()

        for skill in values:
            if skill not in skill_factors[key]:
                skill_factors[key][skill] = 1
            else:
                skill_factors[key][skill] += 1
    return skill_factors, skill_set

    # print(list(skill_factors.items())[0])

    # print("== START EXPORT ===")

    # cleaned_data = pd.DataFrame(skill_factors)

    # # print(cleaned_data.head())

    # # cleaned_data.to_csv('skill_factors.csv', index=False)

    # print("== DONE EXPORT ===")