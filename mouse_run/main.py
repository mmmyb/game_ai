from game import Game


def play_with_trained_model(show_game):
    g = Game("waco.txt", curiosity=False)
    g.ai.load("ai.json")
    if show_game:
        g.show_game()
    while True:
        g.update()
        if g.age % 10000 == 0:
            print "{:d}, e: {:0.2f}, feed: {:d}, eaten: {:d}" \
                .format(g.age, g.ai.epsilon, g.feed, g.eaten)
            print "mouse: %s, cat: %s, cheese: %s" % (g.mouse.get_position(), g.cat.get_position(), g.cheese.get_position())
            g.eaten = 0
            g.feed = 0
        if g.age % 1000000 == 0:
            g.ai.dump("ai.json")
        g.redraw()


def play_and_training_model(show_game):
    g = Game("waco.txt", curiosity=False)
    while True:
        g.update()
        if g.age % 10000 == 0:
            print "{:d}, e: {:0.2f}, feed: {:d}, eaten: {:d}" \
                .format(g.age, g.ai.epsilon, g.feed, g.eaten)
            print "mouse: %s, cat: %s, cheese: %s" % (g.mouse.get_position(), g.cat.get_position(), g.cheese.get_position())
            g.eaten = 0
            g.feed = 0
        if g.age % 1000000 == 0:
            g.ai.dump("ai.json")
        if g.age == 5000000 and show_game:
            g.show_game()
        g.redraw()


if __name__ == "__main__":
    play_with_trained_model(False)
