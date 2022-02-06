from elements import Adventure


def main():
    main_game = Adventure()
    main_game.game_init(player = 'bot', bot_type="breadth_first_tree_search")

if __name__ == "__main__":
    main()
