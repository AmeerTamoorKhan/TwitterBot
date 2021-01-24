import pandas as pd
from TwitterBot import TwitterBot
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
from tkintertable.App import TablesApp
import os
from PIL.ImageTk import PhotoImage
from PIL import Image


root = Tk()
root.title('Twitter Bot')
Total_Tweets = 0
data = 0
Flag = False


def search(trend, noOfTweets, fileName, progress):
    global Total_Tweets, data, Flag
    if trend and noOfTweets:
        try:
            trend = trend.get(1.0, 'end').replace("\n", "")
            no_of_tweets = int(noOfTweets_text.get(1.0, 'end'))
            print(trend, no_of_tweets)
        except:
            return
    else:
        return
    Total_Tweets = no_of_tweets
    bot = TwitterBot(trend, no_of_tweets)
    bot.scrap_tweets(progress)
    data = bot.df[['Id', 'Tweet', 'Likes Count']]

    fileName = fileName.replace("\n", "")
    if fileName != '':
        try:
            os.remove(fileName)
        except:
            pass
        data.to_csv('Data/'+fileName+'.csv', index=False)
    else:
        try:
            os.remove("Data/Tweets.csv")
        except:
            pass

        data.to_csv('Data/Tweets.csv', index=False)
    Flag = True
    step()
    bot.close()


def step():
    progress['value'] += 100


def show_tweets(filename):
    global data, Total_Tweets, Flag
    filename = filename.replace("\n", "")
    if Flag:
        if filename != '':
            Table.importCSV('Data/'+filename+'.csv')
        else:
            Table.importCSV('Data/Tweets'+'.csv')

        Table.show()
        Table.resizeColumn(1, 485)


def reset():
    rows = [i for i in range(Total_Tweets)]
    cols = [0, 1, 2]
    Table.deleteCells(rows=rows, cols=cols)
    trend_text.delete(1.0, 'end')
    saveFile_text.delete(1.0, 'end')
    noOfTweets_text.delete(1.0, 'end')
    progress['value'] = 0


move_x = 0.05
canvas = Canvas(root, width=1000, height=950, bg='#ececec')
canvas.pack()

path = ['Images/Bot.png', 'Images/twitter.png']
twit = Image.open(path[1])
twit.thumbnail((300, 300), Image.ANTIALIAS)
twitter_img = PhotoImage(twit)
canvas.create_image(450, 100, image=twitter_img)

im = Image.open(path[0])
im.thumbnail((175, 175), Image.ANTIALIAS)
bot_img = PhotoImage(im)
canvas.create_image(700, 85, image=bot_img)

trend_label = Label(canvas, bg='#ececec', text='Enter Trend:', font='Helvetica 20 bold')
trend_label.place(relx=move_x+0.08, rely=0.205)

trend_text = Text(canvas, bg='white', bd=3, font='Helvetica 20 bold')
trend_text.place(relx=move_x+0.21, rely=0.2, relwidth=0.25, relheight=0.05)

noOfTweets_label = Label(canvas, bg='#ececec', text='Total Tweets:', font='Helvetica 20 bold')
noOfTweets_label.place(relx=move_x+0.47, rely=0.205)

noOfTweets_text = Text(canvas, bg='white', bd=3, font='Helvetica 20 bold')
noOfTweets_text.place(relx=move_x+0.61, rely=0.2, relwidth=0.15, relheight=0.05)

saveFile_label = Label(canvas, bg='#ececec', text='Save As:', font='Helvetica 20 bold')
saveFile_label.place(relx=move_x+0.08, rely=0.3)

saveFile_text = Text(canvas, bg='white', bd=3, font='Helvetica 20 bold')
saveFile_text.place(relx=move_x+0.21, rely=0.3, relwidth=0.25, relheight=0.05)

search_button = Button(canvas, text='Enter', font='Helvetica 20 bold',
                       command=lambda: search(trend_text, noOfTweets_text, saveFile_text.get(1.0, 'end'), progress))
search_button.place(relx=move_x+0.61, rely=0.3, relwidth=0.15, relheight=0.05)

progress = ttk.Progressbar(canvas, length=100, orient=HORIZONTAL, mode='determinate')
progress.place(relx=move_x+0.45, rely=0.38, relwidth=0.5, anchor='n')

show_button = Button(canvas, text='Show Tweets', font='Helvetica 20 bold', command=lambda: show_tweets(saveFile_text.get(1.0, 'end')))
show_button.place(relx=move_x+0.3, rely=0.42, relwidth=0.15, relheight=0.05, anchor='n')

reset_button = Button(canvas, text='Reset', font='Helvetica 20 bold', command=lambda: reset())
reset_button.place(relx=move_x+0.6, rely=0.42, relwidth=0.15, relheight=0.05, anchor='n')


frame = Frame(canvas, bd=10, bg='#ececec')
frame.config(highlightbackground="red", highlightcolor="red")

model = TableModel()
frame.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.45)
Table = TableCanvas(frame, model=model, cols=3, thefont=('Helvetica', 13),
                    rows=Total_Tweets, rowheight=50, rowselectedcolor='#ececec',
                    cellbackgr='#ececec', read_only=False)
Table.show()
#Table.place(relx=0.06, rely=0.06, relwidth=0.94, relheight=0.94)



root.mainloop()

if __name__ == "__main__":
    pass
