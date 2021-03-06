from collections import defaultdict, namedtuple
import os
import sys

Contributor = namedtuple("Contributor", field_names=["name", "skills"])
Project = namedtuple(
    "Project", field_names=["name", "days", "score", "best_before", "roles"]
)
Skill = namedtuple("Skill", field_names=["name", "level"])
Role = namedtuple("Role", field_names=["name", "level"])
Project = namedtuple("Project", field_names=["name", "days", "score", "best_before", "roles"])

class Role:
    __slots__ = 'name', 'level'

    def __init__(self, name, level):
        self.name = name
        # convert 1 index to 0
        self.level = level - 1

class Skill:
    __slots__ = 'name', 'level'

    def __init__(self, name, level):
        self.name = name
        # convert 1 index to 0
        self.level = level - 1
    
class Planning:
    __slots__ = 'project', 'contributors'

    def __init__(self, project):
        self.project = project
        self.contributors = []

Planning = namedtuple("Planning", field_names=["project", "contributors"])

def parse_file(filename):
    fp = open(filename, "r")
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

        projects.append(
            Project(name, int(days), int(score), int(best_before), roles)
        )

    return contributors, projects

def project_value(project: Project, timestep: int) -> float:
    """Remaining project score over total project days"""
    discount = max(0, timestep - project.best_before)
    return (project.score - discount) / len(project.roles) * project.days

PROBLEMS = [
    "a_an_example.in.txt",
    "b_better_start_small.in.txt",
    "c_collaboration.in.txt",
    "d_dense_schedule.in.txt",
    "e_exceptional_skills.in.txt",
    "f_find_great_mentors.in.txt",
]
for problem_filename in PROBLEMS:
    contributors, projects = parse_file(problem_filename)
    # project_values = [project_value(p, 0) for p in projects]

def write_file(planning_list, filename):
    with open(filename, "w") as fp:
        print(len(planning_list), file=fp)
        for planning in planning_list:
            print(planning.project.name, file=fp)
            print(" ".join(contributor.name for contributor in planning.contributors), file=fp)


def create_solution(projects, contributors):
    skill_contributor = defaultdict(lambda: [[] for _ in range(100)])

    for contributor in contributors:
        for skill in contributor.skills:
            skill_contributor[skill.name][skill.level].append(contributor)

    planning_list = []
    for project in projects:
        contributors = []
        for role in project.roles:
            _level = role.level
            while _level<100  and not skill_contributor[role.name][_level]:
                _level+=1
            
            if _level<100:
                contributors.append(skill_contributor[role.name][_level][0])
            else:
                break
        
        if len(contributors) == len(project.roles):
            planning_list.append(Planning(project, contributors))

    return planning_list

if __name__ == "__main__":
    contributors, projects = parse_file(sys.argv[1])

    planning = create_solution(projects, contributors)
    
    write_file(planning, sys.argv[2])
