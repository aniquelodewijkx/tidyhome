import random
import inquirer
import json

def get_names():
    answer = inquirer.prompt([inquirer.Text('num_players', message="How many players are there?")])
    num_players = int(answer["num_players"])
    questions = []
    for i in range(num_players):
        questions.append(inquirer.Text(f"player_name_{i+1}", message=f"Player #{i+1}"))

    names = inquirer.prompt(questions)
    return names

def get_task_categories():
    with open("tasks.json", "r") as f:
        task_categories = json.load(f)
    return task_categories

def get_task(all_categories: dict[str, list], category_selection: list[str]):
    possible_tasks = []
    for category, task_list in all_categories.items():
        if category in category_selection:
            possible_tasks.extend(task_list)
    return random.choice(possible_tasks)

if __name__ == '__main__':
    names = get_names()
    categories = get_task_categories()
    # task = get_task()

    # display all keys from the tasks.json and ask the user to deselect any they don't want:
    category_selection = inquirer.prompt(
        [inquirer.Checkbox('categories', message="Select all categories to include (Press <space> to select, Enter when finished).", choices=categories)]
    )

    for _, name in names.items():
        task = get_task(categories, category_selection["categories"])

        print(f"Task for {name}:")
        print(task, "\n")

