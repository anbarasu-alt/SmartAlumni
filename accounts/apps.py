from django.apps import AppConfig


class AccountsConfig(AppConfig):
    def ready(self):
        import accounts.signals

    name = 'accounts'
