from databases import build_cs_database
from analysis import create_analysis_graphs

if __name__ == '__main__':
    print("Connecting to the database...")
    user = input("Enter your DB username: ")
    pwd = input("Enter your DB password: ")
    print("Connecting...")
    build_cs_database(user, pwd)
    print("DB tables generated!")
    print("Generating graphs...")
    create_analysis_graphs()
    print("Done!")
