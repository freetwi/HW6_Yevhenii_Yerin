import random
from dataclasses import dataclass, field
from typing import TypeAlias, TypedDict, Any
from collections import defaultdict

from faker import Faker

T_GROUP_NAME: TypeAlias = str
T_GROUP_NAMES: TypeAlias = list[T_GROUP_NAME]
T_USER_NAME: TypeAlias = str

class Human(TypedDict):
    name: T_USER_NAME
    group: T_GROUP_NAME

T_HUMANS: TypeAlias = list[Human]
T_ORGANIZED_DATA: TypeAlias = dict[T_GROUP_NAME, list[T_USER_NAME]]
T_OUTPUT: TypeAlias = str

@dataclass
class DataProvider:
    _faker: Faker = field(default_factory=Faker)

    def _generate_group_names(self, amount: int = 10) -> T_GROUP_NAMES:
        return [self._faker.unique.company() for _ in range(amount)]

    def _generate_human(self, group_name: T_GROUP_NAME) -> Human:
        return Human(
            name=self._faker.unique.first_name(),
            group=group_name,
        )

    def _generate_humans(self, groups: T_GROUP_NAMES, amount_of_humans: int) -> T_HUMANS:
        members = []
        for _ in range(amount_of_humans):
            group_name = random.choice(groups)
            group_member = self._generate_human(group_name=group_name)
            members.append(group_member)
        return members

    def generate_group_members(self, amount_of_groups: None | int = None, amount_of_humans: None | int = None) -> T_HUMANS:
        amount_of_groups = amount_of_groups or random.randint(5, 10)
        amount_of_humans = amount_of_humans or random.randint(3, 30)

        _groups = self._generate_group_names(amount=amount_of_groups)
        return self._generate_humans(groups=_groups, amount_of_humans=amount_of_humans)

def organize_data(humans: T_HUMANS) -> T_ORGANIZED_DATA:
    organized_data = defaultdict(list)
    for human in humans:
        organized_data[human['group']].append(human['name'])
    return organized_data

def get_formatted_output(data: T_ORGANIZED_DATA) -> T_OUTPUT:
    output_lines = []
    for group, members in data.items():
        members_list = ', '.join(members)
        output_lines.append(f"Group: {group} | Members ({len(members)}): {members_list}")
    return '\n'.join(output_lines)

def main():
    """
    Вивести всі групи, з кількістю та іменами учасників для кожної групи.
    """
    group_members = DataProvider().generate_group_members()
    organized_data = organize_data(humans=group_members)
    output = get_formatted_output(data=organized_data)
    print(output)

if __name__ == "__main__":
    main()
