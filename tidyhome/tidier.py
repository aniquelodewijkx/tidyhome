import random
import inquirer
import pandas as pd
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
    with importlib.resources.open_text("tidyhome", "task_completions.csv") as f:
        tasks_df = pd.read_csv(f)

    tasks_df["frequency"] = pd.to_timedelta(tasks_df["frequency"])
    tasks_df["last_completed"] = pd.to_datetime(tasks_df["last_completed"])

    categories = tasks_df["category"].unique().tolist()
    category_selection = inquirer.prompt(
        [inquirer.Checkbox('categories',
                           message="What's getting tidied today? \n(select: <space>, finish: <enter>)",
                           choices=categories)]
    )["categories"]

    possible_tasks = []
    for tasks, category, frequency, last_completed in zip(tasks_df["task"], tasks_df["category"], tasks_df["frequency"], tasks_df["last_completed"]):
        if category in category_selection:
            if pd.Timestamp.now() - last_completed >= frequency:
                possible_tasks.append(tasks)

    if possible_tasks is None:
        print("All tasks in categories selected have been completed recently. Exiting.")
        return None

    return possible_tasks


def assign_tasks(names, tasks) -> list[str]:
    max_length = max(len(word) for word in tasks)

    given_tasks = []
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
        given_tasks.append(task)
        tasks.remove(task)

    return given_tasks

def update_task_completion_dates(completed_tasks):
    with importlib.resources.files(tidyhome).joinpath("task_completions.csv").open("r") as f:
        tasks_df = pd.read_csv(f)

    for task in completed_tasks:
        tasks_df.loc[tasks_df["task"] == task, "last_completed"] = pd.Timestamp.now()

    with importlib.resources.files(tidyhome).joinpath("task_completions.csv").open("w") as f:
        tasks_df.to_csv(f, index=False)


def main():
    # parser = argparse.ArgumentParser(description="A random task assignment tool for tidying up your home")

    names = get_names()
    tasks = get_tasks()

    if tasks is None:
        exit(0)

    completed_tasks = []
    while tasks:
        given_tasks = assign_tasks(names, tasks)
        if not tasks:
            print("All tasks have been assigned. Exiting.")
            break
        completed_prompt = inquirer.prompt(
            [inquirer.Checkbox('completed',
                               message="Which tasks were completed?",
                               choices=given_tasks)])
        for completed_task in completed_prompt['completed']:
            completed_tasks.append(completed_task)
        continue_prompt = inquirer.prompt(
            [inquirer.Confirm('continue', message="Do you want to continue assigning tasks?", default=True)])
        if not continue_prompt['continue']:
            print(f"Congratulations! You completed {len(completed_tasks)} today.")
            break

    update_task_completion_dates(completed_tasks)


if __name__ == '__main__':
    main()