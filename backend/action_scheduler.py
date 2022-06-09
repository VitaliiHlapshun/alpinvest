import schedule
from backend.movie import Movie


def scheduler(func_to_call):
    """Weekly function call action"""
    schedule.every().weeks.do(func_to_call)
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    scheduler(Movie.create_test_100)
