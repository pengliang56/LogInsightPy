import os

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from apps.config.milvus_init import milvus_client as client


class LogHandler(FileSystemEventHandler):
    def __init__(self, log_dir):
        self.log_file = log_dir
        self.last_position = 0
        self.observer = Observer()
        print(f"Monitoring file: {self.log_file}")
        self.start()

    def on_modified(self, event):
        if event.src_path == self.log_file:
            self.read_log_file()

    def read_log_file(self):
        with open(self.log_file, 'r') as f:

            f.seek(self.last_position)

            new_lines = f.readlines()
            if new_lines:
                for line in new_lines:
                    client.insert(line.strip())
                self.last_position = f.tell()

    def start(self):
        log_directory = os.path.dirname(self.log_file)
        self.observer.schedule(self, path=log_directory, recursive=False)
        self.observer.start()

    def stop(self):

        self.observer.stop()
        self.observer.join()
