from typing import List


from main import Contributor, Role


def find_possible_assignment(contributors: List[Contributor], roles: List[Role]):
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
