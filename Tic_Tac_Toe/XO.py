import tkinter as tk        # دي المكتبة الي هنعمل منها ال GUI

player = 'X'
ai = 'O'
                        # هنا انا بعرف اللاعب و ال AI
player_wins = 0
ai_wins = 0
                        # هنا انا بدي قيمة للنتيجة بتاعت اللاعب و ال Ai
window = tk.Tk()        # هنا عملت ويندو 
window.title("TIC-TAC-TOE")     # اديتها عنوان
window.geometry("450x688")      # اديتها ابعاد 

board = [[' ' for _ in range(3)] for _ in range(3)] 
# هنا عملت ماتريكس 3*3  دي هتبقي بتاعت البورد 
buttons = [[None for _ in range(3)] for _ in range(3)]
# هنا عملت ماتريكس 3*3  دي هتبقي بتاعت الزراير الي علي البورد 

def check_winner(board, symbol):
    win_conditions = [
        [(0, 0), (0, 1), (0, 2)], 
        [(1, 0), (1, 1), (1, 2)],  
        [(2, 0), (2, 1), (2, 2)],  
        [(0, 0), (1, 0), (2, 0)],  
        [(0, 1), (1, 1), (2, 1)],  
        [(0, 2), (1, 2), (2, 2)], 
        [(0, 0), (1, 1), (2, 2)],  
        [(0, 2), (1, 1), (2, 0)]   
    ]
    # دي كل احتمالت الي ممكن انا اكسب فيها
    for condition in win_conditions:
        if all(board[r][c] == symbol for r, c in condition):
            return True
    return False

def is_draw(board): # دي عشان تشوف التعادل 
    return all(cell != ' ' for row in board for cell in row)

def get_empty_cells(board):# بترجع قايمة بكل الأماكن الفاضية في اللوحة الي ممكن نحط فيها الرمز
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']

def minimax(board, depth, is_maximizing): # الدالة الي بيشتغل فيها الالجوريزم
    if check_winner(board, ai):
        return 1
    if check_winner(board, player):
        return -1
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -float('inf') # بنخلي القيمة سالب انفنتي
        for r, c in get_empty_cells(board): # هنا بنلف ع البورد و هي فاضية 
            board[r][c] = ai # بنحط الرمز بتاع ال AI
            score = minimax(board, depth + 1, False) # بنعمل ريكرجن للفانكشن بس المرادي هنزود العمق عشان نغير اللعب و نقلل النتيجة
            board[r][c] = ' '
            best_score = max(score, best_score) # بنشوف النتيجة المحسوبة اكبر ولا لا او بمعني اصح بتختار اكبر قيمة
        return best_score
    else:
        best_score = float('inf') # بنخلي القيمة موجب انفنتي
        for r, c in get_empty_cells(board): # هنا بنلف ع البورد و هي فاضية 
            board[r][c] = player    # بنحط الرمز بتاع اللاعب
            score = minimax(board, depth + 1, True) # بنعمل ريكرجن للفانكشن بس المرادي هنزود العمق عشان نغير اللعب و نخلي اللعب الي هيعلي النتيجة يلعب
            board[r][c] = ' '
            best_score = min(score, best_score) # بنشوف النتيجة المحسوبة اقل ولا لا او بمعني اصح بتختار اقل قيمة
        return best_score

def ai_move():
    best_score = -float('inf')
    best_move = None  # بدي ليها قيمة ابتدائية هخزن فيها احسن حركة ل AI
    for r, c in get_empty_cells(board):
        board[r][c] = ai    #الذكاء الاصطناعي بيحط الرمز بتاعه 
        score = minimax(board, 0, False)
        board[r][c] = ' '
        if score > best_score:
            best_score = score
            best_move = (r, c)
    
    if best_move:  
        #بعد ما تخلص اللوب، لو لقينا حركة أفضل (لو كانت best_move ليست None)، هننفذ الجركة
        r, c = best_move
        board[r][c] = ai
        update_button(r, c, ai)

def update_button(row, col, symbol): # دي بتخلي اللعبة الي لعبتها انا او الذكاء تظهر ع البوردة او الزرار 
    buttons[row][col].config(text=symbol, state=tk.DISABLED)

def player_move(row, col):
    if board[row][col] == ' ':
        board[row][col] = player
        update_button(row, col, player)
        # هما الخلاصة لو كان في مكان فاضي ممكن اللاعب يلعب في المكان ده و ينحدث عشان يظهر ع الشاشة
        
        if check_winner(board, player): # بنشوف لو اللعب كسب
            result_label.config(text="You Win") # ده ليبول ليظهر لو انا كسب 
            update_counters(player) # دي فانطشن بتحسب عدد المرات الي كسبت فيها او الذكاء الي كسب فيها
            disable_all_buttons()
            return
        
        if is_draw(board):
            result_label.config(text="DRAW")
            disable_all_buttons()
            return
        
        ai_move()
        
        if check_winner(board, ai):
            result_label.config(text="You Lose")
            update_counters(ai)
            disable_all_buttons()
            return
        
        if is_draw(board):
            result_label.config(text="DRAW")
            disable_all_buttons()


def disable_all_buttons(): # بوقف الزراير بعد ما تخلص اللعبة
    for row in buttons:
        for button in row:
            button.config(state=tk.DISABLED)


def reset_game(): # دي فانكشن معموولة عشان ترستر اللعبة
    global board   # هنا بعرف ان البورد دي ممتغير بستعمله في كل الفانكشنز الي عندي 
    board = [[' ' for _ in range(3)] for _ in range(3)]  
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text=' ', state=tk.NORMAL) # المهم هنا انو بيبقي جاخز انك تشتغل علية عادي
    result_label.config(text="")


def update_counters(winner): # دي لو الي هيكسب يزداد واحد
    global player_wins, ai_wins
    if winner == player:
        player_wins += 1
    elif winner == ai:
        ai_wins += 1
    update_counters_label()


def update_counters_label(): # بيظهرلك النتايج
    counters_label.config(text=f"X Wins: {player_wins} | O Wins: {ai_wins}")


for r in range(3):
    for c in range(3):
        button = tk.Button(window, text=' ', font=('Helvetica', 24), width=6, height=3,
                           command=lambda r=r, c=c: player_move(r, c))
        button.grid(row=r, column=c, padx=10, pady=10)
        buttons[r][c] = button
        # هنا بنظبط حجم و شكل الزراير


result_label = tk.Label(window, text="", font=('Helvetica', 18))
result_label.grid(row=3, column=0, columnspan=3, pady=20)
# وهننا الليبول حجمه و خطة 

restart_button = tk.Button(window, text="Restart", font=('Helvetica', 18), command=reset_game)
restart_button.grid(row=5, column=0, columnspan=3, pady=20)
# و ده زرار ال restart

counters_label = tk.Label(window, text=f"X Wins: {player_wins} | O Wins: {ai_wins}", font=('Helvetica', 16))
counters_label.grid(row=4, column=0, columnspan=3)


window.mainloop()
# دي بقي الي بتشغل ال GUI 