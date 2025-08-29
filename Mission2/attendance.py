from abc import abstractmethod, ABC
from typing import Dict, List, Tuple


class GradePolicy(ABC):
    @abstractmethod
    def classify(self, points):
        pass


class TresholdGradePolicy(GradePolicy):
    def __init__(self, threshold):
        self.threshold_policy = threshold

    def classify(self, points: int) -> str:
        for threshold, grade in self.threshold_policy:
            if points >= threshold:
                return grade
        return "NORMAL"


class ATTENDANCE:
    def __init__(self):
        self.names = [''] * 100
        self.points = [0] * 100
        self.grade = [""] * 100
        self.id_dict = {}
        self.wed_cnt = [0] * 100
        self.weekend_cnt = [0] * 100
        self.grade_policy = TresholdGradePolicy([(50, "GOLD"), (30, "SILVER")])

    def get_id(self, name: str) -> None:
        max_id = len(self.id_dict)
        if name not in self.id_dict:
            max_id += 1
            self.id_dict[name] = max_id
            self.names[max_id] = name
        return max_id

    def get_attendance_points(self, id: int, day: str) -> None:
        add_point = 0
        if day in ["monday", "tuesday", "thursday", "friday"]:
            add_point += 1
        elif day == "wednesday":
            add_point += 3
            self.wed_cnt[id] += 1
        elif day in ["saturday", "sunday"]:
            add_point += 2
            self.weekend_cnt[id] += 1
        self.points[id] += add_point

    def get_bonus_points(self) -> None:
        for id in range(1, len(self.id_dict) + 1):
            if self.wed_cnt[id] > 9:
                self.points[id] += 10
            if self.weekend_cnt[id] > 9:
                self.points[id] += 10

    def get_grade(self) -> None:
        for id in range(1, len(self.id_dict) + 1):
            self.grade[id] = self.grade_policy.classify(self.points[id])
            print(f"NAME : {self.names[id]}, POINT : {self.points[id]}, GRADE : {self.grade[id]}")

    def show_removed_player(self) -> None:
        print("\nRemoved player")
        print("==============")
        for id in range(1, len(self.id_dict) + 1):
            if self.grade[id] == "NORMAL" and self.wed_cnt[id] == 0 and self.weekend_cnt[id] == 0:
                print(self.names[id])

    def run_attendance_system(self) -> None:
        try:
            with open("attendance_weekday_500.txt", encoding='utf-8') as f:
                for _ in range(500):
                    line = f.readline()
                    if not line:
                        break
                    parts = line.strip().split()
                    if len(parts) == 2:
                        self.get_id(parts[0])
                        self.get_attendance_points(self.id_dict[parts[0]], parts[1])
            self.get_bonus_points()
            self.get_grade()
            self.show_removed_player()

        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")


if __name__ == "__main__":
    attendance = ATTENDANCE()
    attendance.run_attendance_system()
