from pydantic_settings import CliApp

from .settings import Settings


def main() -> None:
    args = CliApp.run(Settings)
    print(args.model_dump())


if __name__ == "__main__":
    main()
