# test changes
import random

# исходная заготовка для изображения игрового поля
game_field = [["   0  1  2"], ["0", "_", "_", "_"], ["1", "_", "_", "_"], ["2", "_", "_", "_"]]
# [1][0]
# перечень координат всех клеток в виде списка, из которого мы убираем одну с каждым ходом
game_field_cells = ["00", "01", "02",
                    "10", "11", "12",
                    "20", "21", "22"]
# множество выигрышеых комбинаций координат клеток на поле
win_set = [{"00", "10", "20"}, # по горизонтали
           {"01", "11", "21"},
           {"02", "12", "22"},
           {"00", "01", "02"}, # по вертикали
           {"10", "11", "12"},
           {"20", "21", "22"},
           {"00", "11", "22"},  # по диагонали
           {"20", "11", "02"}]
# рабочее множество для х и для о
h_set = set({}) # human set
m_set = set({}) # machine set
# рабочие переменные (глобальные)
h_choice = ""  # Выбор игрока, х или о
m_choice = ""  # х или о
first_move = ""  # кто первый ходит, 1 - игрок, 0 - машина
playing = "y"  # Пока "у" играем
count_h = 0   # счетчики ходов, первые три хода поиск победителя не производится
count_m = 0
player = ""        # индикатор того, кто выиграл, h or m

def init_game():
    global playing
    global h_choice
    global m_choice
    global first_move

    # Печатаем игровое поле
    display_field()
    # Потом инструкции
    print("Вам предлагается популярная игра 'Крестики-нолмки'.")
    print("Правила игры Вам должны быть давным-давно известны.")
    response = input("Если нет, нажмите 'Нет' (N), если да - любую другую клавишу.")
    if response.lower() == "n":
        print()
        print("Пока!")
        playing = "n"
        return
    while True:
        print()
        h_choice = input("Выберите что у вас крестики 'x' или нолики 'o': (X/O)")
        h_choice = h_choice.lower()
        if h_choice == "x":
            m_choice = "o"
            break
        elif h_choice == "o":
            m_choice = "x"
            break
        else:
            print("Непонятно. Введите еще раз.")
    print(h_choice)
    print()
    print("При каждом ходе вводите координаты клеточки в виде двузначного числа, типа '12'.")
    print("Потом нажимайте 'Ввод'. Если хотите выйти из игры в любое время нажмите 'N'.")
    print()
    while True:
        first_move = input("Кто первый ходит? 1 - Вы. 0 - я.")
        if first_move == "1" or first_move == "0":
            break
        else:
            print("Непонятно. Введите еще раз.")

def display_field():
    # Поле игры:
    #     0  1  2
    #  0  _  _  _
    #  1  _  _  _
    #  2  _  _  _
    print()
    for i in game_field:
        row_cur = ""
        for j in i:
            row_cur = row_cur + j + "  "
        print(row_cur)

def update_field(xy, xo):
    game_field[int(xy[1]) + 1][int(xy[0]) + 1] = xo
    display_field()

def who_win(temp_xo):
    # temp_xo - это множество соординат игрока х или о, накопленных в ходе игры
    # Последовательно перебираем множества выигрышных комбинаций, находим пеересечение 2-х множеств.
    # Еслм есть полное совпадение - победа
    for i in win_set:
        if len((temp_xo.intersection(i))) == 3:
            print()
            print("Gotcha!")
            # есть победитель
            return 1
    else:
       # победитель не найден
       return 0

def end_of_game():
    global player

    print("Конец игры.")
    print()
    if playing == "n":
        print("Игра отменена")
        return

    if player == "h":
        print("Поздравляю, Вы выиграли! Возьмите с полки пирожок!")
    elif player == "m":
        print("Увы, на этот раз непруха. Но ничего, в следующий раз Вы все отыграете. Заходите еще.")
    else:
        print("Спортиная ничья.")

def available_cell(xy):
    if xy in game_field_cells:
        game_field_cells.remove(xy)
        return 1
    else:
        return 0

def human_move():
    global count_h
    global playing

    if not game_field_cells:      # список пустой?
        return 0
    while True:
        print()
        in_coord = input("Ваш ход:")
        if in_coord.lower() == "n":
            playing = "n"
            return 0 # Выходим из игры по желанию игрока
        if in_coord.isnumeric() and len(in_coord) == 2 and in_coord <= "22":
            if not available_cell(in_coord):
                print()
                print("Эта клетка занята. Попробуйте еще раз.")
                continue
            else:
                update_field(in_coord, h_choice)
                h_set.add(in_coord)
                count_h += 1
                if count_h >= 3:
                    return who_win(h_set) # проверка условий выигрыша 1/0
                break
        else:
            print("Непонятно. Введите еще раз.")

    return 0

def machine_move():
    global count_m

    if not game_field_cells:      # список пустой?
        return 0
    print()
    print("Мой ход:")
    # получить координату любой свободной ячейки из списка оставшихся
    xy = game_field_cells[int(random.random() * len(game_field_cells))]

    game_field_cells.remove(xy)
    update_field(xy, m_choice)
    m_set.add(xy)
    count_m += 1
    if count_m >= 3:
        return who_win(m_set)  # проверка условий выигрыша 1/0
    pass

    return 0

# ===========================================================

init_game()

# Основной цикл
while playing == "y" and len(game_field_cells) > 0:
    if first_move == "1":      # в зависимости от заданной очередности хода
        if playing == "n" or human_move():  # выигрыш или выход из игры
            player = "h"
            break
        if machine_move():  # выигрыш
            player = "m"
            break
    else:
        if machine_move():  # выигрыш
            player = "m"
            break
        if playing == "n" or human_move():       # выигрыш  или выход из игры
            player = "h"
            break

end_of_game()


