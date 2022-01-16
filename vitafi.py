import curses
import yfinance as yf


def main_menu(stdscr):
    def getTicker():
        curses.echo()
        prompt = "Ticker: "
        stdscr.addstr(height - 1, 0, prompt)
        tick = (stdscr.getstr(height-1, len(prompt), 15)).decode('utf-8')
        curses.noecho()
        return tick
    def getPrice(t):
        return str((yf.Ticker(t).history().tail(1)['Close'].iloc[0]))

    stdscr.clear()
    k = 0
    x_pos = 0
    y_pos = 0
    tick_arr = []

    stdscr.clear()
    stdscr.refresh()

    while (k != ord('q')):

        stdscr.clear()
        selection = ""
        height, width = stdscr.getmaxyx()
        start_y = int((height // 2) - 2)
        prompt = "Current Selection: {}".format(selection)
        inprompt = ""


        ticker = "Add Ticker"[:width-1]
        analyze = "Analyze"[:width-1]

        start_x_ticker, start_x_analyze = 0,0
        if k == curses.KEY_DOWN:
            y_pos = y_pos + 1
            if x_pos == 0:
              if (y_pos > 1):
                y_pos = 0
            if x_pos == 1:
                if (y_pos >= len(tick_arr)):
                    y_pos = 0
        elif k == curses.KEY_UP:
            y_pos = y_pos - 1
            if x_pos == 0:
                if y_pos <= - 1:
                    y_pos = 1
            if x_pos == 1:
                if y_pos <= -1:
                    y_pos = y_pos + len(tick_arr)
        if len(tick_arr) > 0 and y_pos <= 1:
            if k == curses.KEY_RIGHT:
                x_pos = x_pos + 1
                if x_pos > 1:
                    x_pos = 0
        if len(tick_arr) > 0 and y_pos <= 1:
            if k == curses.KEY_LEFT:
                x_pos = x_pos - 1
        if x_pos == -1:
            x_pos = 1

        if y_pos == 0 and x_pos == 0:
            stdscr.addstr(start_y, start_x_ticker, ticker, curses.A_STANDOUT)
            inprompt = "Add a Ticker!"
            if k == 10:
                newTick = getTicker()
                tick_arr.append(newTick)
        else:
            stdscr.addstr(start_y, start_x_ticker, ticker)

        if y_pos == 1 and x_pos == 0:
            stdscr.addstr(start_y + 1, start_x_analyze, analyze, curses.A_STANDOUT)
            inprompt = "Analyze a Ticker!"
        else:
            stdscr.addstr(start_y + 1, start_x_analyze, analyze)

        if len(tick_arr) > 0:
            for x in range(len(tick_arr)):
                tick_x = tick_arr[x]
                if y_pos == x and x_pos == 1:
                    stdscr.addstr(start_y + x,((width // 2) - (len(tick_arr[x]) // 2) - len(tick_arr[x]) % 2), tick_arr[x],curses.A_STANDOUT)
                    stdscr.addstr(start_y + x, (width - len(getPrice(tick_x))), getPrice(tick_x))
                    inprompt = "See price history for {}".format(tick_arr[x])
                else:
                    stdscr.addstr(start_y + x,((width // 2) - (len(tick_arr[x]) // 2) - len(tick_arr[x]) % 2), tick_arr[x])
                    stdscr.addstr(start_y + x, (width - len(getPrice(tick_x))), getPrice(tick_x))
        if len(tick_arr) > 0:
            prompt = "Action: {} | Data Type for tick_arr[]: {}".format(inprompt, type(tick_arr[0]))
        else:
            prompt = "Action: {} | test MVIS: {}".format(inprompt, getPrice("MVIS"))
        stdscr.addstr(height-1, 0, prompt)


        stdscr.refresh()
        k = stdscr.getch()

def main():
    curses.wrapper(main_menu)

if __name__ == "__main__":
    main()
