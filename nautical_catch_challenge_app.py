from typing import List

from project.divers.base_diver import BaseDiver
from project.divers.free_diver import FreeDiver
from project.divers.scuba_diver import ScubaDiver
from project.fish.base_fish import BaseFish
from project.fish.deep_sea_fish import DeepSeaFish
from project.fish.predatory_fish import PredatoryFish


class NauticalCatchChallengeApp:
    divers_class = {
        "ScubaDiver": ScubaDiver,
        "FreeDiver": FreeDiver
    }

    fish_class = {
        "DeepSeaFish": DeepSeaFish,
        "PredatoryFish": PredatoryFish
    }

    def __init__(self):
        self.divers: List[BaseDiver] = []
        self.fish_list: List[BaseFish] = []

    def dive_into_competition(self, diver_type: str, diver_name: str):
        if diver_type not in self.divers_class:
            return f"{diver_type} is not allowed in our competition."
        try:
            diver = [d for d in self.divers if d.name == diver_name][0]
            return f"{diver_name} is already a participant."
        except IndexError:
            diver = self.divers_class[diver_type](diver_name)
            self.divers.append(diver)
            return f"{diver_name} is successfully registered for the competition as a {diver_type}."

    def swim_into_competition(self, fish_type: str, fish_name: str, points: float):
        if fish_type not in self.fish_class:
            return f"{fish_type} is forbidden for chasing in our competition."

        try:
            fish = [f for f in self.fish_list if f.name == fish_name][0]
            return f"{fish.name} is already permitted."
        except IndexError:
            new_fish = self.fish_class[fish_type](fish_name, points)
            self.fish_list.append(new_fish)
            return f"{fish_name} is allowed for chasing as a {fish_type}."

    def chase_fish(self, diver_name: str, fish_name: str, is_lucky: bool):
        try:
            diver = [d for d in self.divers if d.name == diver_name][0]
        except IndexError:
            return f"{diver_name} is not registered for the competition."

        try:
            fish = [f for f in self.fish_list if f.name == fish_name][0]
        except IndexError:
            return f"The {fish_name} is not allowed to be caught in this competition."

        if diver.has_health_issue:
            return f"{diver_name} will not be allowed to dive, due to health issues."

        if diver.oxygen_level < fish.time_to_catch:
            diver.miss(fish.time_to_catch)
            return f"{diver.name} missed a good {fish.name}."
        elif diver.oxygen_level == fish.time_to_catch:
            if is_lucky:
                diver.hit(fish)
                return f"{diver_name} hits a {fish.points:1f}pt. {fish_name}."
            else:
                diver.miss(fish)
                return f"{diver_name} missed a good {fish_name}."
        else:  #diver.oxygen_level > fish.time_to_catch:
            diver.hit(fish)
            return f"{diver_name} hits a {fish.points:1f}pt. {fish_name}."

        if diver.oxygen_level == 0:
            diver.update_health_status()

    def health_recovery(self):
        divers_with_health_issue = [d for d in self.divers if d.has_health_issue]

        for d in divers_with_health_issue:
            d.has_health_issue = False
            d.renew_oxy()

        return f"Divers recovered: {len(divers_with_health_issue)}"

    def diver_catch_report(self, diver_name: str):
        diver = [d for d in self.divers if d.name == diver_name][0]
        result = f"**{diver.name} Catch Report**\n"
        fish_details = "\n".join([f.fish_details() for f in diver.catch()])
        result += fish_details
        return result

    def competition_statistics(self):
        pass
