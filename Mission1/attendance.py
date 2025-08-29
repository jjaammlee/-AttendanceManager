from platform import mac_ver

id_lst = {}
max_id = 0
points = [0] * 100
grade = {}
names = [''] * 100
wed = [0] * 100
weekend = [0] * 100


def get_id(name):
    global max_id
    if name not in id_lst:
        max_id += 1
        id_lst[name] = max_id
        names[max_id] = name


def get_attendance_points(name, day):
    id = id_lst[name]
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


def get_bonus_points():
    for id in range(1, max_id + 1):
        if wed[id] > 9:
            points[id] += 10
        if weekend[id] > 9:
            points[id] += 10


def get_grade():
    for id in range(1, max_id + 1):
        if points[id] >= 50:
            grade[id] = (1, "GOLD")
        elif points[id] >= 30:
            grade[id] = (2, "SILVER")
        else:
            grade[id] = (0, "NORMAL")
        print(f"NAME : {names[id]}, POINT : {points[id]}, GRADE : {grade[id][1]}")


def show_removed_player():
    print("\nRemoved player")
    print("==============")
    for id in range(1, max_id + 1):
        if grade[id][0] == 0 and wed[id] == 0 and weekend[id] == 0:
            print(names[id])


def input_file():
    try:
        with open("attendance_weekday_500.txt", encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    get_id(parts[0])
                    get_attendance_points(parts[0], parts[1])
        get_bonus_points()
        get_grade()
        show_removed_player()

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


if __name__ == "__main__":
    input_file()
