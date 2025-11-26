import uvicorn

from app.libs.db.create_db import get_db_interface

def run_app():
    print("starting...")
    db_interface = get_db_interface()
    db_interface.create_db_and_tables()
    print("done.")

    uvicorn.run("app.app:app", host="0.0.0.0", port=8282, reload=False)


if __name__ == "__main__":
    run_app()
