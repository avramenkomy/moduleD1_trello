import configparser

config = configparser.ConfigParser()
config.read("auth_params.ini")

def get_auth_params():

    key = input("Enter your key: ")
    token = input("Enter your token: ")

    if len(key) != 32:
        print("Invalid auth params. Try again enter.")
        get_auth_params()
    elif len(token) != 64:
        print("Invalid auth params. Try again enter.")
        get_auth_params()
    else:
        return {
            "key": key,
            "token": token
        }


def add_auth_params():

    if (config.has_option("Trello", "key") and config.has_option("Trello", "token")) and (len(config["Trello"]["key"]) == 32 and len(config["Trello"]["token"]) == 64):
        print("auth params is available")
    else:
        auth_params = get_auth_params()

        config.set("Trello", "key", auth_params["key"])
        config.set("Trello", "token", auth_params["token"])

        with open('auth_params.ini', 'w') as configfile:
            config.write(configfile)
            print("auth params is available")

    return {
        "key": str(config["Trello"]["key"]),
        "token": str(config["Trello"]["token"])
    }

def get_board_id():
    if config["Trello"]["board_id"]:
        return config["Trello"]["board_id"]
    else:
        board_id = input("Enter the board ID: ")
        config.set("Trello", "board_id", board_id)
        with open('auth_params.ini', 'w') as configfile:
                config.write(configfile)
                print("board_id is available")

        return config["Trello"]["board_id"]


if __name__ == "__main__":
    add_auth_params()