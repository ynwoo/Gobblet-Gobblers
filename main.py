import sys  # sys 패키지 임포트
import time
import pygame  # 파이게임 패키지 임포트
import numpy as np
from pygame.locals import QUIT  # 파이게임의 기능 중 종료를 임포트
from tqdm import tqdm
sys.setrecursionlimit(5000)
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


def limit_2(arr, c_player, which_piece):  # 두개씩만 놓을 수 있게 개수 제한
    s = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if arr[which_piece][i][j] == c_player:
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
def end_check(arr):
    ec_winner = None
    ec_draw = False

    board_v = copy_real_to_vision(arr)
    # print("board_v : {}".format(board_v))
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
            ec_winner = 'P1'
            p1_cnt += 1
        if board_v[line[0]] == board_v[line[1]] and \
                board_v[line[1]] == board_v[line[2]] and \
                board_v[line[0]] == -1:  # 플레이어2 이 이겼다면
            # 종료됐다면 누가 이겼는지 표시
            ec_winner = 'P2'
            p2_cnt += 1

    # 비긴 상태. 양쪽 모두 승리 조건을 동시에 만족하는 경우.
    if p1_cnt >= 1 and p2_cnt >= 1:
        ec_draw = True
    # draw_status()
    return ec_winner, ec_draw


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
    global winner, draw
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
    if player == "P1":
        c_player = 1
    else:
        c_player = -1
    if array[which_piece][row][col] == 0:  # 놓을 자리가 비어있는지 여부
        if which_piece == 0:  # 작은것 놓으려할때
            if (array[1][row][col] == 0) and (array[2][row][col] == 0):
                if limit_2(array, c_player, which_piece):
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
                if limit_2(array, c_player, which_piece):
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
            if limit_2(array, c_player, which_piece):
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
    winner, draw = end_check(array)


def change(x, y):  # 옮기기
    print("change")
    global col_1, row_1, array
    global biggest, ch, player
    global winner, draw
    # 마우스 클릭의 열을 저장
    biggest = -1
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

    print(biggest)
    ch = 1
    winner, draw = end_check(array)


def change2(x, y):
    print("change2")
    global biggest, col_1, row_1
    global array, ch
    global player, turn_end
    global winner, draw
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
    biggest = -1
    ch = 0
    winner, draw = end_check(array)


def reset_game():
    global array, winner, player, draw
    global biggest
    biggest = -1
    time.sleep(3)
    player = 'P1'
    draw = False
    winner = None
    new_game_window()
    for i in range(0, 3):
        for j in range(0, 3):
            for k in range(0, 3):
                array[i][j][k] = 0


def new_game_window():
    screen.blit(initiating_window, (0, 0))
    pygame.display.update()
    time.sleep(1)
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
                print(choice)
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


def Random_player():
    global turn_end, player, array
    global winner, draw
    c_player = 0
    if player == "P1":
        c_player = 1
    else:
        c_player = -1

    # 가능한 행동 조사
    available_action = get_action(c_player, array)
    print("available_action : {}".format(available_action))
    # 가능한 행동 중 하나를 무작위로 선택
    action = np.random.randint(len(available_action))
    action = available_action[action]
    print("action : {}".format(action))
    # 그 행동에 따라 착수
    set_action(action, array)
    turn_end = True
    winner, draw = end_check(array)


def Monte_Carlo_player():
    global turn_end, player, array
    global winner, draw
    c_player = 0
    if player == "P1":
        c_player = 1
    else:
        c_player = -1
    num_playout = 300  # 10초안에 둘 수 있는 값이어야함.

    # 가능한 행동 조사
    available_action = get_action(c_player, array)
    # 상태가치를 저장할 배열 V
    V = np.zeros(len(available_action))

    # 가능한 행동들을 돌면서 V[i]+=1을 해줌
    for i in range(len(available_action)):
        # 플레이 아웃을 300번 반복
        for j in range(num_playout):
            # 지금 상태를 복사해서 플레이 아웃에 사용
            temp_array = array.copy()
            # play out 의 결과는 승리플레이어의 값으로 반환
            # p1이 이기면 1, p2가 이기면 -1
            reward = playout(temp_array, available_action[i], c_player)
            # print("reward : {}".format(reward))
            if player == reward:
                V[i] += 1
    v_table = {name:value for name, value in zip(available_action, V)}
    print("V : {}".format(v_table))
    # 가장 승률이 높은 행동을 저장
    action = np.argmax(V)
    action = available_action[action]

    set_action(action, array)
    turn_end = True
    winner, draw = end_check(array)


def Q_player(action):
    global turn_end, array
    global winner, draw

    set_action(action, array)
    turn_end = True
    winner, draw = end_check(array)


def playout(temp_array, action, c_player):
    # 보드에 플레이어의 선택을 표시(만약 새로운 말을 놓는 거라면)
    if isinstance(action, int):
        which_piece = action // 9
        if which_piece == 0:
            action = action
        elif which_piece == 1:
            action = action - 9
        else:
            action = action - 18
        row = action // 3
        col = action % 3

        temp_array[which_piece][row][col] = c_player
    else:  # 문자라면 -> 움직이는 액션이다
        action = action.split('to')  # pos[0]가 지울 장소, pos[1]이 생길 장소
        before_place = int(action[0])
        after_place = int(action[1])

        if 0 <= before_place < 9:
            which_piece = 0
        elif 9 <= before_place < 18:
            which_piece = 1
        else:
            which_piece = 2

        if which_piece == 0:
            before_place = before_place
            after_place = after_place
        elif which_piece == 1:
            before_place = before_place - 9
            after_place = after_place - 9
        else:
            before_place = before_place - 18
            after_place = after_place - 18

        row_b = before_place // 3
        col_b = before_place % 3

        row_a = after_place // 3
        col_a = after_place % 3

        # 원래 있던 자리에 있는 말을 지운다
        temp_array[which_piece][row_b][col_b] = 0
        # 옮길 위채에 말을 둔다.
        temp_array[which_piece][row_a][col_a] = c_player
    # print("temp_arr : {}".format(temp_array))
    po_winner, po_draw = end_check(temp_array)
    if po_winner is not None or po_draw:  # 게임이 끝났으면
        # print("po_winner : {}, po_draw : {}".format(po_winner,po_draw))
        return po_winner
    else:
        # 플레이어 교체
        c_player = -c_player
        # 가능한 행동 조사
        available_action = get_action(c_player, temp_array)
        # print("2: {}".format(available_action))
        # 무작위로 행동을 선택
        action = np.random.randint(len(available_action))
        # print(action)
        reward = playout(temp_array, available_action[action], c_player)
        return reward


def set_action(action, arr):
    if isinstance(action, int):  # 숫자라면
        which_piece = action // 9
        if which_piece == 0:
            action = action
        elif which_piece == 1:
            action = action - 9
        else:
            action = action - 18
        row = action // 3
        col = action % 3

        if player == 'P1':
            arr[which_piece][row][col] = 1
        else:
            arr[which_piece][row][col] = -1
        drawIcon(row, col, which_piece)
    else:  # 문자라면 -> 움직이는 액션이다
        action = action.split('to')  # pos[0]가 지울 장소, pos[1]이 생길 장소
        before_place = int(action[0])
        after_place = int(action[1])

        if 0 <= before_place < 9:
            which_piece = 0
        elif 9 <= before_place < 18:
            which_piece = 1
        else:
            which_piece = 2

        if which_piece == 0:
            before_place = before_place
            after_place = after_place
        elif which_piece == 1:
            before_place = before_place - 9
            after_place = after_place - 9
        else:
            before_place = before_place - 18
            after_place = after_place - 18

        row_b = before_place // 3
        col_b = before_place % 3

        row_a = after_place // 3
        col_a = after_place % 3

        # 원래 있던 자리에 있는 말을 지운다
        arr[which_piece][row_b][col_b] = 0
        # 옮길 위채에 말을 둔다.
        if player == 'P1':
            arr[which_piece][row_a][col_a] = 1
        else:
            arr[which_piece][row_a][col_a] = -1
        array_to_display()  # 화면 새로고침


def get_action(c_player, arr):
    observation = []
    board_r = arr.reshape(27)
    # print(board_r)
    if limit_2(arr, c_player, 2):  # 큰 말을 놓을 수 있으면
        for i in range(18, 27):
            if board_r[i] == 0:
                observation.append(i)
    if limit_2(arr, c_player, 1):  # 작은 말을 놓을 수 있으면
        for i in range(9, 18):
            if board_r[i] == 0:
                observation.append(i)
    if limit_2(arr, c_player, 0):
        for i in range(9):
            if board_r[i] == 0:
                observation.append(i)

    #  중간말이 놓인 위치에는 작은 말을 놓을 수 없다.(제거 작업)
    for i in range(9, 18):
        if board_r[i] != 0 and board_r[i - 9] == 0:
            if i - 9 in observation:
                observation.remove(i - 9)
    for i in range(18, 27):
        # 큰 말이 놓인 위치에는 중간말과 작은 말을 놓을 수 없다.
        if board_r[i] != 0 and board_r[i - 9] == 0:
            if i - 9 in observation:
                observation.remove(i - 9)
        if board_r[i] != 0 and board_r[i - 18] == 0:
            if i - 18 in observation:
                observation.remove(i - 18)
    observation.sort()  # 정렬
    # 이동 가능한 경우의 수 추가
    for i in range(9):
        if board_r[i] == c_player and board_r[i + 9] == 0 and board_r[i + 18] == 0:
            for j in range(9):
                if board_r[j] == 0 and board_r[j + 9] == 0 and board_r[j + 18] == 0:
                    observation.append(str(i) + 'to' + str(j))
    for i in range(9, 18):
        if board_r[i] == c_player and board_r[i + 9] == 0:
            for j in range(9, 18):
                if board_r[j] == 0 and board_r[j + 9] == 0:
                    observation.append(str(i) + 'to' + str(j))
    for i in range(18, 27):
        if board_r[i] == c_player:
            # 옮길 수 있는 위치 탐색
            for j in range(18, 27):
                # 빈 공간이면
                if board_r[j] == 0:
                    observation.append(str(i) + 'to' + str(j))

    return observation


def array_to_display():
    global array

    for i in range(3):
        for j in range(3):
            draw_empty(i, j)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if array[i][j][k] == 1:
                    if j == 0:
                        posx = height * 3 / 12
                    if j == 1:
                        posx = height * 5 / 12
                    if j == 2:
                        posx = height * 7 / 12

                    if k == 0:
                        posy = width / 6
                    if k == 1:
                        posy = width / 2
                    if k == 2:
                        posy = width / 6 * 5

                    if i == 0:
                        screen.blit(p2_small_piece_img, (posy - 10, posx - 10))
                    elif i == 1:
                        screen.blit(p2_medium_piece_img, (posy - 20, posx - 20))
                    else:  # which_icon == 2
                        screen.blit(p2_large_piece_img, (posy - 30, posx - 30))

                elif array[i][j][k] == -1:
                    if j == 0:
                        posx = height * 3 / 12
                    if j == 1:
                        posx = height * 5 / 12
                    if j == 2:
                        posx = height * 7 / 12

                    if k == 0:
                        posy = width / 6
                    if k == 1:
                        posy = width / 2
                    if k == 2:
                        posy = width / 6 * 5

                    if i == 0:
                        screen.blit(p1_small_piece_img, (posy - 10, posx - 10))
                    elif i == 1:
                        screen.blit(p1_medium_piece_img, (posy - 20, posx - 20))
                    else:  # which_icon == 2
                        screen.blit(p1_large_piece_img, (posy - 30, posx - 30))

    init_game_window()
    pygame.display.update()


class Q_learning_player:
    def __init__(self):
        self.name = "Q_player"
        # Q-table을 딕셔너리로 정의
        self.qtable = {}
        # e-greedy 계수 정의
        self.epsilon = 1
        # 학습률 정의
        self.learning_rate = 0.1
        self.gamma = 0.9
        self.print = False

    # policy 에 따라 상태에 맞는 행동을 선택
    def select_action(self, arr, c_player):
        #         print("Q_learning_player select action")
        # policy 에 따라 행동을 선택
        action = self.policy(arr, c_player)
        return action

    def policy(self, arr, c_player):
        board_r = arr.reshape(27)
        # 해당 state 저장
        tmp_board = np.zeros(27)
        if np.array_equal(tmp_board, board_r):
            key = (tuple(board_r), 22)
            self.qtable[key] = 0
            return 22

        for i in range(0,9) :
            tmp_board = np.zeros(27)
            tmp_board[i] = -1
            tmp_board[22] = 1
            if np.array_equal(tmp_board, board_r):
                key = (tuple(board_r), 18+i)
                self.qtable[key] = 0
                return 18+i

        for i in range(9,18) :
            tmp_board = np.zeros(27)
            tmp_board[i] = -1
            tmp_board[22] = 1
            if np.array_equal(tmp_board, board_r):
                key = (tuple(board_r), 9+i)
                self.qtable[key] = 0
                return 9+i

        tmp_board = np.zeros(27)
        tmp_board[22] = 1
        tmp_board[18] = -1
        if np.array_equal(tmp_board, board_r):
            key = (tuple(board_r), 19)
            self.qtable[key] = 0
            return 19

        tmp_board = np.zeros(27)
        tmp_board[22] = 1
        tmp_board[19] = -1
        if np.array_equal(tmp_board, board_r):
            key = (tuple(board_r), 20)
            self.qtable[key] = 0
            return 20

        tmp_board = np.zeros(27)
        tmp_board[22] = 1
        tmp_board[20] = -1
        if np.array_equal(tmp_board, board_r):
            key = (tuple(board_r), 19)
            self.qtable[key] = 0
            return 19

        tmp_board = np.zeros(27)
        tmp_board[22] = 1
        tmp_board[21] = -1
        if np.array_equal(tmp_board, board_r):
            key = (tuple(board_r), 18)
            self.qtable[key] = 0
            return 18

        tmp_board = np.zeros(27)
        tmp_board[22] = 1
        tmp_board[23] = -1
        if np.array_equal(tmp_board, board_r):
            key = (tuple(board_r), 20)
            self.qtable[key] = 0
            return 20

        tmp_board = np.zeros(27)
        tmp_board[22] = 1
        tmp_board[24] = -1
        if np.array_equal(tmp_board, board_r):
            key = (tuple(board_r), 25)
            self.qtable[key] = 0
            return 25

        tmp_board = np.zeros(27)
        tmp_board[22] = 1
        tmp_board[25] = -1
        if np.array_equal(tmp_board, board_r):
            key = (tuple(board_r), 24)
            self.qtable[key] = 0
            return 24

        tmp_board = np.zeros(27)
        tmp_board[22] = 1
        tmp_board[26] = -1
        if np.array_equal(tmp_board, board_r):
            key = (tuple(board_r), 25)
            self.qtable[key] = 0
            return 25    
        
        
        else:
            # 행동 가능한 상태를 저장
            available_action = get_action(c_player, arr)
            # 행동 가능한 상태의 Q-value를 저장
            qvalues = np.zeros(len(available_action))
            board_r = arr.reshape(27)
            # 행동 가능한 상태의 Q-value를 조사
            for i, act in enumerate(available_action):
                key = (tuple(board_r), act)

                # 현재 상태를 경험한 적이 없다면(딕셔너리에 없다면) 딕셔너리에 추가(Q-value = 0)
                if self.qtable.get(key) == None:
                    self.qtable[key] = 0
                # 행동 가능한 상태의 Q-value 저장
                qvalues[i] = self.qtable.get(key)

            # e-greedy
            # 가능한 행동들 중에서 Q-value 가 가장 큰 행동을 저장
            greedy_action = np.argmax(qvalues)

            # max Q-value와 같은 값이 여러개 있는지 확인한 후 double_check에 상태를 저장
            double_check = (np.where(qvalues == np.max(qvalues), 1, 0))

            # 여러개 있다면 중복된 상태중에서 다시 무작위로 선택
            if np.sum(double_check) > 1:
                double_check = double_check / np.sum(double_check)
                greedy_action = np.random.choice(range(0, len(double_check)), p=double_check)

            # e-greedy 로 행동들의 선택 확률을 계산
            pr = np.zeros(len(available_action))

            for i in range(len(available_action)):
                if i == greedy_action:
                    pr[i] = 1 - self.epsilon
                else:
                    pr[i] = self.epsilon / (len(available_action) - 1)

            action = np.random.choice(range(0, len(available_action)), p=pr)
            return available_action[action]

    def learn_qtable(self, board_backup, action_backup, arr, c_reward, c_player):
        # 현재 상태와 행동을 키로 저장
        key = (board_backup, action_backup)

        winner, draw = end_check(arr)
        # Q-table 학습
        if winner is not None or draw:
            # 게임이 끝났을 경우 학습
            self.qtable[key] += self.learning_rate * (c_reward - self.qtable[key])
        else:
            # 게임이 진행중일 경우 학습
            # 다음 상태의 max Q 값 계산
            available_action = get_action(c_player, arr)

            qvalues = np.zeros(len(available_action))
            board_r = arr.reshape(27)
            for i, act in enumerate(available_action):
                next_key = (tuple(board_r), act)

                # 다음 상태를 경험한 적이 없다면(딕셔너리에 없다면) 딕셔너리에 추가(Q-value = 0)
                if self.qtable.get(next_key) == None:
                    self.qtable[next_key] = 0
                qvalues[i] = self.qtable.get(next_key)

            # maxQ 조사
            maxQ = np.max(qvalues)

            # 게임이 진행중일 때 학습
            self.qtable[key] += self.learning_rate * (c_reward + self.gamma * maxQ - self.qtable[key])


def main():  # 메인함수
    new_game_window()  # 화면 초기화
    global player, turn_end  # player 1P:1p, 2P:2p
    # Q-learning 플레이어 훈련
    p1_Qplayer = Q_learning_player()
    p2_Qplayer = Q_learning_player()

    # 입실론은 0.5로 설장
    p1_Qplayer.epsilon = 0.5
    p2_Qplayer.epsilon = 0.5

    p1_score = 0
    p2_score = 0
    draw_score = 0
    max_learn = 300000

    for j in tqdm(range(max_learn)):
        np.random.seed(j)
        temp_array = np.arange(27).reshape(3, 3, 3)
        for i in range(0, 3):
            for j in range(0, 3):
                for k in range(0, 3):
                    temp_array[i][j][k] = 0

        for i in range(10000):
            # p1 행동 선택
            c_player = 1
            pos = p1_Qplayer.policy(temp_array, c_player)

            # 현재 상태 s, 행동 a를 저장
            board_r = temp_array.reshape(27)
            p1_board_backup = tuple(board_r)
            p1_action_backup = pos

            if isinstance(pos, int):  # 숫자라면
                board_r[pos] = c_player
            else:  # 문자라면 -> 움직이는 액션이다
                pos = pos.split('to')  # pos[0]가 지울 장소, pos[1]이 생길 장소
                board_r[int(pos[0])] = 0
                board_r[int(pos[1])] = c_player
            temp_array = board_r.reshape(3, 3, 3)
            w, d = end_check(temp_array)

            # 게임이 종료상태라면 각 플레이어의 Q-table을 학습
            if w is not None or d:
                # 비겼으면 보수 0
                if d:
                    p1_Qplayer.learn_qtable(p1_board_backup, p1_action_backup, temp_array, 0, player)
                    p2_Qplayer.learn_qtable(p2_board_backup, p2_action_backup, temp_array, 0, player)
                    draw_score += 1
                    break
                elif w == "P2":  # p1이 두었는데 p2가 이기는 경우
                    p1_Qplayer.learn_qtable(p1_board_backup, p1_action_backup, temp_array, -1, player)
                    p2_Qplayer.learn_qtable(p2_board_backup, p2_action_backup, temp_array, 1, player)
                    p2_score += 1
                    break
                # p1이 이겼으므로 보상 +1
                # p2이 졌으므로 보상 -1
                else:
                    p1_Qplayer.learn_qtable(p1_board_backup, p1_action_backup, temp_array, 1, player)
                    p2_Qplayer.learn_qtable(p2_board_backup, p2_action_backup, temp_array, -1, player)
                    p1_score += 1
                    break

            # 게임이 끝나지 않았다면 p2의 Q-table을 학습 (게임 시작직후에는 p2는 학습할 수 없음)
            if i != 0:
                p2_Qplayer.learn_qtable(p2_board_backup, p2_action_backup, temp_array, -0.01, player)

            # p2 행동 선택
            c_player = -1
            pos = p2_Qplayer.policy(temp_array, c_player)

            board_r = temp_array.reshape(27)
            p2_board_backup = tuple(board_r)
            p2_action_backup = pos

            if isinstance(pos, int):  # 숫자라면
                board_r[pos] = c_player
            else:  # 문자라면 -> 움직이는 액션이다
                pos = pos.split('to')  # pos[0]가 지울 장소, pos[1]이 생길 장소
                board_r[int(pos[0])] = 0
                board_r[int(pos[1])] = c_player

            temp_array = board_r.reshape(3, 3, 3)
            w, d = end_check(temp_array)

            if w is not None or d:
                # 비겼으면 보수 0
                if d:
                    p1_Qplayer.learn_qtable(p1_board_backup, p1_action_backup, temp_array, 0, player)
                    p2_Qplayer.learn_qtable(p2_board_backup, p2_action_backup, temp_array, 0, player)
                    draw_score += 1
                    break
                elif w == "P1":  # p2가 두었는데 p1이 이기는 경우
                    p1_Qplayer.learn_qtable(p1_board_backup, p1_action_backup, temp_array, 1, player)
                    p2_Qplayer.learn_qtable(p2_board_backup, p2_action_backup, temp_array, -1, player)
                    p1_score += 1
                    break
                # p2이 이겼으므로 보상 +1
                # p1이 졌으므로 보상 -1
                else:
                    p1_Qplayer.learn_qtable(p1_board_backup, p1_action_backup, temp_array, -1, player)
                    p2_Qplayer.learn_qtable(p2_board_backup, p2_action_backup, temp_array, 1, player)
                    p2_score += 1
                    break

            # 게임이 끝나지 않았다면 p1의 Q-table 학습
            p1_Qplayer.learn_qtable(p1_board_backup, p1_action_backup, temp_array, -0.01, player)
            # # 1000 게임마다 게임 결과 표시
    #         if j % 1000 == 0:
    #             print("j = {} p1 = {} p2 = {} draw = {}".format(j, p1_score, p2_score, draw_score))
    #             print("p1 len : {}".format(len(p1_Qplayer.qtable)))
    #             print("p2 len : {}".format(len(p2_Qplayer.qtable)))

    print("p1 = {} p2 = {} draw = {}".format(p1_score, p2_score, draw_score))
    print("end train")
    # 최적의 선택만 하도록
    p1_Qplayer.epsilon = 0
    p2_Qplayer.epsilon = 0
    while True:  # 화면을 계속 띄우기 위해
        if player == "P1":
            # 1플레이어 두는 곳.
            time.sleep(0.5)
            # Random_player()
            # Human_player()
            # Monte_Carlo_player()

            act = p1_Qplayer.select_action(array, 1)
            Q_player(act)
            turn_end = False
        else:
            # 2플레이어 두는 곳.
            time.sleep(0.5)
            # Random_player()
            # Monte_Carlo_player()
            # act = p2_Qplayer.select_action(array, -1)
            # Q_player(act)
            Human_player()
            turn_end = False

        if player == "P1":
            player = "P2"
        else:
            player = "P1"
        draw_status()

        if winner or draw:
            reset_game()

        pygame.display.update()  # 지금까지 작성한 코드를 윈도우 창에 표시해주겠다는 업데이트(필수!)
        FPSCLOCK.tick(fps)  # 몇 프레임으로 해줄지 : 30프레임


# 여기서 부터 시작!
if __name__ == '__main__':
    main()  # 메인함수 호출
