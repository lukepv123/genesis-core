import os
from genesis.bootstrap import create_app
from genesis.app import run

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    app = create_app(root_dir)
    run(app)

if __name__ == "__main__":
    main()
