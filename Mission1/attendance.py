from platform import mac_ver

wed = [0] * 100
weekend = [0] * 100


def get_id(name, id_dict, names):
    max_id = len(id_dict)
    if name not in id_dict:
        max_id += 1
        id_dict[name] = max_id
        names[max_id] = name
    return id_dict, names


def get_attendance_points(id, day, points):
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
    return points


def get_bonus_points(points, max_id):
    for id in range(1, max_id + 1):
        if wed[id] > 9:
            points[id] += 10
        if weekend[id] > 9:
            points[id] += 10
    return points


def get_grade(points, max_id, names):
    grade = {}
    for id in range(1, max_id + 1):
        if points[id] >= 50:
            grade[id] = (1, "GOLD")
        elif points[id] >= 30:
            grade[id] = (2, "SILVER")
        else:
            grade[id] = (0, "NORMAL")
        print(f"NAME : {names[id]}, POINT : {points[id]}, GRADE : {grade[id][1]}")
    return grade


def show_removed_player(grade, max_id, names):
    print("\nRemoved player")
    print("==============")
    for id in range(1, max_id + 1):
        if grade[id][0] == 0 and wed[id] == 0 and weekend[id] == 0:
            print(names[id])


def input_file():
    try:
        points = [0] * 100
        names = [''] * 100  # id -> name
        id_dict = {}        # name -> id
        with open("attendance_weekday_500.txt", encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    id_dict, names =  get_id(parts[0], id_dict, names)
                    points = get_attendance_points(id_dict[parts[0]], parts[1], points)
        points = get_bonus_points(points, len(id_dict))
        grade = get_grade(points, len(id_dict), names)
        show_removed_player(grade, len(id_dict), names)

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


if __name__ == "__main__":
    input_file()