from elements import Adventure


def main():
    main_game = Adventure(bot_type="breadth_first_search")
    main_game.game_init('bot')

if __name__ == "__main__":
    main()
