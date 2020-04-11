import pygame
import random
import math

pygame.init()
win = pygame.display.set_mode((1500, 800))
pygame.display.set_caption("Gera Game")


def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


WalkRight = [pygame.image.load('GeraGame/pygame_right_1.png'), pygame.image.load('GeraGame/pygame_right_2.png'),
             pygame.image.load('GeraGame/pygame_right_3.png'),
             pygame.image.load('GeraGame/pygame_right_4.png'), pygame.image.load('GeraGame/pygame_right_5.png'),
             pygame.image.load('GeraGame/pygame_right_6.png'), ]

WalkLeft = [pygame.image.load('GeraGame/pygame_left_1.png'), pygame.image.load('GeraGame/pygame_left_2.png'),
            pygame.image.load('GeraGame/pygame_left_3.png'),
            pygame.image.load('GeraGame/pygame_left_4.png'), pygame.image.load('GeraGame/pygame_left_5.png'),
            pygame.image.load('GeraGame/pygame_left_6.png'), ]
PiratRight = [pygame.image.load('GeraGame/2_entity_000_WALK_000.png'),
              pygame.image.load('GeraGame/2_entity_000_WALK_001.png'),
              pygame.image.load('GeraGame/2_entity_000_WALK_002.png'),
              pygame.image.load('GeraGame/2_entity_000_WALK_003.png'),
              pygame.image.load('GeraGame/2_entity_000_WALK_004.png'),
              pygame.image.load('GeraGame/2_entity_000_WALK_005.png'),
              pygame.image.load('GeraGame/2_entity_000_WALK_006.png')]
PiratLeft = [pygame.image.load('GeraGame/2_entity_000_WALKLeft_000.png'),
             pygame.image.load('GeraGame/2_entity_000_WALKLeft_001.png'),
             pygame.image.load('GeraGame/2_entity_000_WALKLeft_002.png'),
             pygame.image.load('GeraGame/2_entity_000_WALKLeft_003.png'),
             pygame.image.load('GeraGame/2_entity_000_WALKLeft_004.png'),
             pygame.image.load('GeraGame/2_entity_000_WALKLeft_005.png'),
             pygame.image.load('GeraGame/2_entity_000_WALKLeft_006.png')]
BG = pygame.image.load('GeraGame/BG.jpg')
PiratStand = pygame.image.load('GeraGame/2_entity_000_ATTACK_003.png')
PlayerStand = pygame.image.load('GeraGame/pygame_idle.png')

clock = pygame.time.Clock()
x = 50
y = 50
width = 60
height = 71
speed = 5

IsJump = False
JumpCount = 10

left = False
right = False

AnimCount = 0

BulletType = "OrdinaryBullet"


class snaryad():
    def __init__(self, x, y, radius, color, BiasX, BiasY, damage):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.BiasX = BiasX
        self.BiasY = BiasY
        self.damage = damage

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class OrdinaryBullet(snaryad):
    def __init__(self, x, y, radius, color, BiasX, BiasY, damage, type):
        super(OrdinaryBullet, self).__init__(x, y, radius, color, BiasX, BiasY, damage)
        self.type = type


class TeleportBullet(snaryad):
    def __init__(self, x, y, radius, color, BiasX, BiasY, damage, type):
        super(TeleportBullet, self).__init__(x, y, radius, color, BiasX, BiasY, damage)
        self.type = type


class Person():
    def __init__(self, x, y, width, height, speed, left, right, AnimCount, WalkRight, WalkLeft, PlayerStand, health,
                 Colors):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.left = left
        self.right = right
        self.AnimCount = AnimCount
        self.WalkRight = WalkRight
        self.WalkLeft = WalkLeft
        self.PlayerStand = PlayerStand
        self.health = health
        self.Colors = Colors

    def draw(self, win):
        if self.AnimCount + 1 >= 30:
            self.AnimCount = 0
        if self.left:
            win.blit(self.WalkLeft[self.AnimCount // round(30 / len(self.WalkLeft))], (self.x, self.y))
            self.AnimCount += 1
        elif self.right:
            win.blit(self.WalkRight[self.AnimCount // round(30 / len(self.WalkRight))], (self.x, self.y))
            self.AnimCount += 1
        else:
            win.blit(self.PlayerStand, (self.x, self.y))


class Tramp(Person):
    def __init__(self, x, y, width, height, speed, left, right, AnimCount, WalkRight, WalkLeft, PlayersStand, health,
                 IsJump,
                 JumpCount,
                 BulletType, Colors):
        super(Tramp, self).__init__(x, y, width, height, speed, left, right, AnimCount, WalkRight, WalkLeft,
                                    PlayersStand, health, Colors)
        self.IsJump = IsJump
        self.JumpCount = JumpCount
        self.BulletType = BulletType


class Pirat(Person):
    def __init__(self, x, y, width, height, speed, left, right, AnimCount, WalkRight, WalkLeft, PlayerStand, health,
                 Colors, TimeToShoot):
        super(Pirat, self).__init__(x, y, width, height, speed, left, right, AnimCount, WalkRight, WalkLeft,
                                    PlayerStand, health, Colors)
        self.TimeToShoot = TimeToShoot


def DrawWindow():
    global Persons
    global bullets
    win.fill((0, 0, 0))
    win.blit(BG, (0, 0))
    for charaster in Persons:
        charaster.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


Persons = [
    Tramp(x, y, width, height, speed, left, right, AnimCount, WalkRight, WalkLeft, PlayerStand, 10, IsJump, JumpCount,
          BulletType, [(0, 0, 0), (0, 0, 255)])]

bullets = []
run = True
while run:

    clock.tick(60)

    for event in pygame.event.get():  # обрабатываем единичные нажатия
        if (event.type == pygame.QUIT):
            run = False
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if (Persons[0].BulletType == "OrdinaryBullet"):
                x1 = round(Persons[0].x + Persons[0].width // 2)
                y1 = round(Persons[0].y + Persons[0].height // 2 + 10)
                tox = event.pos[0]
                toy = event.pos[1]
                k = (math.sqrt((toy - Persons[0].y) ** 2 + (tox - Persons[0].x) ** 2) / 4) / 2
                BiasX = round((tox - x1) / k)
                BiasY = round((toy - y1) / k)
                bullets.append(OrdinaryBullet(x1, y1, 5, (0, 0, 0), BiasX, BiasY, 1, "OrdinaryBullet"))
            if (Persons[0].BulletType == "TeleportBullet"):
                q = 0
                for bullet in bullets:
                    if (bullet.type == "TeleportBullet"):
                        q = 1
                        Persons[0].x = bullet.x
                        Persons[0].y = bullet.y
                        bullets.pop(bullets.index(bullet))
                if (q == 0):
                    x1 = round(Persons[0].x + Persons[0].width // 2)
                    y1 = round(Persons[0].y + Persons[0].height // 2) + 10
                    tox = event.pos[0]
                    toy = event.pos[1]
                    k = (math.sqrt((toy - Persons[0].y) ** 2 + (tox - Persons[0].x) ** 2) / 4) / 2.5
                    BiasX = round((tox - x1) / k)
                    BiasY = round((toy - y1) / k)
                    bullets.append(TeleportBullet(x1, y1, 10, (0, 0, 255), BiasX, BiasY, 1, "TeleportBullet"))
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_1):
                Persons[0].BulletType = "OrdinaryBullet"
            if (event.key == pygame.K_2):
                Persons[0].BulletType = "TeleportBullet"
            if (event.key == pygame.K_p):
                L = False
                R = False
                w = 140
                h = 119
                s = 3
                Anim = 0
                t = 0
                Persons.append(
                    Pirat(random.randint(5, 1450), random.randint(5, 750), w, h, s, L, R, Anim, PiratRight,
                          PiratLeft, PiratStand, 10, [(255, 0, 0), (0, 0, 255)], t))
    for bullet in bullets:
        for charaster in Persons:
            if (not charaster.Colors.__contains__(bullet.color) and (dist(round(charaster.x + charaster.width // 2),
                                                                          round(
                                                                              charaster.y + charaster.height // 2) + 10,
                                                                          bullet.x,
                                                                          bullet.y) < charaster.height / 2)):
                charaster.health -= bullet.damage
                bullets.pop(bullets.index(bullet))
                if (charaster.health <= 0):
                    Persons.pop(Persons.index(charaster))
                break
    for bullet in bullets:
        if bullet.x < 1500 and bullet.x > 0 and bullet.y > 0 and bullet.y < 800:
            bullet.x += bullet.BiasX
            bullet.y += bullet.BiasY
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if (keys[pygame.K_a]) and Persons[0].x > 5:
        Persons[0].x -= Persons[0].speed
        Persons[0].left = True
        Persons[0].right = False

    elif (keys[pygame.K_d]) and Persons[0].x < 1500 - Persons[0].width - 5:
        Persons[0].x += Persons[0].speed
        Persons[0].right = True
        Persons[0].left = False
    else:
        Persons[0].left = False
        Persons[0].right = False
        Persons[0].AnimCount = 0

    if not (Persons[0].IsJump):
        if (keys[pygame.K_w]) and Persons[0].y > 5:
            Persons[0].y -= Persons[0].speed + 2

        if (keys[pygame.K_s]) and Persons[0].y < 800 - Persons[0].height - 5:
            Persons[0].y += Persons[0].speed + 2

        if (keys[pygame.K_SPACE]):
            Persons[0].IsJump = True
    else:
        if Persons[0].JumpCount >= -10:
            if (Persons[0].JumpCount >= 0):
                Persons[0].y -= (Persons[0].JumpCount ** 2) / 5
            else:
                Persons[0].y += (Persons[0].JumpCount ** 2) / 5

            Persons[0].JumpCount -= 1
        else:
            Persons[0].IsJump = False
            Persons[0].JumpCount = 10
    for i in range(1, len(Persons)):
        Persons[i].TimeToShoot += 1
        if(Persons[i].TimeToShoot >= 100):
            Persons[i].TimeToShoot = 0
            x1 = round(Persons[i].x + Persons[i].width // 2)
            y1 = round(Persons[i].y + Persons[i].height // 2 + 10)
            tox = Persons[0].x
            toy = Persons[0].y
            k = (math.sqrt((toy - y1) ** 2 + (tox - x1) ** 2) / 4) / 2
            BiasX = round((tox - x1) / k)
            BiasY = round((toy - y1) / k)
            bullets.append(OrdinaryBullet(x1, y1, 5, (255, 0, 0), BiasX, BiasY, 1, "OrdinaryBullet"))

    DrawWindow()
pygame.quit()
