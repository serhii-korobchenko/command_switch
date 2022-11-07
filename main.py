from netmiko import ConnectHandler
import getpass
import sys

passwd = getpass.getpass('Будь ласка введіть пароль: ')

with open('multiple_sw_hp_ssh_devices.txt') as f:
    my_devices = f.read().splitlines()

device_list = list() #create an empty list to use it later

for device_ip in my_devices:
    device = {
        "device_type": "hp_comware",
        "host": device_ip,
        "username": "admin",
        "password": passwd,
        "secret": passwd
    }
    device_list.append(device)

with open('multiple_sw_hp_ssh_command.txt') as f:
    config_commands = f.read().splitlines()

try:
    operation_select = float(input("Виберіть дію яку необхідно виконати: \n"
                                   "1. Виконати скрипт без збереження конфігурації. \n"
                                   "2. Виконати скрипт та зберегти налаштування.\n"
                                   "3. Зберегти налаштування. \n\n"
                                   "Оберіть відповідний пункт меню (введіть порядковий номер меню):"))
except ValueError:
    print("Помилка: введіть будь-ласка число")
    sys.exit(1)

if 1 <= operation_select < 2:
    for each_device in device_list:
        connection = ConnectHandler(**each_device)
        connection.enable()
        print(f'Connecting to {each_device["host"]}')
        output = connection.send_config_set(config_commands)
        print(output)
        print(f'Closing Connection on {each_device["host"]}')
        connection.disconnect()
        print('-'*65)
elif 2  <=  operation_select < 3:
    for each_device in device_list:
        connection = ConnectHandler(**each_device)
        connection.enable()
        print(f'Connecting to {each_device["host"]}')
        output = connection.send_config_set(config_commands)
        print(output)
        connection.save_config()
        print('saving config...')
        print(f'Closing Connection on {each_device["host"]}')
        connection.disconnect()
        print('-'*65)
elif 3 <= operation_select < 4:
    for each_device in device_list:
        connection = ConnectHandler(**each_device)
        connection.enable()
        print(f'Connecting to {each_device["host"]}')
        connection.save_config()
        print('saving config...')
        print(f'Closing Connection on {each_device["host"]}')
        connection.disconnect()
        print('-'*65)
else:
    print("Ви ввели некоректне число меню!!!")
