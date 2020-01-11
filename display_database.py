#!/usr/bin/env python3
import db_utils


def main():
    con = db_utils.db_connect()
    db_utils.print_table(con)

    con.close()
    print('---------Done--------')


if __name__ == "__main__":
    main()
