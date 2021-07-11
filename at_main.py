import at_token
import sys

def main():
    result = at_token.getToken()
    if result == -1:
        print('error at getToken')
        sys.exit()
    

if __name__ == "__main__":
    main()
