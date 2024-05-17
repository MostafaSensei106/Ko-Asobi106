import pygame
import cv2
import mediapipe as mp
import sys
import tkinter
from pygame.math import Vector2
from tkinter import messagebox
import random


mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 700)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)


class Main_Game_Logic:

    def BackGround_Grass_Draw(self):
        Green_Color = (206, 205, 227)

        for row in range(Grid_Number):
            for col in range(Grid_Number):
                BackGround_X_Pos = col * Grid_Size
                BackGround_Y_Pos = row * Grid_Size
                if (row + col) % 2 == 0:
                    Green_Rect = pygame.Rect(BackGround_X_Pos, BackGround_Y_Pos, Grid_Size, Grid_Size)
                    pygame.draw.rect(screen, Green_Color, Green_Rect)

    def __init__(self):
        self.event = None
        self.new_Snake = Snake()
        self.new_Appel = Appel()

    def Opject_Draw(self):
        self.BackGround_Grass_Draw()
        self.new_Snake.Snake_Draw()
        self.new_Appel.Appel_Draw()
        self.Score_Draw()


    def AI_Control(self):
        ret, frame = cap.read()
        if not ret:
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                print(hand_landmarks)
                # Get landmarks of the index finger and thumb
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                # Convert coordinates from normalized to pixel values
                img_h, img_w, _ = frame.shape
                index_finger_x = int(index_finger_tip.x * img_w)
                index_finger_y = int(index_finger_tip.y * img_h)
                thumb_x = int(thumb_tip.x * img_w)
                thumb_y = int(thumb_tip.y * img_h)

                # Calculate distance between index finger and thumb
                index_thumb_dist = ((index_finger_x - thumb_x) ** 2 + (index_finger_y - thumb_y) ** 2) ** 0.5

                # Determine the direction of movement based on hand gestures
                if thumb_x < index_finger_x:
                    # Index finger to the right of thumb, move right
                    self.new_Snake.Snake_Direction = Vector2(1, 0)
                elif thumb_x > index_finger_x:
                    # Index finger to the left of thumb, move left
                    self.new_Snake.Snake_Direction = Vector2(-1, 0)
                elif thumb_y < index_finger_y:
                    # Index finger below thumb, move down
                    self.new_Snake.Snake_Direction = Vector2(0, 1)
                elif thumb_y > index_finger_y:
                    # Index finger above thumb, move up
                    self.new_Snake.Snake_Direction = Vector2(0, -1)

                # Display the camera output in a new window
                cv2.imshow('Camera Output', frame)

                if cv2.waitKey(1) == ord('q'):
                    break

    def Snake_Control(self):



        if (event.type == Screen_Update):
            self.new_Snake.Snake_Move()
            self.Snake_Appel_Check()
            #self.Check_if_Snake_Is_Dead()
        if event.type == pygame.KEYDOWN:

            # Up Down Left Right  Press Key
            if event.key == pygame.K_UP:
                if self.new_Snake.Snake_Direction.y != 1:
                    self.new_Snake.Snake_Direction = Vector2(0, -1)

            if event.key == pygame.K_DOWN:
                if self.new_Snake.Snake_Direction.y != -1:
                    self.new_Snake.Snake_Direction = Vector2(0, 1)

            if event.key == pygame.K_LEFT:
                if self.new_Snake.Snake_Direction.x != 1:
                    self.new_Snake.Snake_Direction = Vector2(-1, 0)

            if event.key == pygame.K_RIGHT:
                if self.new_Snake.Snake_Direction.x != -1:
                    self.new_Snake.Snake_Direction = Vector2(1, 0)

            # W A S D Press Key
            if event.key == pygame.K_w:
                if self.new_Snake.Snake_Direction.y != 1:
                    self.new_Snake.Snake_Direction = Vector2(0, -1)

            if event.key == pygame.K_s:
                if self.new_Snake.Snake_Direction.y != -1:
                    self.new_Snake.Snake_Direction = Vector2(0, 1)

            if event.key == pygame.K_a:
                if self.new_Snake.Snake_Direction.x != 1:
                    self.new_Snake.Snake_Direction = Vector2(-1, 0)

            if event.key == pygame.K_d:
                if self.new_Snake.Snake_Direction.x != -1:
                    self.new_Snake.Snake_Direction = Vector2(1, 0)

    def Snake_Appel_Check(self):
        if self.new_Appel.Vector_Position == self.new_Snake.Snake_Body[0]:
            self.new_Snake.Snake_Grow_UP()
            self.new_Appel.Random_Appel_Position()
            for block in self.new_Snake.Snake_Body[1:]:
                if block == self.new_Appel.Vector_Position:
                    self.new_Appel.Random_Appel_Position()
            self.new_Snake.Play_Snake_Sound()

    # def Check_if_Snake_Is_Dead(self):
    #     head = self.new_Snake.Snake_Body[0]
    #
    #     # Check if the snake is out of bounds
    #     if not (0 <= head.x < Grid_Number) or not (0 <= head.y < Grid_Number):
    #         self.Game_Over()
    #         return
    #
    #     # Check if the snake has collided with itself
    #     for block in self.new_Snake.Snake_Body[1:]:
    #         if block == head:
    #             self.Game_Over()
    #             return

    def Score_Draw(self):
        self.score = len(self.new_Snake.Snake_Body) - 3
        self.Score_Text = str(self.score)
        Score_Land = Sensei_Font.render(self.Score_Text, True, (56, 74, 12))
        Score_X_Pos = int(Grid_Size * Grid_Number - 60)
        Score_Y_Pos = int(Grid_Size * Grid_Number - 40)
        Score_Rect = Score_Land.get_rect(center=(Score_X_Pos, Score_Y_Pos))
        Appel_Rect = Appel_image.get_rect(midright=(Score_Rect.left, Score_Rect.centery))
        BackGround_Rect = pygame.Rect(Appel_Rect.left, Appel_Rect.top, Appel_Rect.width + Score_Rect.width + 6,
                                      Appel_Rect.height)

        pygame.draw.rect(screen, (167, 209, 61), BackGround_Rect)
        screen.blit(Score_Land, Score_Rect)
        screen.blit(Appel_image, Appel_Rect)
        pygame.draw.rect(screen, (56, 74, 12), BackGround_Rect, 2)
        print(self.score)
        return self.score

    def Show_Score_Massage(self):
        window = tkinter.Tk()
        window.title('Score')
        window.geometry('0x0')
        window.resizable(False, False)
        var = window.withdraw
        tkinter.messagebox.showinfo("Ko-Asobi Game Over", f"Good Game. \n Your Score : {self.score}")
        window.destroy()

    def Game_Over(self):
        self.Show_Score_Massage()
        pygame.quit()
        sys.exit()


class Snake:
    def __init__(self):
        self.Snake_Body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.Snake_Direction = Vector2(1, 0)
        self.new_Snake_Grow = False

        self.Head_Up = pygame.image.load("../Assets/Assets_Ko-Asobi_Snakke_Game/head_up.png").convert_alpha()
        self.Head_Down = pygame.image.load("../Assets/Assets_Ko-Asobi_Snakke_Game/head_down.png").convert_alpha()
        self.Head_Right = pygame.image.load("../Assets/Assets_Ko-Asobi_Snakke_Game/head_right.png").convert_alpha()
        self.Head_Left = pygame.image.load("../Assets/Assets_Ko-Asobi_Snakke_Game/head_left.png").convert_alpha()

        self.Tail_Up = pygame.image.load("../Assets/Assets_Ko-Asobi_Snakke_Game/tail_up.png").convert_alpha()
        self.Tail_Down = pygame.image.load("../Assets/Assets_Ko-Asobi_Snakke_Game/tail_down.png").convert_alpha()
        self.Tail_Right = pygame.image.load("../Assets/Assets_Ko-Asobi_Snakke_Game/tail_right.png").convert_alpha()
        self.Tail_Left = pygame.image.load("../Assets/Assets_Ko-Asobi_Snakke_Game/tail_left.png").convert_alpha()

        self.Body_Ver = pygame.image.load("../Assets/Assets_Ko-Asobi_Snakke_Game/body_vertical.png").convert_alpha()
        self.Body_Hor = pygame.image.load(
            "../Assets/Assets_Ko-Asobi_Snakke_Game/body_horizontal.png").convert_alpha()

        self.Body_TR = pygame.image.load("../Assets/Assets_Ko-Asobi_Snakke_Game/body_topright.png").convert_alpha()
        self.Body_TL = pygame.image.load("../Assets/Assets_Ko-Asobi_Snakke_Game/body_topleft.png").convert_alpha()
        self.Body_BR = pygame.image.load(
            "../Assets/Assets_Ko-Asobi_Snakke_Game/body_bottomright.png").convert_alpha()
        self.Body_BL = pygame.image.load(
            "../Assets/Assets_Ko-Asobi_Snakke_Game/body_bottomleft.png").convert_alpha()

        self.Eat_Sound = pygame.mixer.Sound("../Sound/Eat_Sound.wav")

    def Snake_Draw(self):

        self.Snake_Head_Change()
        self.Snake_Tail_Change()

        for index, block in enumerate(self.Snake_Body):
            Snake_Pos_X = int(block.x * Grid_Size)
            Snake_Pos_Y = int(block.y * Grid_Size)
            block_Rect = pygame.Rect(Snake_Pos_X, Snake_Pos_Y, Grid_Size, Grid_Size)

            if index == 0:
                screen.blit(self.Head, block_Rect)
            elif index == len(self.Snake_Body) - 1:
                screen.blit(self.Tail, block_Rect)
            else:
                Next_block = self.Snake_Body[index - 1] - block
                Previous_Block = self.Snake_Body[index + 1] - block
                if Previous_Block.x == Next_block.x:
                    screen.blit(self.Body_Ver, block_Rect)
                elif Previous_Block.y == Next_block.y:
                    screen.blit(self.Body_Hor, block_Rect)
                else:
                    if Previous_Block.x == -1 and Next_block.y == -1 or Previous_Block.y == -1 and Next_block.x == -1:
                        screen.blit(self.Body_TL, block_Rect)

                    if Previous_Block.x == -1 and Next_block.y == 1 or Previous_Block.y == 1 and Next_block.x == -1:
                        screen.blit(self.Body_BL, block_Rect)

                    if Previous_Block.x == 1 and Next_block.y == -1 or Previous_Block.y == -1 and Next_block.x == 1:
                        screen.blit(self.Body_TR, block_Rect)

                    if Previous_Block.x == 1 and Next_block.y == 1 or Previous_Block.y == 1 and Next_block.x == 1:
                        screen.blit(self.Body_BR, block_Rect)

    def Snake_Head_Change(self):
        Snake_Head_Re = self.Snake_Body[1] - self.Snake_Body[0]
        if Snake_Head_Re == Vector2(1, 0):
            self.Head = self.Head_Left
        elif Snake_Head_Re == Vector2(-1, 0):
            self.Head = self.Head_Right
        elif Snake_Head_Re == Vector2(0, 1):
            self.Head = self.Head_Up
        elif Snake_Head_Re == Vector2(0, -1):
            self.Head = self.Head_Down

    def Snake_Tail_Change(self):
        Snake_Tail_Re = self.Snake_Body[-2] - self.Snake_Body[-1]
        if Snake_Tail_Re == Vector2(1, 0):
            self.Tail = self.Tail_Left
        elif Snake_Tail_Re == Vector2(-1, 0):
            self.Tail = self.Tail_Right
        elif Snake_Tail_Re == Vector2(0, 1):
            self.Tail = self.Tail_Up
        elif Snake_Tail_Re == Vector2(0, -1):
            self.Tail = self.Tail_Down

    def Snake_Move(self):
        if self.new_Snake_Grow:
            Snake_Body_Copy = self.Snake_Body[:]
            Snake_Body_Copy.insert(0, Snake_Body_Copy[0] + self.Snake_Direction)
            self.Snake_Body = Snake_Body_Copy[:]
            self.new_Snake_Grow = False
        else:
            Snake_Body_Copy = self.Snake_Body[:-1]
            Snake_Body_Copy.insert(0, Snake_Body_Copy[0] + self.Snake_Direction)
            self.Snake_Body = Snake_Body_Copy[:]

    def Snake_Grow_UP(self):
        self.new_Snake_Grow = True

    def Play_Snake_Sound(self):
        self.Eat_Sound.play()


class Appel:
    def __init__(self):
        self.X_Postion = random.randrange(0, Grid_Number - 1)
        self.Y_Postion = random.randrange(0, Grid_Number - 1)
        self.Vector_Position = Vector2(self.X_Postion, self.Y_Postion)

    def Random_Appel_Position(self):
        self.X_Postion = random.randrange(0, Grid_Number - 1)
        self.Y_Postion = random.randrange(0, Grid_Number - 1)
        self.Vector_Position = Vector2(self.X_Postion, self.Y_Postion)

    def Appel_Draw(self):
        Appel_Rect = pygame.Rect(self.X_Postion * Grid_Size, self.Y_Postion * Grid_Size, Grid_Size, Grid_Size)
        screen.blit(Appel_image, Appel_Rect)
        # pygame.draw.rect(screen, (215, 59, 88), Appel_Rect)


pygame.init()
Grid_Size = 40
Grid_Number = 17
FPS = 60
Timer_Millis = 150
Primary_Color = (69, 94, 158)
pygame.display.set_caption("Ko-Asobi-Snake-Game")
Screen_Update = pygame.USEREVENT
screen = pygame.display.set_mode((Grid_Number * Grid_Size, Grid_Size * Grid_Number))
clock = pygame.time.Clock()
Appel_image = pygame.image.load("../Assets/Assets_Ko-Asobi_Snakke_Game/Appel_Assets.png").convert_alpha()
Sensei_Font = pygame.font.Font('../Font/YujiSyuku-Regular.ttf', 27)
Main_Game_Logic = Main_Game_Logic()

pygame.time.set_timer(Screen_Update, Timer_Millis)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        Main_Game_Logic.Snake_Control()
    screen.fill(Primary_Color)
    Main_Game_Logic.Opject_Draw()
    pygame.display.update()
    clock.tick(FPS)
