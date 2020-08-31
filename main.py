#!/usr/local/bin/python3
from meroshare import MeroShare

def main():
    meroshare = MeroShare()
    print(meroshare.getCurrentIssues().issues)
    # meroshare.printCurrentIssues()


if __name__ == '__main__':
    main()
