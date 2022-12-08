import arcade
import random

SCREEN_WIDTH = 732
SCREEN_HEIGHT = 410

# These numbers represent "states" that the game can be in.
GAME_INTRO = 1
GAME_RUNNING = 2
GAME_OVER = 3
TIMEBETWEENDROPS = 100

# Index of textures, first element faces left, second faces right
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1


class Chicken(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.scale = 0.2
        self.textures = []

        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        texture = arcade.load_texture("images/chicken.png")
        self.textures.append(texture)
        texture = arcade.load_texture("images/chicken-right.png")
        self.textures.append(texture)

        # By default, face right.
        self.texture = texture

    def update(self):

        # bounce off sides
        if self.left <= 71 or self.right >= 659:
            self.change_x *= -1

        elif random.randrange(200) == 0:
            self.change_x *= -1

        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]

        self.center_x += self.change_x
        super(Chicken, self).update()


class MyApplication(arcade.Window):
    """ Main application class """

    def __init__(self, width, height):
        super().__init__(width, height)
        # Background image will be stored in this variable
        self.background = None

        self.frame_count = 0
        self.all_sprites_list = []
        self.Chicken = None
        self.egg_list = []

        self.player = None
        self.score = 0
        self.score_text = None
        self.current_state = None
        self.dropTime = TIMEBETWEENDROPS
        self.difficulty = 70  # Intial speed determiner

        # Do show the mouse cursor
        self.set_mouse_visible(True)

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):

        self.background = arcade.load_texture("images/coop.jpg")
        self.all_sprites_list = arcade.SpriteList()
        self.egg_list = arcade.SpriteList()
        # Score
        self.score = 0
        self.current_state = GAME_INTRO

        self.player = arcade.Sprite("images/bigbird.png", 1)
        self.player.scale = 0.3
        self.all_sprites_list.append(self.player)

        self.chicken = Chicken()
        self.chicken.center_x = 200
        self.chicken.center_y = SCREEN_HEIGHT - (1.7 * self.chicken.height)
        self.chicken.angle = 0
        self.chicken.change_x = 1
        self.all_sprites_list.append(self.chicken)

    def on_draw(self):
        """Render the screen. """

        arcade.start_render()
        # Draw the background texture
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        if self.current_state == GAME_INTRO:
            arcade.draw_text("Big Bird's Egg Catch 2.0", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30,
                             arcade.color.WHITE, font_size=30, anchor_x="center")
            arcade.draw_text("Help Big Bird catch the chicken's eggs!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 25,
                             arcade.color.WHITE, font_size=20, anchor_x="center")
            arcade.draw_text("Press the space bar to Start", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                             arcade.color.GRAY, font_size=20, anchor_x="center")


        elif self.current_state == GAME_RUNNING:
            self.draw_game()

        else:
            # End game
            self.draw_game_over()

    def draw_game(self):

        self.chicken.draw()
        self.egg_list.draw()
        self.player.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 385, arcade.color.WHITE, 14)

    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """

        output = "Game Over"
        arcade.draw_text(output, 180, 180, arcade.color.WHITE, 54)

        if self.frame_count == 100:
            print("done")
            # arcade.finish_render()
            # arcade.close_window()

    def update(self, delta_time):
        """All the logic to move, and the game logic goes here. """

        # Use this if you want something to stay on the screen for a limited time
        self.frame_count += 1

        # Determine when to drop next egg
        if self.dropTime == 0:
            egg = arcade.Sprite("images/egg.png")
            egg.center_x = self.chicken.center_x
            egg.top = self.chicken.bottom
            egg.change_y = -2
            egg.scale = 0.75

            self.egg_list.append(egg)
            self.all_sprites_list.append(egg)
            self.dropTime = TIMEBETWEENDROPS * (random.randrange(self.difficulty, 100) / 100)

        else:
            self.dropTime = self.dropTime - 1

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player,
                                                        self.egg_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for egg in hit_list:
            egg.kill()
            self.score += 1

        if self.score % 100 == 0 and self.score > 0 and self.difficulty > 0:
            self.difficulty -= 10

        # Get rid of the egg when it flies off-screen
        for egg in self.egg_list:
            if egg.top < 0:
                egg.kill()
                self.current_state = GAME_OVER
                self.frame_count = 0

        self.egg_list.update()
        self.chicken.update()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """ Called whenever the mouse moves. """
        self.player.center_x = x
        self.player.center_y = 90

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.current_state == GAME_INTRO:
                self.current_state = GAME_RUNNING
        elif key == arcade.key.ESCAPE:
            if self.current_state == GAME_OVER:
                self.close()

def main():
    """ Main method """
    window = MyApplication(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


main()
