import os
import sys
import random
import pygame as pg
import time


WIDTH, HEIGHT = 1600, 900
DELTA = {
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0), 
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect，または，爆弾Rectの画面内外判定用の関数
    引数：こうかとんRect，または，爆弾Rect
    戻り値：横方向判定結果，縦方向判定結果（True：画面内／False：画面外）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: 
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def gamenhyouji(screen):
    """
    GameOverの画面内表示用の関数
    引数：screen
    戻り値：screenをblitしたもの
    """
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    enn_1 = pg.Surface((20, 20))
    pg.draw.circle(enn_1, (255, 0, 0), (10, 10), 10)
    pg.draw.rect(screen,(255,255,255),(900,400))
    fonto = pg.font.Font(None, 80) 
    txt = fonto.render("Game Over",
                         True, (255, 255, 255))
    return screen.blit(txt, [900, 400])


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk2_img = pg.transform.flip(kk_img, True, False)
    JISYO = {
        (-5, 0): kk_img,
        (-5, -5): pg.transform.rotozoom(kk_img, 315, 1.0),
        (0, -5): pg.transform.rotozoom(kk2_img, 90, 1.0),
        (+5, -5): pg.transform.rotozoom(kk2_img, 45, 1.0),
        (+5, 0): kk2_img,
        (+5, +5): pg.transform.rotozoom(kk2_img, 315, 1.0),
        (0, +5): pg.transform.rotozoom(kk2_img, 270, 1.0),
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0),
        (0, 0): kk_img
    }
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    enn=pg.Surface((20,20))
    enn.set_colorkey((0,0,0))
    pg.draw.circle(enn, (255,0,0),(10,10),10)
    enn_rct=enn.get_rect()
    enn_rct.center=random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx, vy = +5, +5
    

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            if kk_rct.colliderect(enn_rct):
                print("Game Over")
                gamenhyouji(screen)
                time.sleep(5)
                pg.display.update()
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
              sum_mv[0] += v[0]
              sum_mv[1] += v[1]
            for i in JISYO.items():
                if (k,v):
                    kk_img = i

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        kk_img = JISYO[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)
        enn_rct.move_ip(vx,vy)
        screen.blit(enn,enn_rct)
        yoko, tate = check_bound(enn_rct)
        if not yoko:  
            vx *= -1
        if not tate:  
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
