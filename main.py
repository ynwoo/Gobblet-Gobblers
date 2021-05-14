import sys  # sys 패키지 임포트
import time
import pygame  # 파이게임 패키지 임포트
import numpy as np
from pygame.locals import QUIT  # 파이게임의 기능 중 종료를 임포트

# 글로벌 변수 선언

# 플레이어 값을 저장 P1 or P2
player = 'P1'
# 승자의 값을 저장
winner = None
# 게임이 비겼는지 체크
draw = None
# game window 창의 크기 값 설정
width = 400
height = 600
# 배경화면 색
white = (255, 255, 255)
# 선 색
line_color = (0, 0, 0)
# 말을 선택한 상태인지 표시
choice = False
biggest = -1
col_1 = None
row_1 = None
ch = 0
turn_end = False
# 게임 진행을 위한 삼중배열
# player에 따라 1,-1 비어있으면 0
# 깊이가 종류를 표현
array = np.arange(27).reshape(3, 3, 3)
for i in range(0, 3):
    for j in range(0, 3):
        for k in range(0, 3):
            array[i][j][k] = 0

pygame.init()  # 파이게임 모듈을 초기화
fps = 30  # fps 설정
screen = pygame.display.set_mode((width, height))  # 만들 윈도우 창의 화면 크기 설정
FPSCLOCK = pygame.time.Clock()  # 설정할 프레임을 저장할 변수
pygame.display.set_caption("Gobblet Gobblers")  # 만든 윈도우창에 이름을 적는 코드

# 이미지 불러오기
initiating_window = pygame.image.load("cover.png")
p1_piece_img = pygame.image.load("p1_icon.png")
p2_piece_img = pygame.image.load("p2_icon.png")
empty_img = pygame.image.load("NULL.png")

# 이미지 스케일링
initiating_window = pygame.transform.scale(initiating_window, (width, height + 100))
p1_large_piece_img = pygame.transform.scale(p1_piece_img, (60, 60))
p1_medium_piece_img = pygame.transform.scale(p1_piece_img, (40, 40))
p1_small_piece_img = pygame.transform.scale(p1_piece_img, (20, 20))

p2_large_piece_img = pygame.transform.scale(p2_piece_img, (60, 60))
p2_medium_piece_img = pygame.transform.scale(p2_piece_img, (40, 40))
p2_small_piece_img = pygame.transform.scale(p2_piece_img, (20, 20))
empty_img = pygame.transform.scale(empty_img, (60, 60))


def limit_2(which_piece):  # 두개씩만 놓을 수 있게 개수 제한
    global player ,array
    s = 0
    if player == 'P1':
        for i in range(0, 3):
            for j in range(0, 3):
                if array[which_piece][i][j] == 1:
                    s += 1
    else:
        for i in range(0, 3):
            for j in range(0, 3):
                if array[which_piece][i][j] == -1:
                    s += 1
    if s < 2:  # 두개 놓여있으면 False 리턴
        return True
    else:
        return False


# 말의 이미지 불러오기(추가)
def init_game_window():
    screen.fill((255, 255, 0), (0, 0, width, 100))
    screen.fill((255, 255, 0), (0, 400, width, 500))  # 조각선택란 색상 임의 변경

    # 세로줄 그리기.. pygame.draw.line(화면, 색, 시작위치, 끝위치, 굵기)
    pygame.draw.line(screen, line_color, (width / 3, 0), (width / 3, height - (height / 6)), 5)  # 화면, 색, 시작위치, 끝위치, 굵기
    pygame.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height - (height / 6)), 5)

    # 가로줄 그리기
    pygame.draw.line(screen, line_color, (0, 0), (width, 0), 5)
    pygame.draw.line(screen, line_color, (0, height / 6), (width, height / 6), 5)
    pygame.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 5)
    pygame.draw.line(screen, line_color, (0, height / 2), (width, height / 2), 5)
    pygame.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 5)
    pygame.draw.line(screen, line_color, (0, height / 6 * 5), (width, height / 6 * 5), 5)

    # 말을 두개씩 객체 생성
    screen.blit(p2_small_piece_img, (40, 40))
    screen.blit(p2_small_piece_img, (70, 40))
    screen.blit(p2_medium_piece_img, (155, 30))
    screen.blit(p2_medium_piece_img, (205, 30))
    screen.blit(p2_large_piece_img, (275, 20))
    screen.blit(p2_large_piece_img, (335, 20))

    # 말을 두개씩
    screen.blit(p1_small_piece_img, (40, 40 + 400))
    screen.blit(p1_small_piece_img, (70, 40 + 400))
    screen.blit(p1_medium_piece_img, (155, 30 + 400))
    screen.blit(p1_medium_piece_img, (205, 30 + 400))
    screen.blit(p1_large_piece_img, (275, 20 + 400))
    screen.blit(p1_large_piece_img, (335, 20 + 400))

    draw_status()


# 맨 밑의 상태정보 표시
def draw_status():
    global draw

    if winner is None:
        message = player.upper() + "'s Turn"
    else:
        message = winner.upper() + " won !"
    if draw:
        message = "Game Draw !"

    # 폰트 설정
    font = pygame.font.Font(None, 50)
    # 텍스트의 너비 및 색
    text = font.render(message, 1, (255, 255, 255))

    # 메세지를 복사
    # 메인 디스플레이 하단에 작은 블록 생성
    screen.fill((0, 0, 0), (0, height - 100, width, height))
    text_rect = text.get_rect(center=(width / 2, 600 - 50))
    screen.blit(text, text_rect)
    pygame.display.update()


def copy_real_to_vision(arr):
    board_r = arr.reshape(27)
    board_v = np.zeros(9)
    for i in range(3):
        for j in range(3):
            if board_r[3 * i + j + 18] == 1:
                board_v[3 * i + j] = 1
            elif board_r[3 * i + j + 18] == -1:
                board_v[3 * i + j] = -1
            elif board_r[3 * i + j + 9] == 1:
                board_v[3 * i + j] = 1
            elif board_r[3 * i + j + 9] == -1:
                board_v[3 * i + j] = -1
            elif board_r[3 * i + j] == 1:
                board_v[3 * i + j] = 1
            elif board_r[3 * i + j] == -1:
                board_v[3 * i + j] = -1
    return board_v


# 게임이 종료됐는지 판단
def end_check():
    global array, winner, draw
    print(array)  # 높이 열 행 배열(?)
    board_v = copy_real_to_vision(array)
    # 0 1 2
    # 3 4 5
    # 6 7 8
    # 승패 조건은 가로, 세로, 대각선이 -1이나 1로 동일할 때
    # 승패 조건 생성
    end_condition = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

    # 이긴사람의 수 카운트 -> 두명 다 라인을 완성할 경우 비기므로
    p1_cnt = 0
    p2_cnt = 0
    # 승리 판별
    for line in end_condition:
        if board_v[line[0]] == board_v[line[1]] and \
                board_v[line[1]] == board_v[line[2]] and \
                board_v[line[0]] == 1:  # 플레이어1 이 이겼다면
            # 종료됐다면 누가 이겼는지 표시
            winner = 'P1'
            p1_cnt += 1
        if board_v[line[0]] == board_v[line[1]] and \
                board_v[line[1]] == board_v[line[2]] and \
                board_v[line[0]] == -1:  # 플레이어2 이 이겼다면
            # 종료됐다면 누가 이겼는지 표시
            winner = 'P2'
            p2_cnt += 1

    # 비긴 상태. 양쪽 모두 승리 조건을 동시에 만족하는 경우.
    if p1_cnt >= 1 and p2_cnt >= 1:
        draw = True
    draw_status()


def draw_empty(row, col):  # 지우기 대신 흰색 덮어 씌우기
    if row != 4:
        if row == 0:
            posx = height * 3 / 12
        if row == 1:
            posx = height * 5 / 12
        if row == 2:
            posx = height * 7 / 12

        if col == 0:
            posy = width / 6
        if col == 1:
            posy = width / 2
        if col == 2:
            posy = width / 6 * 5
    screen.blit(empty_img, (posy - 30, posx - 30))
    pygame.display.update()


# 해당하는 위치에 아이콘 그리기
def drawIcon(row, col, which_icon):
    print("drawIcon")
    global player, choice, ch
    # print(row, col)
    if row != 4:
        if row == 0:
            posx = height * 3 / 12
        if row == 1:
            posx = height * 5 / 12
        if row == 2:
            posx = height * 7 / 12

        if col == 0:
            posy = width / 6
        if col == 1:
            posy = width / 2
        if col == 2:
            posy = width / 6 * 5

        if player == 'P2':
            if which_icon == 0:
                screen.blit(p1_small_piece_img, (posy - 10, posx - 10))
            elif which_icon == 1:
                screen.blit(p1_medium_piece_img, (posy - 20, posx - 20))
            else:  # which_icon == 2
                screen.blit(p1_large_piece_img, (posy - 30, posx - 30))
            # if ch == 1:
            #     player = 'P1'

        else:
            if which_icon == 0:
                screen.blit(p2_small_piece_img, (posy - 10, posx - 10))
            elif which_icon == 1:
                screen.blit(p2_medium_piece_img, (posy - 20, posx - 20))
            else:  # which_icon == 2
                screen.blit(p2_large_piece_img, (posy - 30, posx - 30))
            # if ch == 1:
            #     player = 'P2'

    choice = False
    init_game_window()
    pygame.display.update()


# 사용자 마우스 클릭에서 말을 선택하는 입력을 얻기 위한 함수
def select_piece(x,y):
    print("select piece")
    global choice
    # 마우스 클릭 좌표
    if player == 'P1':
        if y > 100:  # 선택안하면 진행 X
            choice = False
            if y < (height * 4) / 6:
                change(x, y)
            else:
                return None
        elif 0 < x < (width / 3):
            screen.fill((45, 180, 0), (0, 0, width / 3, height / 6))
            choice = True
            return 0
        elif (width / 3) < x < (width * 2 / 3):
            screen.fill((45, 180, 0), (width / 3, 0, width / 3, height / 6))
            choice = True
            return 1
        elif x < width:
            screen.fill((45, 180, 0), (width / 3 * 2, 0, width / 3, height / 6))
            choice = True
            return 2

    elif player == 'P2':
        if (((height * 4) / 6) > y) or (y > ((height * 5) / 6)):
            choice = False
            if (y < (height * 4) / 6) and (y > 100):
                change(x, y)
            else:
                return None
        elif 0 < x < (width / 3):
            screen.fill((45, 180, 0), (0, ((height * 4) / 6), width / 3, height / 6))
            choice = True
            return 0
        elif (width / 3) < x < (width * 2 / 3):
            screen.fill((45, 180, 0), (width / 3, ((height * 4) / 6), width / 3, height / 6))
            choice = True
            return 1
        elif x < width:
            screen.fill((45, 180, 0), (width / 3 * 2, ((height * 4) / 6), width / 3, height / 6))
            choice = True
            return 2

    pygame.display.update()
    # 해당 좌표에 해당하는 말의 크기를 반환, 이후 객체 사라져야함.


# 사용자 마우스 클릭에서 입력을 얻기 위해 설계한 함수
def user_click(x, y, which_piece):
    print("user click")
    global choice, array, turn_end

    col = None
    row = None
    # 마우스 클릭의 열을 저장
    if x < width / 3:
        col = 0
    elif x < width / 3 * 2:
        col = 1
    elif x < width:
        col = 2

    # 마우스 클릭의 행을 저장
    if height / 3 > y > height / 6:
        row = 0
    elif height / 2 > y > height / 3:
        row = 1
    elif height / 3 * 2 > y > height / 2:
        row = 2

    if (col == None) or (row == None):
        return
    # 만약 얻은 행, 열에 말을 놓을 수 있다면 말을 놓는다!

    if array[which_piece][row][col] == 0:  # 놓을 자리가 비어있는지 여부
        if which_piece == 0:  # 작은것 놓으려할때
            if (array[1][row][col] == 0) and (array[2][row][col] == 0):
                if limit_2(which_piece):
                    if player == 'P1':
                        array[which_piece][row][col] = 1
                    else:
                        array[which_piece][row][col] = -1
                    drawIcon(row, col, which_piece)
                    turn_end = True
                else:
                    choice = False
                    init_game_window()
            else:
                choice = False
                init_game_window()
        elif which_piece == 1:  # 중간것 놓으려 할때
            if array[2][row][col] == 0:
                if limit_2(which_piece):
                    if player == 'P1':
                        array[which_piece][row][col] = 1
                    else:
                        array[which_piece][row][col] = -1
                    drawIcon(row, col, which_piece)
                    turn_end = True
                else:
                    choice = False
                    init_game_window()
            else:
                choice = False
                init_game_window()
        else:  # 큰거 놓으려 할때
            if limit_2(which_piece):
                if player == 'P1':
                    array[which_piece][row][col] = 1
                else:
                    array[which_piece][row][col] = -1
                drawIcon(row, col, which_piece)
                turn_end = True
            else:
                choice = False
                init_game_window()
    else:
        choice = False
        init_game_window()
    # if ...
    end_check()


def change(x, y):  # 옮기기
    print("change")
    global col_1, row_1, array
    global biggest, ch, player

    # 마우스 클릭의 열을 저장
    if x < width / 3:
        col_1 = 0
    elif x < width / 3 * 2:
        col_1 = 1
    elif x < width:
        col_1 = 2

    # 마우스 클릭의 행을 저장
    if height / 3 > y > height / 6:
        row_1 = 0
    elif height / 2 > y > height / 3:
        row_1 = 1
    elif height / 3 * 2 > y > height / 2:
        row_1 = 2

    for i in range(0, 3):
        if array[2 - i][row_1][col_1] != 0:
            biggest = 2 - i
            break
    if player == 'P1':
        if array[biggest][row_1][col_1] == -1:
            print("리턴함P1인데 p2건드림")
            return None
    else:
        if array[biggest][row_1][col_1] == 1:
            print("리턴함P2인데 p1건드림")
            return None
    if biggest == -1:  # 옮길것 없을때
        return None

    # print(biggest)
    ch = 1
    end_check()


def change2(x, y):
    print("change2")
    global biggest, col_1, row_1
    global array, ch
    global player, turn_end

    col_2 = None
    row_2 = None
    if x < width / 3:
        col_2 = 0
    elif x < width / 3 * 2:
        col_2 = 1
    elif x < width:
        col_2 = 2

    # 마우스 클릭의 행을 저장
    if height / 3 > y > height / 6:
        row_2 = 0
    elif height / 2 > y > height / 3:
        row_2 = 1
    elif height / 3 * 2 > y > height / 2:
        row_2 = 2

    if array[biggest][row_2][col_2] != 0:  # 옮길곳에 이미 같은 크기가 있을때
        ch = 0
        return None

    elif biggest == 0:
        if (array[1][row_2][col_2] != 0) or (array[2][row_2][col_2] != 0):
            ch = 0
            return None
        else:
            drawIcon(row_2, col_2, biggest)
            turn_end = True
            if player == 'P1':
                array[biggest][row_2][col_2] = 1
            else:
                array[biggest][row_2][col_2] = -1
            array[biggest][row_1][col_1] = 0
            draw_empty(row_1, col_1)

    elif biggest == 1:
        if array[2][row_2][col_2] != 0:
            ch = 0
            return None
        else:
            drawIcon(row_2, col_2, biggest)
            turn_end = True
            if player == 'P1':
                array[biggest][row_2][col_2] = 1
            else:
                array[biggest][row_2][col_2] = -1

            if array[0][row_1][col_1] != 0:
                draw_empty(row_1, col_1)
                tmp = player
                array[biggest][row_1][col_1] = 0
                if array[0][row_1][col_1] == 1:#player 1
                    player = 'P1'
                    drawIcon(row_1,col_1,0)
                elif array[0][row_1][col_1] == -1:#player 2
                    player = 'P2'
                    drawIcon(row_1, col_1, 0)
                player = tmp
            else:
                draw_empty(row_1, col_1)
                array[biggest][row_1][col_1] = 0

    else:
        drawIcon(row_2, col_2, biggest)
        turn_end = True
        if player == 'P1':
            array[biggest][row_2][col_2] = 1
        else:
            array[biggest][row_2][col_2] = -1

        if array[1][row_1][col_1] != 0:
            draw_empty(row_1, col_1)
            array[biggest][row_1][col_1] = 0
            tmp = player
            if array[1][row_1][col_1] == 1:#player 1
                player = 'P1'
                drawIcon(row_1,col_1,1)
            elif array[1][row_1][col_1] == -1:#player 2
                player = 'P2'
                drawIcon(row_1, col_1, 1)
            player = tmp
        elif array[0][row_1][col_1] != 0:
            draw_empty(row_1, col_1)
            array[biggest][row_1][col_1] = 0
            tmp = player
            if array[0][row_1][col_1] == 1:#player 1
                player = 'P1'
                drawIcon(row_1,col_1,0)
            elif array[0][row_1][col_1] == -1:#player 2
                player = 'P2'
                drawIcon(row_1, col_1, 0)
            player = tmp
        else:
            draw_empty(row_1, col_1)
            array[biggest][row_1][col_1] = 0

    ch = 0
    end_check()


def reset_game():
    global array, winner, player, draw
    time.sleep(3)
    player = 'P1'
    draw = False
    winner = None
    new_game_window()
    array = np.arange(27).reshape(3, 3, 3)
    for i in range(0, 3):
        for j in range(0, 3):
            for k in range(0, 3):
                array[i][j][k] = 0


def new_game_window():
    screen.blit(initiating_window, (0, 0))
    pygame.display.update()
    time.sleep(2)
    screen.fill(white)
    init_game_window()


def Human_player():
    while True:
        for event in pygame.event.get():  # 이벤트를 가지고 와서
            # print(event)
            # 이벤트 타입이 만약 QUIT 이면(종료버튼 누르면)
            if event.type == QUIT:
                pygame.quit()  # 파이게임 종료
                sys.exit()  # 시스템 종료(윈도우 화면 종료)

            # 마우스 클릭하면
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 마우스 클릭 좌표
                x, y = pygame.mouse.get_pos()
                if not choice:
                    if ch == 0:
                        # 1. 놓을 말을 선택(선택했다면 그 말의 정보를 리턴할 것이고 그 리턴한 값을 user_click()에 인자로 넣음.)
                        which_piece = select_piece(x, y)  # which_piece = 어디를 클릭했는지에 따라 반환을 다르게 하는 함수
                    else:
                        change2(x, y)
                else:
                    # 2. 놓을 위치 선택
                    user_click(x, y, which_piece)  # 인자로 0, 1, 2(작은 말, 중간 말, 큰 말)
                # 3. 둘다 아니라면 무시

            if turn_end:
                return
        pygame.display.update()  # 지금까지 작성한 코드를 윈도우 창에 표시해주겠다는 업데이트(필수!)
        FPSCLOCK.tick(fps)  # 몇 프레임으로 해줄지 : 30프레임


def main():  # 메인함수
    new_game_window()  # 화면 초기화
    global player, turn_end  # player 1P:1p, 2P:2p

    while True:  # 화면을 계속 띄우기 위해
        if player == "P1":
            # 1플레이어 두는 곳.
            Human_player()
            turn_end = False
        else:  # turn == -1
            # 2플레이어 두는 곳.
            # 인공지능 플레이어 착수
            print("인공지능 플레이어")
            Human_player()
            turn_end = False

        if player == "P1":
            player = "P2"
        else:
            player = "P1"

        if winner or draw:
            reset_game()

        draw_status()
        pygame.display.update()  # 지금까지 작성한 코드를 윈도우 창에 표시해주겠다는 업데이트(필수!)
        FPSCLOCK.tick(fps)  # 몇 프레임으로 해줄지 : 30프레임


# 여기서 부터 시작!
if __name__ == '__main__':
    main()  # 메인함수 호출
