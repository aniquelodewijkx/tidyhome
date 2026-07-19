import random
import inquirer
import pandas as pd
import time
import importlib.resources

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"

CYCLE_COLORS = [CYAN, MAGENTA, YELLOW, GREEN, BLUE, RED]
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

SPINNER_FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"


BANNER_ART = r"""
                 _ _
                ( Y )
                 \ /
                  \          /^\
                    )       //^\\
                 (         //   \\
                   )      //     \\
                  __     //       \\
                 |=^|   //    _    \\
               __|= |__//    (+)    \\
              /LLLLLLL//      ~      \\
             /LLLLLLL//               \\
            /LLLLLLL//                 \\
           /LLLLLLL//  |~[|]~| |~[|]~|  \\
           ^| [|] //   | [|] | | [|] |   \\
            | [|] ^|   |_[|]_| |_[|]_|   |^
         ___|______|                     |
        /LLLLLLLLLL|_____________________|
       /LLLLLLLLLLL/LLLLLLLLLLLLLLLLLLLLLL\
      /LLLLLLLLLLL/LLLLLLLLLLLLLLLLLLLLLLLL\
      ^||^^^^^^^^/LLLLLLLLLLLLLLLLLLLLLLLLLL\
       || |~[|]~|^^||^^^^^^^^^^||^|~[|]~|^||^^
       || | [|] |  ||  |~~~~|  || | [|] | ||
       || |_[|]_|  ||  | [] |  || |_[|]_| ||
       ||__________||  |   o|  ||_________||
     .'||][][][][][||  | [] |  ||[][][][][||.'.
    ."'||[][][][][]||_-`----'-_||][][][][]||"."
  .(')^(.)(').( )'^@/-- -- - --\@( )'( ).(( )^(.)^
 '( )^(`)'.(').( )@/-- -- - -- -\@ (.)'(.),( ).(').
 ".'.'." ." '.". @/- - --- -- - -\@ '.".'.".'.".'."
 ". '' ".".".'.'@/ - -- -- -- -- -\@".'..'".'."'.'.'
'.".".''.".''."@/ -- --- --- -- - -\@.".''.".''.".'".
"""


def print_banner():
    print(f"{CYAN}{BANNER_ART}{RESET}")
    print(f"{BOLD}🧹 tidyhome{RESET} {DIM}— who's tidying what today?{RESET}\n")


def get_names():
    answer = inquirer.prompt([inquirer.Text('num_players', message="How many players are there?")])
    num_players = int(answer["num_players"])
    questions = []
    for i in range(num_players):
        questions.append(inquirer.Text(f"player_name_{i+1}", message=f"Player #{i+1}"))

    names = inquirer.prompt(questions)
    return list(names.values())


def get_tasks():
    with importlib.resources.open_text("tidyhome", "tasks.csv") as f:
        tasks_df = pd.read_csv(f)

    categories = tasks_df["category"].unique().tolist()
    category_selection = inquirer.prompt(
        [inquirer.Checkbox('categories',
                           message="What's getting tidied today? \n(select: <space>, finish: <enter>)",
                           choices=["all"] + categories)]
    )["categories"]

    if "all" in category_selection:
        category_selection = categories

    possible_tasks = []
    for task, category in zip(tasks_df["task"], tasks_df["category"]):
        if category in category_selection:
            possible_tasks.append(task)

    if not possible_tasks:
        print("No tasks in the selected categories. Exiting.")
        return None

    return possible_tasks


def spin_task(name, tasks):
    max_length = max(len(word) for word in tasks)

    print(HIDE_CURSOR, end="")
    try:
        print(f"\n{BOLD}{name}{RESET}:")
        for i in range(15):
            task = random.choice(tasks)
            frame = SPINNER_FRAMES[i % len(SPINNER_FRAMES)]
            color = CYCLE_COLORS[i % len(CYCLE_COLORS)]
            print(f"\r  {CYAN}{frame}{RESET} {color}{task.ljust(max_length)}{RESET}", end="", flush=True)
            time.sleep(0.1 + (i / 20) * 0.35)

        print(f"\r  {GREEN}✔{RESET} {BOLD}{task.ljust(max_length)}{RESET}\n", flush=True)
    finally:
        print(SHOW_CURSOR, end="", flush=True)

    tasks.remove(task)
    return task

def print_balloons():
    # Three balloons drawn as columns so each can be its own color.
    balloon = [" .-. ", "(   )", " `-' ", "  )  ", "  (  "]
    colors = [RED, MAGENTA, CYAN]
    for row in balloon:
        line = "   ".join(f"{color}{row}{RESET}" for color in colors)
        print(f"      {line}")


def print_session_summary(session_log):
    if not session_log:
        return

    by_name = {}
    for name, task, done in session_log:
        by_name.setdefault(name, []).append((task, done))

    print(f"\n{BOLD}🧾 Session summary{RESET}")
    for name, entries in by_name.items():
        print(f"\n{BOLD}{name}{RESET}")
        for task, done in entries:
            mark = f"{GREEN}✔{RESET}" if done else f"{RED}✘{RESET}"
            print(f"  {mark} {task}")

    completed_count = sum(1 for _, _, done in session_log if done)
    print()
    print_balloons()
    print(f"\n{GREEN}{BOLD}✨ Congratulations! You completed {completed_count} task(s) today.{RESET}")


def main():
    print_banner()
    names = get_names()
    tasks = get_tasks()

    if tasks is None:
        exit(0)

    DONE = "We're done for today"
    in_progress = {}  # name -> the task that player is currently working on
    session_log = []  # (name, task, completed) for every assignment this session

    # Pull model: whoever finishes their task comes back and grabs the next one.
    # Asking for a new task means your previous one is done.
    while tasks:
        answer = inquirer.prompt(
            [inquirer.List('name',
                           message="Who's ready for a task?",
                           choices=names + [DONE])])
        if answer['name'] == DONE:
            break

        name = answer['name']
        if name in in_progress:
            session_log.append((name, in_progress.pop(name), True))
        in_progress[name] = spin_task(name, tasks)

    if not tasks:
        print("All tasks have been assigned.")

    if in_progress:
        finished_prompt = inquirer.prompt(
            [inquirer.Checkbox('finished',
                               message="Which of these last tasks got finished?",
                               choices=[(f"{name}: {task}", name) for name, task in in_progress.items()])])
        finished = set(finished_prompt['finished'] or [])
        for name, task in in_progress.items():
            session_log.append((name, task, name in finished))

    print_session_summary(session_log)


if __name__ == '__main__':
    main()