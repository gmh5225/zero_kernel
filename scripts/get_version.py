from pathlib import Path


def main() -> None:
    rootpath = Path(Path(__file__).absolute().parents[1])
    with open(Path(rootpath, "pyproject.toml")) as f:
        print(f.read().split('version = "')[1].split('"')[0])


if __name__ == "__main__":
    main()
