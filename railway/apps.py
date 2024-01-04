from django.apps import AppConfig


class RailwayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'railway'

    def ready(self) -> None:
        res = super().ready()
        from railway.worker import main
        import asyncio
        import threading
        t = threading.Thread(target=asyncio.run, args=[main()])
        t.daemon = True
        t.start()
        return res
