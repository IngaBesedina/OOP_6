#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pytest

from task1 import Students, UnknownCommandError


def test_add_student():
    students = Students()
    students.add_student("Иванов И.И.", 101, [5, 4, 5, 4, 5])
    assert len(students.students) == 1
    assert students.students[0].surname == "Иванов И.И."
    assert students.students[0].group_number == 101
    assert students.students[0].grades == [5, 4, 5, 4, 5]


def test_sort_students_by_group():
    students = Students()
    students.add_student("Петров П.П.", 102, [4, 4, 4, 4, 4])
    students.add_student("Иванов И.И.", 101, [5, 5, 5, 5, 5])
    assert students.students[0].group_number == 101
    assert students.students[1].group_number == 102


def test_select_students():
    students = Students()
    students.add_student("Иванов И.И.", 101, [5, 5, 5, 5, 5])
    students.add_student("Петров П.П.", 102, [3, 3, 3, 3, 3])
    selected = students.select_students()
    assert len(selected) == 1
    assert selected[0].surname == "Иванов И.И."


def test_save_and_load_students(tmp_path):
    file_path = tmp_path / "students.xml"
    students = Students()
    students.add_student("Иванов И.И.", 101, [5, 4, 5, 5, 4])
    students.save_students(file_path)

    loaded_students = Students()
    loaded_students.load_students(file_path)
    assert len(loaded_students.students) == 1
    assert loaded_students.students[0].surname == "Иванов И.И."
    assert loaded_students.students[0].group_number == 101
    assert loaded_students.students[0].grades == [5, 4, 5, 5, 4]


def test_unknown_command_error():
    with pytest.raises(UnknownCommandError) as excinfo:
        raise UnknownCommandError("unknown")
    assert str(excinfo.value) == "unknown -> Unknown command"
