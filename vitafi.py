import curses
import yfinance as yf
from datetime import datetime

def main_menu(stdscr):
    current_time = datetime.now().strftime("%M")
    def getTicker(): #Func for getting ticker information
        curses.echo()
        prompt = "Type in Ticker: "
        stdscr.addstr(height - 1, 0, prompt)
        tick = (stdscr.getstr(height-1, len(prompt), 15)).decode('utf-8') #Changing binary to string
        curses.noecho()
        tick = tick.upper()
        price_arr.append(getPrice(tick))
        return tick

    def getPrice(t): #Get Price
        try:
            return str((yf.Ticker(t).history().tail(1)['Close'].iloc[0]))
        except IndexError:
            return "No Value Detected"

    def updatePrices():
        for x in range(len(price_arr)):
            price_arr[x] = getPrice(tick_arr[x][1:]) #tick_arr[x][1:] will slice off the '$'

    def timer():
        later_time = datetime.now().strftime("%M")
        delta = int(later_time) - int(current_time)
        return delta

    def save(str):
        file = open("./vitafi_save.txt","a")
        file.write(str + "\n")
        file.close()

    stdscr.clear()
    k = 0
    x_pos = 0
    y_pos = 0
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

        stdscr.clear()
        selection = ""
        height, width = stdscr.getmaxyx()
        start_y = int((height // 3) - 3)
        prompt = "Current Selection: {}".format(selection)
        inprompt = ""
        ticker = "Add Ticker"[:width-1]
        analyze = "Save List"[:width-1]
        refresh = "Refresh List"[:width-1]
        start_x_ticker, start_x_analyze, start_x_refresh = 0,0,0

        #Menu scripts for Ticks
        m_delete = "Delete"
        m_analyze = "Analyze"
        m_cancel = "Cancel"


        #Controls
        if k == curses.KEY_DOWN:
            y_pos = y_pos + 1
            if menu == True:
                menu = False
            if x_pos == 0:
              if (y_pos > 1):
                y_pos = 0
            if x_pos == 1:
                if (y_pos >= len(tick_arr)):
                    y_pos = 0
        elif k == curses.KEY_UP:
            y_pos = y_pos - 1
            if menu == True:
                menu = False
            if x_pos == 0:
                if y_pos <= - 1:
                    y_pos = 1
            if x_pos == 1:
                if y_pos <= -1:
                    y_pos = y_pos + len(tick_arr)
        if len(tick_arr) > 0 and y_pos <= 1:
            if k == curses.KEY_RIGHT:
                x_pos = x_pos + 1
                if menu == True:
                    if x_pos > 3:
                        x_pos = 0
                        menu = False
                elif menu == False:
                    if x_pos > 1:
                        x_pos = 0
        if len(tick_arr) > 0 and y_pos <= 1:
            if k == curses.KEY_LEFT:
                x_pos = x_pos - 1
                if menu == True and x_pos == 0:
                    menu = False
        if x_pos == -1:
            x_pos = 1

        c_down = "Prices will update in {} minutes, delta: {}".format(2 - delta, delta)
        stdscr.addstr(0, (width - len(c_down)), c_down) #timer
        
        # Main Nav
        
        ## Add Ticker
        if y_pos == 0 and x_pos == 0:
            stdscr.addstr(start_y, start_x_ticker, ticker, curses.A_STANDOUT)
            inprompt = "Add a Ticker!"
            if k == 10: # if input is enter
                newTick = getTicker()
                tick_arr.append('$' + newTick)
        else:
            stdscr.addstr(start_y, start_x_ticker, ticker)
        
        ## Save List
        if y_pos == 1 and x_pos == 0:
            stdscr.addstr(start_y + 1, start_x_analyze, analyze, curses.A_STANDOUT)
            inprompt = "Save Ticker List!"
            if k == 10:
                count = 0
                for x in range(len(tick_arr)):
                    save(tick_arr[x])
                    inprompt = "%{} saved...".format((x/len(tick_arr[x])) * 10)
        else:
            stdscr.addstr(start_y + 1, start_x_analyze, analyze)
        
        ## Refresh List
        if y_pos == 2 and x_pos == 0:
            stdscr.addstr(start_y + 2 , start_x_refresh, refresh, curses.A_STANDOUT)
            inprompt = "Refresh List!"
            if k == 10:
                updatePrices()
        else:
            stdscr.addstr(start_y + 2, start_x_refresh, refresh)


        if len(tick_arr) > 0:
            for x in range(len(tick_arr)):
                tick_x = tick_arr[x]
                if y_pos == x and x_pos >= 1 and x_pos <= 3:
                    stdscr.addstr(start_y + x,((width // 3) - (len(tick_arr[x]) // 2) - len(tick_arr[x]) % 2), tick_arr[x],curses.A_STANDOUT)
                    stdscr.addstr(start_y + x, (width - len(price_arr[x])), price_arr[x])
                    inprompt = "See options for {} {}".format(tick_arr[x],k)
                    if k == 10: #if input is enter
                        menu = True
                    if menu == True:
                          inprompt = "|{} Menu|".format(tick_arr[x])
                          if x_pos == 1:
                            stdscr.addstr(height - 2, 0, m_analyze, curses.A_STANDOUT)
                            stdscr.addstr(height - 2, len(m_analyze) + 2, m_delete)
                            stdscr.addstr(height - 2, len(m_analyze) + len(m_delete) + 4, m_cancel)
                            inprompt = inprompt + " Analyze {}".format(tick_arr[x])
                          elif x_pos == 2:
                            stdscr.addstr(height - 2, 0, m_analyze)
                            stdscr.addstr(height - 2, len(m_analyze) + 2, m_delete, curses.A_STANDOUT)
                            stdscr.addstr(height - 2, len(m_analyze) + len(m_delete) + 4, m_cancel)
                            inprompt = inprompt + " Delete - Erase from list"
                            if k == 10:
                                menu = False
                                x_pos = 0
                                inprompt = "Deleted {}! Press Any Key to Continue...".format(tick_arr[x])
                                tick_arr.remove(tick_arr[x])
                                price_arr.remove(price_arr[x])
                          elif x_pos == 3:
                            stdscr.addstr(height - 2, 0, m_analyze)
                            stdscr.addstr(height - 2, len(m_analyze) + 2, m_delete)
                            stdscr.addstr(height - 2, len(m_analyze) + len(m_delete) + 4, m_cancel, curses.A_STANDOUT)
                            inprompt = inprompt + " Cancel - Exit Menu "
                            if k == 10:
                                inprompt = "Out of {} Menu, Press any Key to Continue...".format(tick_arr[x])
                                menu = False


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
