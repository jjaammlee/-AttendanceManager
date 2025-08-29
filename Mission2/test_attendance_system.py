import pytest
import pytest_mock
from Mission2.attendance import ATTENDANCE
import builtins


def test_get_id():
    att = ATTENDANCE()
    att.get_id("Jaewon")
    att.get_id("Minji")
    att.get_id("Jaewon")

    assert att.id_dict["Jaewon"] == 1
    assert att.id_dict["Minji"] == 2
    assert att.names[1] == "Jaewon"
    assert att.names[2] == "Minji"
    assert len(att.id_dict) == 2


@pytest.mark.parametrize("day,inc_points,inc_wed,inc_weekend",
                         [("monday", 1, 0, 0), ("tuesday", 1, 0, 0), ("thursday", 1, 0, 0), ("friday", 1, 0, 0),
                          ("wednesday", 3, 1, 0), ("saturday", 2, 0, 1), ("sunday", 2, 0, 1)])
def test_get_attendance_points(day, inc_points, inc_wed, inc_weekend):
    att = ATTENDANCE()
    id = att.get_id("Jaewon")

    points_org = att.points[id]
    wed_cnt_org = att.wed_cnt[id]
    weekend_cnt_org = att.weekend_cnt[id]

    att.get_attendance_points(id, day)

    assert att.points[id] - points_org == inc_points
    assert att.wed_cnt[id] - wed_cnt_org == inc_wed
    assert att.weekend_cnt[id] - weekend_cnt_org == inc_weekend


def test_get_bonus_points():
    att = ATTENDANCE()
    id = att.get_id("Jaewon")

    att.wed_cnt[id] = 10
    att.weekend_cnt[id] = 11
    points_org = att.points[id]
    att.get_bonus_points()

    assert att.points[id] - points_org == 20


def test_get_grade(capsys):
    att = ATTENDANCE()
    id1 = att.get_id("Jaewon")
    id2 = att.get_id("Minji")
    id3 = att.get_id("Jinwoo")

    att.points[id1] = 55
    att.points[id2] = 35
    att.points[id3] = 10

    att.get_grade()
    captured = capsys.readouterr()

    assert att.grade[id1] == "GOLD"
    assert att.grade[id2] == "SILVER"
    assert att.grade[id3] == "NORMAL"
    assert "NAME : Jaewon, POINT : 55, GRADE : GOLD" in captured.out
    assert "NAME : Minji, POINT : 35, GRADE : SILVER" in captured.out
    assert "NAME : Jinwoo, POINT : 10, GRADE : NORMAL" in captured.out


def test_show_removed_player(capsys):
    att = ATTENDANCE()
    id1 = att.get_id("Jaewon")
    id2 = att.get_id("Minji")

    att.points[id1] = 10
    att.grade[id1] = "NORMAL"
    att.wed_cnt[id1] = 0
    att.weekend_cnt[id1] = 0

    att.points[id2] = 51
    att.grade[id2] = "GOLD"
    att.wed_cnt[id2] = 4
    att.weekend_cnt[id2] = 2

    att.show_removed_player()
    out = capsys.readouterr().out

    assert "Removed player" in out
    assert "Jaewon" in out


def test_run_attendance_system_good(mocker: pytest_mock.MockerFixture, capsys):
    m = mocker.mock_open(read_data="Jaewon wednesday\nMinji saturday\n")
    mocker.patch.object(builtins, "open", m)

    att = ATTENDANCE()
    att.id_dict = {"Jaewon": 1, "Minji": 2}

    get_id_mock = mocker.patch.object(att, 'get_id')
    get_attendance_points_mock = mocker.patch.object(att, 'get_attendance_points')
    get_bonus_points_mock = mocker.patch.object(att, 'get_bonus_points')
    get_grade_mock = mocker.patch.object(att, 'get_grade')
    show_removed_player_mock = mocker.patch.object(att, 'show_removed_player')

    att.run_attendance_system()

    builtins.open.assert_called_once_with("attendance_weekday_500.txt", encoding="utf-8")
    assert get_id_mock.call_count == 2
    assert get_attendance_points_mock.call_count == 2
    get_bonus_points_mock.called_once()
    get_grade_mock.called_once()
    show_removed_player_mock.called_once()


def test_run_attendance_system_bad(mocker: pytest_mock.MockerFixture, capsys):
    mocker.patch.object(builtins, "open", side_effect=FileNotFoundError)

    att = ATTENDANCE()
    att.id_dict = {"Jaewon": 1, "Minji": 2}

    get_id_mock = mocker.patch.object(att, 'get_id')
    get_attendance_points_mock = mocker.patch.object(att, 'get_attendance_points')
    get_bonus_points_mock = mocker.patch.object(att, 'get_bonus_points')
    get_grade_mock = mocker.patch.object(att, 'get_grade')
    show_removed_player_mock = mocker.patch.object(att, 'show_removed_player')

    att.run_attendance_system()

    out = capsys.readouterr().out
    assert "파일을 찾을 수 없습니다." in out

    get_bonus_points_mock.assert_not_called()
    get_grade_mock.assert_not_called()
    show_removed_player_mock.assert_not_called()
