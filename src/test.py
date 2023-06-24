from main import clean_entry, proccess_data

test = ["(html,css)., etl - informatica - datastage - teradata -hadoop"]

_, skill_set = proccess_data(test)

print(skill_set)
# print('"sdfsdf","asdsfsdf","sdfsdfd"'.replace('"',''))