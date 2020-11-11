import requests
import sys

base_url = "https://api.trello.com/1/{}"
board_id = input("Enter the long boards ID: ")

auth_params = {
    'key': input("Enter your key for trello api: "),
    'token': input("Enter your token for trello api: ")
}

def read():
    """Read all info from board"""

    # request data about all columns
    columns_list = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # for each column, making request for task data
    for column in columns_list:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()

        # output format column name with number of tasks
        if len(task_data) == 0 or len(task_data) > 1:
            print('{}: {} tasks'.format(column['name'], len(task_data)))
        else:
            print('{}: {} task'.format(column['name'], len(task_data)))

        if not task_data:
            print('\tNo tasks')
            continue
        # Output format task, if tasks with name more than 1, then output with task id
        for task in task_data:
            if check_duplicates(task['name']):
                print('\t' + task['name'] + ', id: ' + task['id'])
            else:
                print('\t' + task['name'])


def check_column(column_name):
    """Check column"""

    # creating empty array for save columns names
    columns_name_list = []

    # request data about all columns
    columns_list = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # for each column save name in array
    for column in columns_list:
        columns_name_list.append(column['name'])

    if column_name in columns_name_list:
        return True
    else:
        return False


def create_column(column_name):
    """Create a new column with name "column_name"""
    if check_column(column_name):
        print('WARNING: Column with name \"{}\" is already exists'.format(column_name))
    else:
        requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': board_id, **auth_params})
        print("A new column has been created")


def delete_column(column_name):
    """Column delete"""
    # checking column name and if column is found, make request for columns data
    if check_column(column_name):
        columns_list = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
        # for each column, if name equal to "column_name", making request for delete this column
        for column in columns_list:
            if column['name'] == column_name:
                requests.put(base_url.format('lists') + '/' + column['id'] + '/closed', params={'value': 'true', **auth_params})
                print('Column \"{}\" was deleted'.format(column['name']))
                # after deleting, exit the loop with "break"
                break
    else: # if checking is False, then print message
        print('WARNING: Column with name \"{}\" does not exist'.format(column_name))


def create_task(task_name, column_name):
    """Create task with name task_name in column with name column_name"""
    # if a column with "column_name" is found
    if check_column(column_name):
        # request data about all columns
        columns_list = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
        # for each column, if name equal "column_name", making request for create a new task(card)
        for column in columns_list:
            if column['name'] == column_name:
                requests.post(base_url.format('cards'), data={'name': task_name, 'idList': column['id'], **auth_params})
                print('task \"{}\" create in column \"{}\"'.format(task_name, column_name))
    else:
        # create a new column
        create_column(column_name)
        # request data about all columns
        columns_list = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
        # for each column, if name equal "column_name", making request for create a new task(card)
        for column in columns_list:
            if column['name'] == column_name:
                requests.post(base_url.format('cards'), data={'name': task_name, 'idList': column['id'], **auth_params})
                print('task \"{}\" create in column \"{}\"'.format(task_name, column_name))


def check_duplicates(task_name):
    """check duplicates tasks"""
    # creating an empty array for storing task names
    task_names_list = []
    # creating a request for columns data
    columns_list = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # for each column, making request for tasks data and saving task_name in array
    for column in columns_list:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        if not task_data:
            continue
        for task in task_data:
            task_names_list.append(task['name'])
    # if task_name not in array, then output an error
    if task_name not in task_names_list:
        return "ERROR: Task not found"
    elif task_names_list.count(task_name) > 1:
        return True
    else:
        return False


def move(task_name, column_name):
    """Move the task with task_name in column with name column_name"""
    # if a column with "column_name" is found
    if check_column(column_name):
        if check_duplicates(task_name) == "ERROR: Task not found": # if task is not found
            print("ERROR: Task not found")
        elif check_duplicates(task_name): # if the name is not unique
            task_id = input("Enter task id: ") # user request for the task ID
            # creating a request for columns data
            columns_list = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
            # for each column making request for tasks data
            for column in columns_list:
                task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
                already = False # special boolean flag
                # for each task
                for task in task_data:
                    # if task already add in this column with column_name
                    if (task['name'] == task_name and task['id'] == task_id and column['name'] == column_name):
                        print('WARNING: Task \"{}\" already in this column \"{}\"'.format(task_name, column_name))
                        already = True
                # for each task
                for task in task_data:
                    # if column is found, then making request for update task data (move the task)
                    if column['name'] == column_name and not already:
                        requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
                        print('Task \"{}\" successfully move in column \"{}\"'.format(task_name, column_name))
                        # if moving is completed, then exit from cycle with "break"
                        break
        else: # if name is unique
            task_id = None
            # creating a request for columns data
            columns_list = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
            # for each column making request for tasks data
            for column in columns_list:
                task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
                # for each task
                for task in task_data:
                    # if the task alredy in this column, output message
                    if task['name'] == task_name:
                        if column['name'] == column_name:
                            print('WARNING: Task \"{}\" already in this column \"{}\"'.format(task_name, column_name))
                            break # exit from cycle
                        else:
                            task_id = task['id']
                            break
                if task_id:
                    break
            # if task id is received, for each column, on task ID making request for update task data(move the task)
            for column in columns_list:
                if column['name'] == column_name and task_id:
                    requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
                    print('Task \"{}\" successfully move in column \"{}\"'.format(task_name, column_name))
                    break
    else: # If the check failed
        print('\"Invalid value for column_name\"')


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create_task(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])
    elif sys.argv[1] == 'delete_column':
        delete_column(sys.argv[2])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])