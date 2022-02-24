from collections import defaultdict, namedtuple
import os
import sys
from typing import List, Tuple

from find_assignments import find_possible_assignment

Contributor = namedtuple("Contributor", field_names=["name", "skills"])
Project = namedtuple(
    "Project", field_names=["name", "days", "score", "best_before", "roles"]
)
Skill = namedtuple("Skill", field_names=["name", "level"])
Role = namedtuple("Role", field_names=["name", "level"])
Project = namedtuple(
    "Project", field_names=["name", "days", "score", "best_before", "roles"]
)


class Role:
    __slots__ = "name", "level"

    def __init__(self, name, level):
        self.name = name
        # convert 1 index to 0
        self.level = level - 1


class Skill:
    __slots__ = "name", "level"

    def __init__(self, name, level):
        self.name = name
        # convert 1 index to 0
        self.level = level - 1


class Planning:
    __slots__ = "project", "contributors"

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


def write_file(planning_list, filename):
    with open(filename, "w") as fp:
        print(len(planning_list), file=fp)
        for planning in planning_list:
            print(planning.project.name, file=fp)
            print(
                " ".join(
                    contributor.name for contributor in planning.contributors
                ),
                file=fp,
            )


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
            while _level < 100 and not skill_contributor[role.name][_level]:
                _level += 1

            if _level < 100:
                contributors.append(skill_contributor[role.name][_level][0])
            else:
                break

        if len(contributors) == len(project.roles):
            planning_list.append(Planning(project, contributors))

    return planning_list


def find_possible_assignment_roel(contributors: List[Contributor], roles: List[Role]):
    skill_contributor = defaultdict(lambda: [[] for _ in range(100)])
    for contributor in contributors:
        for skill in contributor.skills:
            skill_contributor[skill.name][skill.level].append(contributor)

    assignment = []
    for role in roles:
        _level = role.level
        while _level < 100 and not skill_contributor[role.name][_level]:
            _level += 1

        if _level < 100:
            assignment.append(skill_contributor[role.name][_level].pop())
        else:
            return None
    return assignment


def create_solution_simulation(projects, contributors):
    max_t = max([p.best_before + p.score - p.days for p in projects])
    available_contributors = contributors
    working_contributors = []  # list of tuples: (nr of days remaining and value, list of contributors)

    planning_list = []
    t = 0
    while True:
        remaining_projects = projects

        if not remaining_projects:
            return planning_list

        elif t > max_t:
            return planning_list

        projects = []
        for project in remaining_projects:
            assignment: List[
                Tuple[Contributor, Role]
            ] = find_possible_assignment_roel(available_contributors, project.roles)

            if assignment:
                assigned_contributors = assignment

                ## required by Daniel version
                # assigned_contributors = [
                #     contributor for contributor, role in assignment
                # ]
                planning = Planning(project, assigned_contributors)
                planning_list.append(planning)

                working_contributors.append((project.days, assigned_contributors))
                for c in assigned_contributors:
                    available_contributors.remove(c)
                
            else:
                projects.append(project)

        t += 1        
        back_to_work = [v for k, v in working_contributors if k == 1]
        for contrs in back_to_work:
            for contr in contrs:
                available_contributors.append(contr)
        working_contributors = [(k-1, v) for k, v in working_contributors if k > 1]
        

PROBLEM_FILENAMES = [
    "a_an_example.in.txt",
    "b_better_start_small.in.txt",
    "c_collaboration.in.txt",
    "d_dense_schedule.in.txt",
    "e_exceptional_skills.in.txt",
    "f_find_great_mentors.in.txt",
]


def solve_all(problem_filenames=PROBLEM_FILENAMES):
    for problem_filename in problem_filenames:
        print(f"Working on {problem_filename}..")
        contributors, projects = parse_file(f"problems/{problem_filename}")
        planning = create_solution_simulation(projects, contributors)

        if not os.path.exists("solutions"):
            os.makedirs("solutions")
        write_file(planning, f"solutions/{problem_filename}")
        # project_values = [project_value(p, 0) for p in projects]


if __name__ == "__main__":
    solve_all()
    # contributors, projects = parse_file(sys.argv[1])
    #
    # planning = create_solution_simulation(projects, contributors)
    #
    # write_file(planning, sys.argv[2])
