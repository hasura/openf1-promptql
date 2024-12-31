from openf1_dump.cli import get_year_input
from openf1_dump.models.meetings import ingest_meetings

def main():
    year = get_year_input()

    ingest_meetings(year)

if __name__ == '__main__':
    main()