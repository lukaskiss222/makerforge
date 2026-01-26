from pydantic_settings import CliApp

from infrastructure.ioc import init_container

from .settings import Settings


def main() -> None:
    settings = CliApp.run(Settings)
    init_container(settings)
    print(settings)


if __name__ == "__main__":
    main()
