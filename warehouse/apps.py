from django.apps import AppConfig


class SellerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'warehouse'

    def ready(self) -> None:
        res = super().ready()
        from warehouse.worker import main
        import asyncio
        import threading
        t = threading.Thread(target=asyncio.run, args=[main()])
        t.daemon = True
        t.start()
        return res
