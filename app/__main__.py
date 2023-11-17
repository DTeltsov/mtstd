from app.src import Application
from logger import install_qml_handler


def main():
    app = Application()
    app.init_app()

    install_qml_handler()
    app.start_app()


if __name__ == '__main__':
    main()
