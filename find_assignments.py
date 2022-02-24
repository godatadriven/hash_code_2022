from collections import namedtuple
from typing import List, Tuple

Contributor = namedtuple("Contributor", field_names=["name", "skills"])
Project = namedtuple(
    "Project", field_names=["name", "days", "score", "best_before", "roles"]
)
Skill = namedtuple("Skill", field_names=["name", "level"])
Role = namedtuple("Role", field_names=["name", "level"])


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
