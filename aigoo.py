import numpy as np
import pandas as pd
import re
import sys
from bs4 import BeautifulSoup
import requests
import random
from tkinter import *
from tkinter import ttk
import tkinter as tk
from queue import Queue
from subprocess import PIPE, Popen
from threading import Thread

SEARCH_URL = "https://stackoverflow.com"
# SEARCH_URL = "https://codereview.stackexchange.com/"
USAGE = (f"Usage: {sys.argv[0]} "
         "[--help] | python aigoo.py [file_name | file_path]")


def get_search_results(soup):
    """Returns a list of dictionaries containing each search result."""
    search_results = []
    for result in soup.find_all("div", class_="question-summary search-result"):
        title_container = result.find_all(
            "div", class_="result-link")[0].find_all("a")[0]
        if result.find_all("div", class_="status answered") != []:
            answer_count = int(result.find_all("div", class_="status answered")[
                               0].find_all("strong")[0].text)
        elif result.find_all("div", class_="status answered-accepted") != []:
            answer_count = int(result.find_all(
                "div", class_="status answered-accepted")[0].find_all("strong")[0].text)
        else:
            answer_count = 0
        search_results.append({
            "Title": title_container["title"],
            "Answers": answer_count,
            "URL": SEARCH_URL + title_container["href"]
        })
    return search_results


def souper(url):
    """Turns a given URL into a BeautifulSoup object."""
    try:

        html = requests.get(url)
    except requests.exceptions.RequestException:
        print('''Dope was unable to fetch Stack Overflow results.
                    Please check that you are connected to the internet.\n''')
        sys.exit(1)
    if re.search("\.com/nocaptcha", html.url):  # URL is a captcha page
        return None
    else:
        return BeautifulSoup(html.text, "html.parser")


def search(query):
    """Wrapper function for get_search_results."""
    soup = souper(SEARCH_URL + "/search?pagesize=50&q=%s" %
                  query.replace(' ', '+'))
    if soup == None:
        return (None, True)
    else:
        return (get_search_results(soup), False)


def get_error_message(error, language):
    if error == '':
        return None
    elif language == "python":
        # Non-compiler errors
        if any(e in error for e in ["KeyboardInterrupt", "SystemExit", "GeneratorExit"]):
            return None
        else:
            return error.split('\n')[-2].strip()


def get_language(file_path):
    """Returns the language a file is written in."""
    # print(file_path)
    if file_path.endswith(".py"):
        return "python"
    else:
        return ''


def read(pipe, funcs):
    """Reads and pushes piped output to a shared queue and appropriate lists."""
    for line in iter(pipe.readline, b''):
        for func in funcs:
            func(line.decode("utf-8"))
    pipe.close()


def write(get):
    """Pulls output from shared queue and prints to terminal."""
    for line in iter(get, None):
        print(line)


def execute(command):
    """Executes a given command and clones stdout/err to both variables and the
    terminal (in real-time)."""
    # print(command)
    process = Popen(
        command,
        # cwd=None,
        # shell=True,
        # stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
    )

    output, errors = [], []
    pipe_queue = Queue()

    # Threads for reading stdout and stderr pipes and pushing to a shared queue
    stdout_thread = Thread(target=read, args=(
        process.stdout, [pipe_queue.put, output.append]))
    stderr_thread = Thread(target=read, args=(
        process.stderr, [pipe_queue.put, errors.append]))

    # Thread for printing items in the queue
    writer_thread = Thread(target=write, args=(pipe_queue.get,))

    # Spawns each thread
    for thread in (stdout_thread, stderr_thread, writer_thread):
        thread.daemon = True
        thread.start()

    process.wait()

    for thread in (stdout_thread, stderr_thread):
        thread.join()

    pipe_queue.put(None)

    output = ' '.join(output)
    errors = ' '.join(errors)

    # output, errors = process.communicate()[0], process.communicate()[1]
    # print('combined output:', repr(output.decode('utf-8')))
    # print('stderr value   :', repr(errors.decode('utf-8')))

    return (output, errors)
    # while process.returncode is None:
    #     i = sys.stdin.read(1)
    #     if i == '':
    #         process.stdin.close()
    #         break
    #     process.stdin.write(i)
    #     process.poll()

    # while process.returncode is None:
    #     process.poll()
gurl = []


def app(r):
    def selectItem(a):
        curItem = tree.focus()
        # print(tree.item(curItem))
        x = (tree.item(curItem).values())
        x = list(x)
        # print(x)
        global gurl
        gurl = (x[2][2])
        # print(gurl)
        get_question_and_answers(gurl)

    m = r
    main1 = []
    l = []
    for _ in range(len(m)):
        array = np.array([(key, val) for (key, val) in m[_].items()])
        l.append(array)
    data = pd.Series(l)
    for i in range(len(m)):
        main = []
        for j in range(3):
            main.append(data[i][j][1])
        main1.append(main)
    d = pd.DataFrame(main1, columns=['Title', 'Answer', 'URL'])
    data = d.values.tolist()

    root = Tk()
    root.title("RESULT")
    root.geometry("1200x800")

    frame = Frame(root)
    frame.pack()
    tree = ttk.Treeview(frame, columns=(1, 2, 3), height=30, show="headings")
    tree.pack(side='left')
    #tree.heading(1,text="Sr. No")
    tree.heading(1, text="Title")
    tree.heading(2, text="Answer")
    tree.heading(3, text="Url")
    #tree.column(1, width=100)
    tree.column(1, width=500)
    tree.column(2, width=50)
    tree.column(3, width=500)
    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scroll.set)
    # def printans():
    #    print(s)
    for val in data:  # for i in data: i is counter
        # tree.insert('', 'end', values = (i, data[0], data[1], data[2]))
        tree.insert('', 'end', values=(val[0], val[1], val[2]))
    #selection = list.curselection()
    #print([list.get(i) for i in selection])
    tree.bind('<ButtonRelease-1>', selectItem)
    #slogan = ttk.Button(frame, text="Search Result", command=get_question_and_answers(gurl))
    # slogan.pack(side=tk.LEFT)
    root.mainloop()


# print(y)
def get_question_and_answers(url):
    soup = souper(url)
    if soup == None:  # Captcha page
        return "Sorry, Stack Overflow blocked our request. Try again in a couple seconds.", "", "", ""
    else:
        question_title = soup.find_all(
            'a', class_="question-hyperlink")[0].get_text()
        question_stats = soup.find(
            "div", class_="js-vote-count").get_text()  # Vote count
        try:
            question_stats = question_stats + " Votes | " + '|'.join((((soup.find_all("div", class_="module question-stats")[0].get_text())
                                                                       .replace('\n', ' ')).replace("     ", " | ")).split('|')[:2])  # Vote count, submission date, view count
        except IndexError:
            question_stats = "Could not load statistics."
        question_desc = (soup.find_all("div", class_="post-text")
                         [0].get_text())  # TODO: Handle duplicates
        question_stats = ' '.join(question_stats.split())
        # answercell post-layout--right
        answers = (
            soup.find("div", class_="answercell post-layout--right")).get_text()
        if len(answers) == 0:
            answers.append(
                (("No Answers", u"\nNo Answers for this question.")))
        # print("questions :", question_title)
        # print("Question Discription : ")
        # print(question_desc)
        # print("Answers : ")
        answers = (''.join(map(str, answers)))
        # print(answers)

        lst = []
        lst.append(question_title)
        lst.append(question_desc)
        lst.append(answers)

        r1 = Tk()
        r1.title("Question & Solutions")
        r1.geometry("1600x800")
        t = Text(r1)
        for x in lst:
            t.insert(END, x + '\n')
        t.pack()
        r1.mainloop()


def main():
    args = sys.argv[1:]
    # args = sys.argv[1:]
    if not args:
        args = ["-"]
    if args[0] == "-" or args[0] == '-h' or args[0] == '--help':
        raise SystemExit(USAGE)
    else:
        language = get_language(args[0])  # Gets the language name

        if language == '':  # Unknown language
            print(f"Sorry,  doesn't support this file type.")
            return
        file_path = args[0]
        # print(file_path)
        # Compiles the file and pipes stdout
        output, error = execute([language] + [file_path])
        if (output, error) == (None, None):  # Invalid file
            return
        # Prepares error message for search
        error_msg = get_error_message(error, language)
        if error_msg != None:
            query = f'{language} {error_msg}'
            search_results, captcha = search(query)
            if search_results != []:
                if captcha:
                    print(
                        f"Sorry, Stack Overflow blocked our request. Try again in a minute.")
                    return
                # elif confirm("Display Stack Overflow results?"):
                # print(search_results)
                # printlinks(search_results)  # Opens interface
                else:
                    app(search_results)
                    # print(search_results)
            else:
                print(f"No Stack Overflow results found.")
        else:
            print(f"No error detected :)")
    return
