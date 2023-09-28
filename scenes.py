import pygame, math
import gridlogic as gl
import random

class SceneManager():

    scene_context = {}

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((300, 300))
        self.current_scene = None
        

    def get_scene(self):
        return self.current_scene
    
    def start_scene(self, scene):
        self.current_scene = scene(self.screen, self.scene_context)

    def set_scene_context(self, context):
        self.scene_context = context
        
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SceneManager, cls).__new__(cls)
        return cls.instance
    

class Scene():

    #MUST BE OVERRIDDEN ELSE IT WILL SHARE ACROSS SCENES
    interactables = []

    def __init__(self, screen, context) -> None:
        self.screen = screen
    
    def create_button(self, size=(150, 50), position=(150, 150), border_size = 4, border_radius=0,
                      color=(0, 0, 0), border_color=(255, 255, 255), text='', text_color=(255, 255, 255),
                      action=lambda: print("Hello")):
        
        btn_rect = pygame.Rect(0, 0, 0, 0)
        btn_rect.size = size
        btn_rect.center = position
        border_box = pygame.draw.rect(self.screen, border_color, btn_rect, border_radius=border_radius)
        btn_rect.size = (size[0] - border_size, size[1] - border_size)
        btn_rect.center = position
        inner_box = pygame.draw.rect(self.screen, color, btn_rect, border_radius=border_radius)

        btn_font = pygame.font.Font('freesansbold.ttf', 24)
        btn = btn_font.render(text, True, text_color)
        btn_rect = btn.get_rect(center=(position))
        self.screen.blit(btn, btn_rect)
        self.interactables.append((border_box, action))
    
    def create_section(self, position=(0, 0), size=(100, 100), color=(30, 30, 30)):
        game_area_rect = pygame.Rect(0, 0, 0, 0)
        game_area_rect.size = size
        game_area_rect.center = (position[0] + (size[0] // 2), position[1] + (size[1] // 2))
        return pygame.draw.rect(self.screen, color, game_area_rect)

    def delete_scene(self):
        self.screen.fill((0, 0, 0))
        self.interactables = []
        del self

    def next_scene(self, scene):
        SceneManager().start_scene(scene)


class TitleScene(Scene):

    interactables = []

    def __init__(self, screen, context) -> None:
        super().__init__(screen, context)
        self.interactables = []
        self.screen.fill((30, 30, 30))
        font = pygame.font.Font('freesansbold.ttf', 32)
        game_title = font.render("Tic Tac Toe", True, (255, 255, 255))
        text_rect = game_title.get_rect()
        text_rect.center = (150, 100)
        self.screen.blit(game_title, text_rect)

        self.create_button(color=(30, 30, 30), border_radius=20, text='1 Player', position=(150, 180), action=self.one_player_scene)
        self.create_button(color=(30, 30, 30), border_radius=20, text='2 Player', position=(150, 250), action=self.two_player_scene)

    def one_player_scene(self):
        self.delete_scene()
        SceneManager().set_scene_context({"mode": 1})
        self.next_scene(GameScene)
        

    def two_player_scene(self):
        self.delete_scene()
        SceneManager().set_scene_context({"mode": 2})
        self.next_scene(GameScene)
        

class GameScene(Scene):

    interactables = []

    def __init__(self, screen, context) -> None:
        super().__init__(screen, context)
        self.interactables = []
        self.context = context
        self.game_finished = False
        self.draw = False
        self.screen.fill((30, 30, 30))
        self.font = pygame.font.Font('freesansbold.ttf', 50)
        self.current_player = 'X'
        self.game_grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        self.game_grid_dict = {
            1: self.create_section(color=(40, 40, 40)),
            2: self.create_section(position=(100, 0)),
            3: self.create_section(color=(40, 40, 40), position=(200, 0)),
            4: self.create_section(position=(0, 100)),
            5: self.create_section(color=(40, 40, 40), position=(100, 100)),
            6: self.create_section(position=(200, 100)),
            7: self.create_section(color=(40, 40, 40), position=(0, 200)),
            8: self.create_section(position=(100, 200)),
            9: self.create_section(color=(40, 40, 40), position=(200, 200)),
        }

        self.open_locations = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for index, collider in self.game_grid_dict.items():
            self.interactables.append((collider, lambda x=index: self.play_made(x)))
    
    def play_made(self, location):
        if location not in self.open_locations:
            return
        
        self.update_grid_ui(location)
        self.update_game_grid(location)
        self.check_for_match()
        if self.game_finished == True:
                self.game_end()
                return
        
        self.current_player = self.swap_player()
        if self.context["mode"] == 2:
            return
        elif self.context["mode"] == 1:
            self.computer_play_made()
            
    
    def swap_player(self):
        if self.current_player == 'X':
            return 'O'
        else:
            return 'X'
    
    def computer_play_made(self):
        priority_spots = gl.almost_match(self.game_grid, computer=self.current_player, player=self.swap_player())
        if priority_spots:
            place = random.choice(priority_spots)
        else:
            place = random.choice(self.open_locations)

        self.update_grid_ui(place)
        self.update_game_grid(place)
        self.check_for_match()
        if self.game_finished == True:
                self.game_end()
                return
        
        self.current_player = self.swap_player()

    def update_grid_ui(self, location):
        mark = self.font.render(self.current_player, True, (255, 255, 255))
        position = self.game_grid_dict[location].center
        mark_rect = mark.get_rect(center=(position))
        self.screen.blit(mark, mark_rect)
        self.open_locations.pop(self.open_locations.index(location))

    def update_game_grid(self, location):
        grid_index = math.ceil(location / 3) - 1
        axis_index = (location % 3) - 1
        self.game_grid[grid_index][axis_index] = self.current_player
 
    def check_for_match(self):
        if gl.check_horizonal_match(self.game_grid) or gl.check_vertical_match(self.game_grid) or gl.check_diagonal_match(self.game_grid):
            self.interactables = []
            self.game_finished = True
        elif gl.grid_full(self.game_grid):
            self.interactables = []
            self.game_finished = True
            self.draw = True

    def game_end(self):
        bg_rect = pygame.Rect(0, 0, 300, 300)
        bg_surf = pygame.Surface(bg_rect.size)
        bg_surf.fill((0, 0, 0))
        bg_surf.set_alpha(128)
        self.screen.blit(bg_surf, bg_rect)
        pygame.draw.rect(bg_surf, (0, 0, 0, 128), bg_rect)
        font = pygame.font.Font('freesansbold.ttf', 32)
        if self.draw:
            end_title = font.render("Draw!", True, (255, 255, 255))
        else:
            end_title = font.render(f"{self.current_player} Wins!", True, (255, 255, 255))
        text_rect = end_title.get_rect()
        text_rect.center = (150, 100)
        self.screen.blit(end_title, text_rect)

        self.create_button(color=(30, 30, 30), border_radius=20, text='Play Again', position=(150, 180), action=self.play_again)
        self.create_button(color=(30, 30, 30), border_radius=20, text='Title Screen', position=(150, 250), action=self.back_to_title)

    def back_to_title(self):
        self.delete_scene()
        self.next_scene(TitleScene)

    def play_again(self):
        self.delete_scene()
        SceneManager().set_scene_context(self.context)
        self.next_scene(GameScene)
