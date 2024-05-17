import pygame
import cv2
import mediapipe as mp
from pygame.math import Vector2
import  math
import random
import tkinter
from tkinter import messagebox

mp_hands = mp.solutions.hands
hand = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

pygame.init()
width_Screen, height_Screen = 900, 600
FPS = 60
Ball_Radius = 7
Player_Width, Player_Height = 20, 100
BackGround_Color = (40, 42, 56)
Item_Color = (133, 122, 252) #Score And Line
PLayer_Color = (117, 216, 230)
Ball_Color = (250, 245, 126)
Win_Game = 10
screen = pygame.display.set_mode((width_Screen, height_Screen))
pygame.display.set_caption('Ko-Asobi-Pong-Game')
Sensei_Font = pygame.font.Font('../Font/YujiSyuku-Regular.ttf', 27)
Hentai_1_Sound = pygame.mixer.Sound("../Sound/Pong_Game_Sounds/Hentai_1.wav")
Hentai_2_Sound = pygame.mixer.Sound("../Sound/Pong_Game_Sounds/Hentai_2.wav")
Hentai_3_Sound = pygame.mixer.Sound("../Sound/Pong_Game_Sounds/Hentai_3.wav")
Hentai_4_Sound = pygame.mixer.Sound("../Sound/Pong_Game_Sounds/Hentai_4.wav")
Hentai_5_Sound = pygame.mixer.Sound("../Sound/Pong_Game_Sounds/Hentai_5.wav")


def Hentai_Sounds():
    Oni_Chan = random.randint(1, 5)
    if Oni_Chan == 1:
        Hentai_1_Sound.play()
    elif Oni_Chan == 2:
        Hentai_2_Sound.play()
    elif Oni_Chan == 3:
        Hentai_3_Sound.play()
    elif Oni_Chan == 4:
        Hentai_4_Sound.play()
    elif Oni_Chan == 5:
        Hentai_5_Sound.play()
    else:
        print("Oni San")

def Sensei_Ai():
    while True:
        success, frame = cap.read()
        if success:
            RGB_Frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hand.process(RGB_Frame)
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.imshow('Sensei_Pong', frame)
            if cv2.waitKey(1) == ord('q'):
                break
    cv2.destroyAllWindows()


def Player_Control(Keys, First_Player, Seconder_Player):
    success, frame = cap.read()
    if success:
        RGB_Frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand.process(RGB_Frame)
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                index_finger_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                First_Player.y = int(index_finger_tip_y * height_Screen)

                if First_Player.y < 0:
                    First_Player.y = 0
                elif First_Player.y > height_Screen - First_Player.height:
                    First_Player.y = height_Screen - First_Player.height
        # cv2.imshow('Sensei_Pong', frame)
        # if cv2.waitKey(1) == ord('q'):
        #     cv2.destroyAllWindows()

    if Keys[pygame.K_w] and First_Player.y - First_Player.Speed >= 0:
        First_Player.Player_Move(UP=True)
    if Keys[pygame.K_s] and First_Player.y + First_Player.Speed + First_Player.height <= height_Screen:
        First_Player.Player_Move(UP=False)

    if Keys[pygame.K_UP] and Seconder_Player.y - Seconder_Player.Speed >= 0:
        Seconder_Player.Player_Move(UP=True)
    if Keys[pygame.K_DOWN] and Seconder_Player.y + Seconder_Player.Speed + Seconder_Player.height <= height_Screen:
        Seconder_Player.Player_Move(UP=False)


class Player:
    Speed = 12
    Color = PLayer_Color

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def Player_Move(self, UP=True):
        if UP:
            self.y -= self.Speed
        else:
            self.y += self.Speed

    def draw_player(self, screen):
        pygame.draw.rect(screen, self.Color, (self.x, self.y, self.width, self.height))


class Ball:
    Max_Speed = 15
    Color = Ball_Color

    def __init__(self, x, y, radius):
        self.x = self.ORG_X = x
        self.y = self.ORG_Y = y
        self.radius = radius
        angel = random.uniform(0, 2 * math.pi)
        self.X_Speed = self.Max_Speed * math.cos(angel)
        self.Y_Speed = self.Max_Speed * math.sin(angel)

    def draw_ball(self, screen):
        pygame.draw.circle(screen, self.Color, (self.x, self.y), self.radius)

    def move_ball(self):
        self.x += self.X_Speed
        self.y += self.Y_Speed

    def Reset_Ball(self):
        self.x = self.ORG_X
        self.y = self.ORG_Y
        angle = random.uniform(0, 2 * math.pi)
        speed = self.Max_Speed
        self.X_Speed = speed * math.cos(angle)
        self.Y_Speed = speed * math.sin(angle)


def Draw_Game(My_Screen, Players, ball, F_Score, S_Score):
    My_Screen.fill(BackGround_Color)
    Score1 = Sensei_Font.render(f"{F_Score}", True, Item_Color)
    Score2 = Sensei_Font.render(f"{S_Score}", True, Item_Color)
    My_Screen.blit(Score1, (width_Screen / 4 - Score1.get_width() // 2, 20))
    My_Screen.blit(Score2, (width_Screen * (3 / 4) - Score2.get_width() // 2, 20))

    for Player in Players:
        Player.draw_player(My_Screen)

    for i in range(10, height_Screen, height_Screen // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(My_Screen, Item_Color, (width_Screen // 2 - 5, i, 1, height_Screen // 20))
    ball.draw_ball(My_Screen)
    pygame.display.update()






def Ball_Collision(ball, First_Player, Seconder_Player):
    if ball.y + ball.radius >= height_Screen:
        ball.Y_Speed *= -1
    elif ball.y - ball.radius <= 0:
        ball.Y_Speed *= -1

    if ball.X_Speed < 0:
        if ball.y >= First_Player.y and ball.y <= First_Player.y + First_Player.height:
            if ball.x - ball.radius <= First_Player.x + First_Player.width:
                ball.X_Speed *= -1

                Middle_Y = First_Player.y + First_Player.height / 2
                Difference_in_y = Middle_Y - ball.y
                Reduction_Factor = (First_Player.height / 2) / ball.Max_Speed
                Y_SP = Difference_in_y / Reduction_Factor
                ball.Y_Speed = -1 * Y_SP



    else:
        if ball.y >= Seconder_Player.y and ball.y <= Seconder_Player.y + Seconder_Player.height:
            if ball.x + ball.radius >= Seconder_Player.x:
                ball.X_Speed *= -1


                Middle_Y = Seconder_Player.y + Seconder_Player.height / 2
                Difference_in_y = Middle_Y - ball.y
                Reduction_Factor = (Seconder_Player.height / 2) / ball.Max_Speed
                Y_SP = Difference_in_y / Reduction_Factor
                ball.Y_Speed = -1 * Y_SP


def Window(F_Score, S_Score):
    window = tkinter.Tk()
    window.title('Winner')
    window.geometry('0x0')
    window.resizable(False, False)
    var = window.withdraw
    if F_Score > S_Score:
        tkinter.messagebox.showinfo("Ko-Asobi Game Over", f"Good Game. \nWinner Is Player 1 Score : {F_Score}")
        window.destroy()
    else:
        tkinter.messagebox.showinfo("Ko-Asobi Game Over", f"Good Game. \nWinner Is Player 2 Score : {S_Score}")


def Winer(F_Score,S_Score):
    if F_Score == Win_Game or S_Score == Win_Game:
        Window(F_Score, S_Score)


def run():
    run = True
    clock = pygame.time.Clock()
    First_Player = Player(10, height_Screen // 2 - Player_Height // 2, Player_Width, Player_Height)
    Seconder_Player = Player(width_Screen - 10 - Player_Width, height_Screen // 2 - Player_Height // 2, Player_Width,
                             Player_Height)
    ball = Ball(width_Screen // 2, height_Screen // 2, Ball_Radius)

    First_Player_Score = 0
    Seconder_Player_Score = 0

    while run:
        clock.tick(FPS)
        Draw_Game(screen, [First_Player, Seconder_Player], ball, F_Score=First_Player_Score,
                  S_Score=Seconder_Player_Score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        Keys = pygame.key.get_pressed()
        Player_Control(Keys, First_Player, Seconder_Player)
        ball.move_ball()
        Ball_Collision(ball, First_Player, Seconder_Player)
        if ball.x < 0:
            Seconder_Player_Score += 1
            #Hentai_Sounds()
            ball.Reset_Ball()
        elif ball.x > width_Screen:
            First_Player_Score += 1
            #Hentai_Sounds()
            ball.Reset_Ball()
            Winer(F_Score=First_Player_Score, S_Score=Seconder_Player_Score)

    pygame.quit()

if __name__ == '__main__':
    run()