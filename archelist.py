import flet as ft
import json
import os
from datetime import datetime, timedelta

ARCHIVE_FILE = "archive.json"
CUSTOM_FILE = "custom.json"

initial_schedules = [
    {"title": "낮징", "date": "2024-07-25"},
    {"title": "밤징", "date": "2024-07-25"},
    {"title": "히라마징", "date": "2024-07-25"},
    {"title": "촛대", "date": "2024-07-25"},
    {"title": "고래", "date": "2024-07-25"},
    {"title": "정원7단(정레공)", "date": "2024-07-25"},
    {"title": "황평(가루다)", "date": "2024-07-25"},
    {"title": "용", "date": "2024-07-25"},
    {"title": "카둠", "date": "2024-07-25"},
    {"title": "알깨기", "date": "2024-07-25"},
]

middle_schedules = [
    {"title": "채권퀘", "date": "2024-07-25"},
    {"title": "가족퀘", "date": "2024-07-25"},
    {"title": "침공", "date": "2024-07-25"},
    {"title": "히라마서부(동물)", "date": "2024-07-25"},
    {"title": "히라마서부(교단)", "date": "2024-07-25"},
    {"title": "히라마동부(계단)", "date": "2024-07-25"},
    {"title": "히라마동부(안개)", "date": "2024-07-25"},
    {"title": "나차쉬동물", "date": "2024-07-25"},
]

right_schedules = [
    {"title": "도서관", "date": "2024-07-25"},
    {"title": "영섬", "date": "2024-07-25"},
    {"title": "나차", "date": "2024-07-25"},
    {"title": "검가", "date": "2024-07-25"},
    {"title": "풍요", "date": "2024-07-25"},
]

custom_schedules = [
    {"title": "", "date":""}
]

def main(page: ft.Page):
    page.title = "ArcheChecklist"
    page.window_resizable = False
    page.window_width = 1200
    page.window_height = 600

    def load_archive():
        if os.path.exists(ARCHIVE_FILE):
            with open(ARCHIVE_FILE, "r") as file:
                return json.load(file)
        else:
            return []

    def save_archive(archive):
        with open(ARCHIVE_FILE, "w") as file:
            json.dump(archive, file, indent=4)
        #print(f"Archive saved: {archive}")

    def update_archive():
        global archive
        today = datetime.today().date()
        one_week_ago = today - timedelta(days=7)
        archive = load_archive()
        current_date_records = [record for record in archive if record['date'] == today.strftime("%Y-%m-%d")]
        if not current_date_records:
            for game in initial_schedules + middle_schedules + right_schedules:
                existing_status = next((record['completed'] for record in archive if record['title'] == game['title'] and record['date'] == today.strftime("%Y-%m-%d")), False)
                archive.append({"title": game['title'], "date": today.strftime("%Y-%m-%d"), "completed": existing_status})
        archive = [record for record in archive if datetime.strptime(record['date'], "%Y-%m-%d").date() > one_week_ago]
        latest_record_date = max(datetime.strptime(record['date'], "%Y-%m-%d").date() for record in archive)
        if latest_record_date != today:
            archive = [record for record in archive if record['date'] == today.strftime("%Y-%m-%d")]
            for game in initial_schedules + middle_schedules + right_schedules:
                if not any(record['title'] == game['title'] for record in archive):
                    archive.append({"title": game['title'], "date": today.strftime("%Y-%m-%d"), "completed": False})
        save_archive(archive)

    def update_check(event):
        checkbox = event.control
        game_title = checkbox.data
        for record in archive:
            if record['title'] == game_title and record['date'] == datetime.today().strftime("%Y-%m-%d"):
                record['completed'] = checkbox.value
                break
        save_archive(archive)

    def create_checklist_item(game):
        completed = next((record['completed'] for record in archive if record['title'] == game['title'] and record['date'] == datetime.today().strftime("%Y-%m-%d")), False)
        return ft.Checkbox(
            label=f"{game['title']}",
            value=completed,
            on_change=update_check,
            data=game['title']
        )

    global archive
    update_archive()

    left_checklist = [create_checklist_item(game) for game in initial_schedules]
    middle_checklist = [create_checklist_item(game) for game in middle_schedules]
    right_checklist = [create_checklist_item(game) for game in right_schedules]
    today = datetime.today().date()
    date_text = ft.Text(f"기준 일자: {today.strftime('%Y-%m-%d')}", size=20, weight="bold")
    version_text = ft.Text("Version 1", size=12, weight="bold", color="gray")

    page.add(
        ft.Column(
            controls=[
                date_text,
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("일일 일정", size=18, weight="bold"),
                                    *left_checklist
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                            ),
                            padding=10,
                            margin=5,
                            border=ft.border.all(1, "black"),
                            width=300
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("주간,추가적 일정", size=18, weight="bold"),
                                    *middle_checklist
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                            ),
                            padding=10,
                            margin=5,
                            border=ft.border.all(1, "black"),
                            width=300
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("인던 일정", size=18, weight="bold"),
                                    *right_checklist
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                            ),
                            padding=10,
                            margin=5,
                            border=ft.border.all(1, "black"),
                            width=300
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Container(
                    content=version_text,
                    alignment=ft.alignment.bottom_right,
                    padding=ft.padding.only(right=10, bottom=10)
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
    )

ft.app(target=main)
