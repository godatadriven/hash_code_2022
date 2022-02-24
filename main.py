from collections import namedtuple
from dataclasses import field
import os
import sys

Contributor = namedtuple("Contributor", field_names=["name", "skills"])
Project = namedtuple("Project", field_names=["name", "days", "score", "best_before", "roles"])
Skill = namedtuple("Skill", field_names=["name", "level"])
Role = namedtuple("Role", field_names=["name", "level"])

def parse_file(filename):
    fp = open(filename, 'r')
    lines = fp.readlines()
    c, p = map(int, lines.pop(0).split())

    contributors = []
    for i in range(c):
        name, nr_skills = lines.pop(0).split()
        skills = []

        for j in range(int(nr_skills)):
            name_of_skill, level = lines.pop(0).split()
            skills.append(Skill(name_of_skill, int(level)))
        
        contributors.append(Contributor(name, skills))
    
    projects = []
    for i in range(p):
        name, days, score, best_before, nr_roles = lines.pop(0).split()
        roles = []
        for j in range(int(nr_roles)):
            name_of_skill, level = lines.pop(0).split()
            roles.append(Role(name_of_skill, int(level)))

        projects.append(Project(name, int(days), int(score), int(best_before), roles))

    return contributors, projects

print(parse_file(sys.argv[1]))