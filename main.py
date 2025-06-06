import sentry_sdk
import os
from control.main_controller import Controller


def call_sentry():
    if os.environ.get("SENTRY_KEY"):
        sentry_sdk.init(
            dsn=os.environ.get("SENTRY_KEY"),
            send_default_pii=True,
        )


def main():
    call_sentry()
    controller = Controller()
    controller.display_welcome_menu()


if __name__ == '__main__':
    main()
