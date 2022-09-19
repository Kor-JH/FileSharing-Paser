import argparse
from  modules import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "-contact", action="store_true", dest="contact", default=False, help= "Get contact information")
    parser.add_argument("-f", "-fileshare", action="store_true",  dest="fileshare", default=False, help= "Get file sharing information")
    args = parser.parse_args()

    if args.contact & args.fileshare:
        get_sharing_info()
