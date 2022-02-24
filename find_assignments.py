from collections import namedtuple, defaultdict
from typing import List, Tuple

Contributor = namedtuple("Contributor", field_names=["name", "skills"])
Project = namedtuple(
    "Project", field_names=["name", "days", "score", "best_before", "roles"]
)
Skill = namedtuple("Skill", field_names=["name", "level"])
Role = namedtuple("Role", field_names=["name", "level"])


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
            candidates = skill_contributor[role.name][_level]
            for index, c in enumerate(candidates):
                if c not in assignment:
                    assignment.append(c)
                    for skill in c.skills:
                        if skill.level < 99 and skill.name == role.name:
                            skill.level += 1
                    skill_contributor[role.name][_level].pop(index)
                    break
        else:
            return None
    return assignment


def find_possible_assignment(contributors: List[Contributor], roles: List[Role]) -> List[Tuple[Contributor, Role]]:
    if not roles:
        return True
    if not contributors:
        return False
    for contributor in contributors:
        for role in roles:
            skill_names = [skill.name for skill in contributor.skills]
            if role.name in skill_names:
                skill = contributor.skills[skill_names.index(role.name)]
                if role.level <= skill.level:
                    possible_assignment = find_possible_assignment(
                        [c for c in contributors if c != contributor],
                        [t for t in roles if t != role]
                    )
                    if possible_assignment is True:
                        return [(contributor, role)]
                    if possible_assignment is not False:
                        return possible_assignment + [(contributor, role)]
    return False
