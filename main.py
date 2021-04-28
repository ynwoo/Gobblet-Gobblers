import sys  # sys 패키지 임포트
import pygame  # 파이게임 패키지 임포트
from pygame.locals import QUIT  # 파이게임의 기능 중 종료를 임포트

# 글로벌 변수 선언

# 플레이어 값을 저장 P1 or P2
player = 'P1'
# 승자의 값을 저장
winner = None
# 게임이 비겼는지 체크
draw = None

# game window창의 크기 값 설정
width = 400
height = 600

# 배경화면 색
white = (255, 255, 255)
# 선 색
line_color = (0, 0, 0)

# 말을 선택한 상태인지 표시
choice = False

#처음인지 여부
first = True

#게임 진행을 위한 이중배열
#player에 따라 1,2 비어있으면 0
#깊이가 종류를 표현
array = [[[0]*4]*4]*3

pygame.init()  # 파이게임 모듈을 초기화
fps = 30  # fps 설정
screen = pygame.display.set_mode((width, height))  # 만들 윈도우 창의 화면 크기 설정
FPSCLOCK = pygame.time.Clock()  # 설정할 프레임을 저장할 변수
pygame.display.set_caption("Gobblet Gobblers")  # 만든 윈도우창에 이름을 적는 코드

# 이미지 불러오기
p1_piece_img = pygame.image.load("p1_icon.png")
p2_piece_img = pygame.image.load("p2_icon.png")

# 이미지 스케일링
p1_large_piece_img = pygame.transform.scale(p1_piece_img, (60, 60))
p1_medium_piece_img = pygame.transform.scale(p1_piece_img, (40, 40))
p1_small_piece_img = pygame.transform.scale(p1_piece_img, (20, 20))

p2_large_piece_img = pygame.transform.scale(p2_piece_img, (60, 60))
p2_medium_piece_img = pygame.transform.scale(p2_piece_img, (40, 40))
p2_small_piece_img = pygame.transform.scale(p2_piece_img, (20, 20))


# 말의 이미지 불러오기(추가)
def init_game_window():
    global first
    if first is True:#처음이후 화면변화에는 채우기 제외
        screen.fill(white)  # 배경 색
        first = False

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


# 게임이 종료됐는지 판단
def end_check():
    draw_status()


# 해당하는 위치에 아이콘 그리기
def drawIcon(row, col, which_icon):
    global player
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
                screen.blit(p1_small_piece_img, (posy-10, posx-10))
            elif which_icon == 1:
                screen.blit(p1_medium_piece_img, (posy-20, posx-20))
            else:  # which_icon == 2
                screen.blit(p1_large_piece_img, (posy-30, posx-30))
            player = 'P1'
        else:
            if which_icon == 0:
                screen.blit(p2_small_piece_img, (posy-10, posx-10))
            elif which_icon == 1:
                screen.blit(p2_medium_piece_img, (posy-20, posx-20))
            else:  # which_icon == 2
                screen.blit(p2_large_piece_img, (posy-30, posx-30))
            player = 'P2'
    init_game_window()
    pygame.display.update()


# 사용자 마우스 클릭에서 말을 선택하는 입력을 얻기 위한 함수
def select_piece():
    global choice
    # 마우스 클릭 좌표
    x, y = pygame.mouse.get_pos()

    if player == 'P1':
        if y > 100:  # 선택안하면 진행 X
            choice = False
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
            screen.fill((45, 180, 0), (width / 3 * 2, ((height * 4) / 6), width / 3, height  / 6))
            choice = True
            return 2

    pygame.display.update()
    # 해당 좌표에 해당하는 말의 크기를 반환, 이후 객체 사라져야함.


# 사용자 마우스 클릭에서 입력을 얻기 위해 설계한 함수
def user_click(which_piece):
    global choice
    global array
    # 어떤 말인지, 크기에 대한 정보가 없으면
    if which_piece is None:
        return

    # 마우스 클릭 좌표
    x, y = pygame.mouse.get_pos()
    print(x, y)
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

    if (col == None) or (row == None) :
        return
    # 만약 얻은 행, 열에 말을 놓을 수 있다면 말을 놓는다!
    
    if array[col][row][which_piece] == 0:
        if which_piece == 0:
            if (array[col][row][1]==0) and (array[col][row][2]==0):
                if player=='p1':
                    array[col][row][which_piece]=1
                else:
                    array[col][row][which_piece]=2
                drawIcon(row,col,which_piece)
            else:
                choice = False
                init_game_window()                
        elif which_piece == 1:
            if array[col][row][2]==0: 
                if player=='p1':
                    array[col][row][which_piece]=1
                else:
                    array[col][row][which_piece]=2
                drawIcon(row,col,which_piece)
            else:
                choice = False
                init_game_window()
        else:
            if player=='p1':
                array[col][row][which_piece]=1
            else:
                array[col][row][which_piece]=2
            drawIcon(row,col,which_piece)
    else:
        choice = False
        init_game_window()

    # if ...
    
    end_check()




def main():  # 메인함수
    init_game_window()  # 화면 초기화

    # p1 = Human_player()  # 플레이어 설정
    # p2 = Human_player()

    # 지정된 게임 수를 자동으로 두게 할 것인지 한 게임씩 두게 할 것인지 결정
    # auto = True: 지정된 판 수(games)를 자동으로 진행
    # auto = False: 한 게임씩 진행

    auto = False

    # auto 모드의 게임 수
    games = 100
    # print("p1 player : {}".format(p1.name))
    # print("p2 player : {}".format(p2.name))

    # 각 플레이어의 승리 횟수를 저장
    p1_score = 0
    p2_score = 0
    draw_score = 0

    while True:  # 화면을 계속 띄우기 위해
        for event in pygame.event.get():  # 이벤트를 가지고 와서
            # print(event.type)
            # 이벤트 타입이 만약 QUIT 이면(종료버튼 누르면)
            if event.type == QUIT:
                pygame.quit()  # 파이게임 종료
                sys.exit()  # 시스템 종료(윈도우 화면 종료)

            # 마우스 클릭하면
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not choice:
                    # 1. 놓을 말을 선택(선택했다면 그 말의 정보를 리턴할 것이고 그 리턴한 값을 user_click()에 인자로 넣음.)
                    which_piece = select_piece()  # which_piece = 어디를 클릭했는지에 따라 반환을 다르게 하는 함수
                    print(which_piece)
                else:
                    # 2. 놓을 위치 선택
                    user_click(which_piece)  # 인자로 0, 1, 2(작은 말, 중간 말, 큰 말)
                # 3. 둘다 아니라면 무시

        pygame.display.update()  # 지금까지 작성한 코드를 윈도우 창에 표시해주겠다는 업데이트(필수!)
        FPSCLOCK.tick(fps)  # 몇 프레임으로 해줄지 : 30프레임


# 여기서 부터 시작!
if __name__ == '__main__':
    main()  # 메인함수 호출
