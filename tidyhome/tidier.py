import random
import inquirer
import json
import time
import argparse
import importlib.resources
import tidyhome


def get_names():
    answer = inquirer.prompt([inquirer.Text('num_players', message="How many players are there?")])
    num_players = int(answer["num_players"])
    questions = []
    for i in range(num_players):
        questions.append(inquirer.Text(f"player_name_{i+1}", message=f"Player #{i+1}"))

    names = inquirer.prompt(questions)
    return names


def get_tasks():
    with importlib.resources.open_text("tidyhome", "tasks.json") as f:
        all_categories = json.load(f)
    category_selection = inquirer.prompt(
        [inquirer.Checkbox('categories',
                           message="What's getting tidied today? \n(Press <space> to select, Enter when finished)",
                           choices=all_categories)]
    )["categories"]

    possible_tasks = []
    for category, task_list in all_categories.items():
        if category in category_selection:
            possible_tasks.extend(task_list)

    return possible_tasks


def assign_tasks(names, tasks):
    max_length = max(len(word) for word in tasks)
    for _, name in names.items():
        if not tasks:
            print("All tasks have been assigned. Exiting.")
            break
        print(f"\n{name}:")
        for i in range(15):
            task = random.choice(tasks)
            print("\r" + task.ljust(max_length), end="", flush=True)
            time.sleep(0.1 + (i / 20) * 0.35)

        print("\r" + task.ljust(max_length), flush=True)
        tasks.remove(task)


def main():
    parser = argparse.ArgumentParser(description="A random task assignment tool for tidying up your home")
    args = parser.parse_args()

    names = get_names()
    tasks = get_tasks()

    if tasks is None:
        print("No tasks selected. Exiting.")
        exit(0)

    while tasks:
        assign_tasks(names, tasks)
        if not tasks:
            print("All tasks have been assigned. Exiting.")
            break
        continue_prompt = inquirer.prompt(
            [inquirer.Confirm('continue', message="Do you want to continue assigning tasks?", default=True)])
        if not continue_prompt['continue']:
            print("Exiting.")
            break


if __name__ == '__main__':
    main()