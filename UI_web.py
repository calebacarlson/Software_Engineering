import webbrowser

path = input("which one do you want all-games (1), one-game(2), or default(any other key)")

if (path == "1"):
    url = "https://3aspume2jt.us-east-1.awsapprunner.com/all_games"
    webbrowser.open(url)

elif (path == "2"):
    game_name = input("whats the name of the game? Ex. test-1, test-2")
    url = "https://3aspume2jt.us-east-1.awsapprunner.com/one_game/"+game_name
    webbrowser.open(url)
else:
    url = "https://3aspume2jt.us-east-1.awsapprunner.com"
    webbrowser.open(url)
