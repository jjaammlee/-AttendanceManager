from platform import mac_ver
from typing import Dict, List, Tuple


def get_id(name: str, id_dict: Dict[str, int], names: List[str]) -> Tuple[Dict[str, int], List[str]]:
    max_id = len(id_dict)
    if name not in id_dict:
        max_id += 1
        id_dict[name] = max_id
        names[max_id] = name
    return id_dict, names


def get_attendance_points(id: int, day: str, points: List[int], wed: List[int], weekend: List[int]) -> Tuple[
    List[int], List[int], List[int]]:
    add_point = 0
    if day in ["monday", "tuesday", "thursday", "friday"]:
        add_point += 1
    elif day == "wednesday":
        add_point += 3
        wed[id] += 1
    elif day in ["saturday", "sunday"]:
        add_point += 2
        weekend[id] += 1
    points[id] += add_point
    return points, wed, weekend


def get_bonus_points(points: List[int], max_id: int, wed: List[int], weekend: List[int]) -> List[int]:
    for id in range(1, max_id + 1):
        if wed[id] > 9:
            points[id] += 10
        if weekend[id] > 9:
            points[id] += 10
    return points


def get_grade(points: List[int], max_id: int, names: List[str]) -> Dict[int, Tuple[int, str]]:
    grade = {}
    for id in range(1, max_id + 1):
        if points[id] >= 50:
            grade[id] = "GOLD"
        elif points[id] >= 30:
            grade[id] = "SILVER"
        else:
            grade[id] = "NORMAL"
        print(f"NAME : {names[id]}, POINT : {points[id]}, GRADE : {grade[id]}")
    return grade


def show_removed_player(grade: Dict[int, str], max_id: int, names: List[str], wed: List[int],
                        weekend: List[int]) -> None:
    print("\nRemoved player")
    print("==============")
    for id in range(1, max_id + 1):
        if grade[id] == "NORMAL" and wed[id] == 0 and weekend[id] == 0:
            print(names[id])


def run_attendance_system() -> None:
    try:
        points = [0] * 100
        names = [''] * 100  # id -> name
        id_dict = {}  # name -> id
        wed_cnt = [0] * 100
        weekend_cnt = [0] * 100
        with open("attendance_weekday_500.txt", encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    id_dict, names = get_id(parts[0], id_dict, names)
                    points, wed_cnt, weekend_cnt = get_attendance_points(id_dict[parts[0]], parts[1], points, wed_cnt, weekend_cnt)
        points = get_bonus_points(points, len(id_dict), wed_cnt, weekend_cnt)
        grade = get_grade(points, len(id_dict), names)
        show_removed_player(grade, len(id_dict), names, wed_cnt, weekend_cnt)

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


if __name__ == "__main__":
    run_attendance_system()