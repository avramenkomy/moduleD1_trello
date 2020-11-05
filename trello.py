import requests
import sys

board_id = "jCEgeWu0"
base_url = "https://api.trello.com/1/{}"

auth_params = {
    'key': "021c7dc68cbd97c821e04a48c67ef606",
    'token': "ee226fc53f65aadb337c6779ec77e0f3775bee5f20656115dd7de937ecfcb379"
}
def read():
    '''Вывод данных колонок на экран'''

    #Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    #Выведем название каждой колонки и все задачи в ней
    for column in column_data:
        print(column['name'])

        #Получим данные всех задач в колонке и выведем их названия
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        if not task_data:
            print('\t' + "Нет задач")
            continue
        for task in task_data:
            print('\t' + task['name'])

def create(task_name, column_name):
    '''Создание задачи task_name в колонке column_name'''

    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    #Переберем все колонки пока не найдем нужную
    for column in column_data:
        if column['name'] == column_name:
            #Создадим задачу методом post и именем task_name в найденной колонке
            requests.post(base_url.format('cards'), data = {
                'name': task_name,
                'idList': column['id'],
                **auth_params
            })
            print("Задача " + task_name +  " добавлена в " + column_name)
            break

def move(task_name, column_name):
    '''Перемещение задачи task_name в колонку column_name'''

    #Получаем данные всех колонок
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    #Среди всех колонок ищем задачу по имени и получаем ее id
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == task_name:
                task_id = task['id']
                break
        if task_id:
            break
    #Теперь у нас есть id задачи, которую нужно переместить, переберем все колонки,
    #пока не найдем ту, в которую нужно переместить найденную задачу
    for column in column_data:
        if column['name'] == column_name:
            #Выполним запрос к API на перемещение задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id + '/idList',
                         data = {
                             'value': column['id'],
                             **auth_params
                         })

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])