import urllib.parse


def main():
    password = input("Enter your MongoDB password to URL encode: ")
    encoded = urllib.parse.quote_plus(password)
    print(f"\nOriginal password: {password}")
    print(f"Encoded password : {encoded}")
    print("\nUse this encoded password in your MONGODB_URI in .env")


if __name__ == "__main__":
    main()
