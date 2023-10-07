from youtube_upload.client import YoutubeUploader
import os

from threading import Thread
from queue import Queue

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
THREAD_COUNT = 10

uploader = YoutubeUploader(CLIENT_ID, CLIENT_SECRET, "./client_secret.json")
uploader.authenticate()

path = os.getcwd() + "/to_upload"


def upload_video(
    video_path,
    title="Test video",
    description="Test description",
    tags=["fun", "ahha", "fuckyou"],
    category_id="22",
    privacy="unlisted",
    kids=False,
    publish_at=None
):
    options = {
        "title": title,
        "description": description,
        "tags": tags,
        "categoryId": category_id,
        "privacyStatus": privacy,
        "kids": kids,
        # "publishAt": None
    }
    uploader.upload(video_path, options=options)


def exec_task():
    while True:

        if queue.unfinished_tasks < 1:
            break

        current_video = queue.get()

        if not current_video:
            break

        print(f"Uploading {current_video}")

        try:
            upload_video(
                current_video, title=f"Video: {current_video.split('/')[-1]}")

        except Exception as e:
            print(f"Something went wrong with {current_video}")

        finally:
            queue.task_done()


queue = Queue()
for file in os.listdir(path):
    queue.put(f"{path}/{file}")


threads = []
for i in range(THREAD_COUNT):
    thread = Thread(target=exec_task)
    thread.start()
    threads.append(thread)

queue.join()

for _ in range(THREAD_COUNT):
    queue.put(None)

for thread in threads:
    thread.join()
