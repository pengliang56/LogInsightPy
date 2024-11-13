import atexit

from django.apps import AppConfig

from apps.config.common import log as log_file_path


class LogMonitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.config'

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.log_handler = None

    def ready(self):
        from .log_monitor import LogHandler
        self.log_handler = LogHandler(log_file_path)
        atexit.register(self.log_handler.stop)
