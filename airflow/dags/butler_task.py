import random
import pendulum
from airflow.exceptions import AirflowException

def greet():
    # now = pendulum.now("Asia/Tokyo")
    now = pendulum.now("Europe/Paris")
    if now.hour < 12:
        greeting = "おはようございます。ご主人様"
    elif now.hour < 18:
        greeting = "こんにちは。ご主人様"
    else:
        greeting = "こんばんは。ご主人様"
    print(greeting)
    return greeting

def next_talk(**kwargs):
    ti = kwargs['ti']
    greeting = ti.xcom_pull(task_ids='greet_task')
    if greeting == "おはようございます。ご主人様":
        return "hawaii_task"
    elif greeting == "こんにちは。ご主人様":
        return "tea_party_task"
    else:
        return "end_task"

def hawaii():
    print("現在、ハワイへ移動中です。")
    airframe_trouble = random.randint(1, 4)
    if airframe_trouble > 2:
        raise AirflowException("機体トラブルが発生したため引き返します")
    else:
        print("無事、ハワイに到着しました")


def tea_party():
    print("次の予定は〇〇ホテルでのお茶会となっております")

def end_day():
    print("本日もご苦労様でした。ゆっくりお休みください")

def private_beach():
    weather_chance = random.randint(1, 10)
    if weather_chance > 5:
        print("晴天でよかったです。プライベートビーチをお楽しみください")
    else:
        print("雨天のため、室内プールをお楽しみください")