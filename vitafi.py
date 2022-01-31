import curses
import yfinance as yf
from datetime import datetime

def main_menu(stdscr):
    current_time = datetime.now().strftime("%M")
    def getTicker(): #Func for getting ticker information
        curses.echo()
        prompt = "Type in Ticker: "
        stdscr.addstr(height - 1, 0, prompt)
        tick = (stdscr.getstr(height-1, len(prompt), 15)).decode('utf-8').upper() #Changing binary to string
        curses.noecho()
        price_arr.append(getPrice(tick))
        return tick

    def getPrice(t): #Get Price
        try:
            return str((yf.Ticker(t).history().tail(1)['Close'].iloc[0]))
        except IndexError:
            return "No Value Detected"

    def updatePrices():
        for x in range(len(price_arr)):
            price_arr[x] = getPrice(tick_arr[x])

    def timer():
        later_time = datetime.now().strftime("%M")
        delta = int(later_time) - int(current_time)
        return delta

    def save(str):
        file = open("vitafi_save.txt","a")
        file.write(str + "\n")
        file.close()

    stdscr.clear()
    k = 0
    x_pos = 0
    y_pos = 0
    
    #def cursor(X_POS, Y_POS):
    #    x = X_POS
    #    y = Y_POS
    #    return (x,y)
    #
    #CURSOR = cursor(x_pos, y_pos)
    #
    #def cursor_state ( cursor, x_check, y_check ):
    #    x, y = cursor
    #    x_state = {
    #       "IN_TOP_MENU" : x == 0,
    #       "IN_TICKER_ARR" : x == 1,
    #    }
    #    y_state = {
    #       "BEYOND_UPPER_BOUND" : y > 1 
    #    }
    #    
    #    return x_state and y_state
        
    tick_arr = [] # Initialize tickers, this is where they go
    price_arr = []  # Initialize ticker prices, this is where they go
    stdscr.clear()
    stdscr.refresh()
    menu = False
    

    while (k != ord('q')):
        delta = timer()
        if delta >= 2:
            updatePrices()
            current_time = datetime.now().strftime("%M")

        ## Initialization
        stdscr.clear()
        selection = ""
        height, width = stdscr.getmaxyx()
        start_y = int((height // 2) - 2)
        prompt = "Current Selection: {}".format(selection)
        inprompt = ""
        ticker = "Add Ticker"[:width-1]
        analyze = "Save List"[:width-1]
        start_x_ticker, start_x_analyze = 0,0

        # Menu options for Ticks
        m_delete = "Delete"
        m_analyze = "Analyze"
        m_cancel = "Cancel"


        # Controls
        controls ={
            "DOWN": curses.KEY_DOWN,
            "UP": curses.KEY_UP,
            "LEFT": curses.KEY_LEFT,
            "RIGHT": curses.KEY_RIGHT,
            "ENTER": 10
        }
        
        # COORD STATES
        ## x_state
        X_STATE = {
            "IN_TOP_MENU": x_pos == 0,
            "IN_TICKER_ARR": x_pos == 1
        }
        ## y_state 
        Y_STATE = {
            "BEYOND_UPPER_BOUND": y_pos >= 1,
            "BEYOND_TICK_ARR_LIM": y_pos > (len(tick_arr) - 1)
        }
        
        # MENU STATE (NOT CURRENTLY BEING USED)
        MENU = {
            "IS_OPEN": menu == True
        }
        
        # TIMER 
        c_down = "Prices will update in {} minutes, delta: {}".format(2 - delta, delta) # moved the timer up towards the top of the loop for legibility
        stdscr.addstr(0, (width - len(c_down)), c_down) #timer
        
        # Begin Control Switch (TODO: REFACTOR TO DICTIONARY AND CASE)
        if k == controls["DOWN"]:
            y_pos += 1
            if MENU["IS_OPEN"]:
                menu = False ## close menu
            if  X_STATE["IN_TOP_MENU"] and Y_STATE["BEYOND_UPPER_BOUND"]: #
                y_pos = 0
            if X_STATE["IN_TICKER_ARR"] and Y_STATE["BEYOND_TICK_ARR_LIM"]:
                y_pos = 0
        elif k == controls["UP"]:
            y_pos -= 1
            if menu == True:
                menu = False
            if X_STATE["IN_TOP_MENU"] and y_pos <= - 1:
                    y_pos = 1
            if X_STATE["IN_TICKER_ARR"] and y_pos <= -1:
                    y_pos = y_pos + len(tick_arr)
                    
        if (tick_arr) and k == controls["RIGHT"]: # if (tick_arr) == if len(tick_arr) > 0 
                x_pos = x_pos + 1                 ## idk if (y_pos <= 1)  was necessary for these conditionals, so I took it out, it's commented out below
                if menu == True and x_pos > 3:
                        x_pos = 0
                        menu = False
                elif menu == False and x_pos > 1:
                        x_pos = 0
        if (tick_arr) and k == controls["LEFT"]: # and y_pos <= 1
                x_pos = x_pos - 1
                if menu == True and x_pos == 0:
                    menu = False
        if x_pos == -1:
            x_pos = 1

        
        #TOP MENU NAV
        if y_pos == 0 and X_STATE["IN_TOP_MENU"]:
            stdscr.addstr(start_y, start_x_ticker, ticker, curses.A_STANDOUT)
            inprompt = "Add a Ticker!"
            if k == controls["ENTER"]: # if input is enter
                newTick = getTicker()
                tick_arr.append(newTick)
        else:
            stdscr.addstr(start_y, start_x_ticker, ticker)

        if y_pos == 1 and X_STATE["IN_TOP_MENU"]:
            stdscr.addstr(start_y + 1, start_x_analyze, analyze, curses.A_STANDOUT)
            inprompt = "Save Ticker List!"
            if k == controls["ENTER"]:
                count = 0
                for x in range(len(tick_arr)):
                    save(tick_arr[x])
                    inprompt = "%{} saved...".format((x/len(tick_arr[x])) * 10)
        else:
            stdscr.addstr(start_y + 1, start_x_analyze, analyze)


        if len(tick_arr) > 0:
            for x in range(len(tick_arr)):
                tick_x = tick_arr[x]
                ARRS = {
                    "$SYMBOLS" : [start_y + x,((width // 3) - (len(tick_arr[x]) // 2) - len(tick_arr[x]) % 2), tick_arr[x]],
                    "PRICES" : [start_y + x, (width - len(price_arr[x])), price_arr[x]]
                }
                if y_pos == x and x_pos >= 1 and x_pos <= 3:
                    stdscr.addstr(*ARRS["$SYMBOLS"],curses.A_STANDOUT)
                    stdscr.addstr(*ARRS["PRICES"])
                    inprompt = "See options for {} {}".format(tick_arr[x],price_arr[x])
                    if k == controls["ENTER"]: #if input is enter
                        menu = True
                    if menu == True:
                        inprompt = "|{} Menu|".format(tick_arr[x])
                        MENU_OPTS = {
                            "ANALYZE" : [height -2, 0, m_analyze],
                            "DELETE" : [height - 2, len(m_analyze) + 2, m_delete],
                            "CANCEL" : [height - 2, len(m_analyze) + len(m_delete) + 4, m_cancel]
                        }
                        
                        #def handle_del(menu, x_pos, inPrompt, tick_arr, price_arr) : 
                        #def handle_cancel(inPrompt, menu) :
                        
                        #HANDLE= {
                        #    "ANALYZE" : lambda: inprompt,
                        #    "DELETE" : handle_del(menu, x_pos, inPrompt, tick_arr, price_arr),
                        #    "CANCEL" : handle_cancel(inPrompt, menu)
                        #}
                        
                        def HIGHLIGHT(here) :
                            for opt, val in MENU_OPTS.items():
                                if opt == here: 
                                    stdscr.addstr(*val, curses.A_STANDOUT)
                                else :
                                    stdscr.addstr(*val)
                                    
                        if x_pos == 1:
                            HIGHLIGHT("ANALYZE")
                            inprompt = inprompt + " Analyze {}".format(tick_arr[x])
                        elif x_pos == 2:
                            HIGHLIGHT("DELETE")
                            inprompt = inprompt + " Delete - Erase from list"
                            if k == controls["ENTER"]:
                                #HANDLE["DELETE"]
                                menu = False
                                x_pos = 0
                                inprompt = "Deleted {}! Press Any Key to Continue...".format(tick_arr[x])
                                tick_arr.remove(tick_arr[x])
                                price_arr.remove(price_arr[x])
                        elif x_pos == 3:
                            HIGHLIGHT("CANCEL")
                            inprompt = inprompt + " Cancel - Exit Menu "
                            if k == controls["ENTER"]:
                                #HANDLE["CANCEL"]
                                inprompt = "Out of {} Menu, Press any Key to Continue...".format(tick_arr[x])
                                menu = False
                       
                       # def menu_nav(x_, inPrompt) :
                       #     def HIGHLIGHT(here) :
                       #         for opt, val in MENU_OPTS.items():
                       #             if opt == here: 
                       #                 stdscr.addstr(*val, curses.A_STANDOUT)
                       #             else :
                       #                 stdscr.addstr(*val)
                       #     def SELECT_1(inPrompt) : 
                       #         HIGHLIGHT("ANALYZE")
                       #         inPrompt = inPrompt + " Analyze {}".format(tick_arr[x])
                       #     def SELECT_2(inPrompt) :
                       #         HIGHLIGHT("DELETE")
                       #         inPrompt = inPrompt + " Delete - Erase from list"
                       #     def SELECT_3(inPrompt) :
                       #         HIGHLIGHT("CANCEL")
                       #         inPrompt = inPrompt + " Cancel - Exit Menu "
                       #     selector = {
                       #         1 : SELECT_1(inPrompt),
                       #         2 : SELECT_2(inPrompt),
                       #         3 : SELECT_3(inPrompt)
                       #       }
                       #     
                       #     return selector.get(x_, lambda: "darn")
                       # menu_nav(x_pos, inprompt)

                else:
                    stdscr.addstr(start_y + x,((width // 3) - (len(tick_arr[x]) // 2) - len(tick_arr[x]) % 2), tick_arr[x])
                    stdscr.addstr(start_y + x, (width - len(price_arr[x])), price_arr[x])
        if len(tick_arr) > 0:
            prompt = "Action: {} ".format(inprompt)
        else:
            prompt = "Action: {}".format(inprompt)
        
        stdscr.addstr(height-1, 0, prompt)
        stdscr.refresh()
        k = stdscr.getch()

def main():
    curses.wrapper(main_menu)

if __name__ == "__main__":
    main()
