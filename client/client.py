import socket
import ssl
import PySimpleGUI as sg

SERVER_HOST = ""
SERVER_PORT = 0

HOST = "127.0.0.1"
PORT = 60002

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

client = ssl.wrap_socket(client, keyfile="ssl\key.pem", certfile="ssl\certificate.pem")

#GUI layout
sg.change_look_and_feel('DarkBlue')
main_layout = [
    [sg.Text('Please enter the message you want to send: ')],
    [sg.Text("Message", size = (15,1)),sg.InputText(key="-CLIENT_MESSAGE-")],
    [sg.Text("")],
    [sg.Text("")],
    [sg.Button("Submit", bind_return_key=True), sg.Exit()]
]

port_layout = [
    [sg.Text('Please input the server HostIP and Port')],
    [sg.Text('HOST IP', size = (15,1)), sg.InputText(key = "-HOST_IP-")],
    [sg.Text('PORT', size = (15,1)), sg.InputText(key = "-PORT-")],
    [sg.Text("")],
    [sg.Button("Submit"), sg.Exit()]
]

window = sg.Window('Client Message', main_layout, size=(600,150), return_keyboard_events=True, use_default_focus=False)
port_window = sg.Window('Connection Configuration', port_layout, size=(600,150))


event1, values1 = port_window.read()

if event1 in (sg.WIN_CLOSED, 'Exit'):
    port_window.close()
    quit()
elif event1 == "Submit":
    SERVER_HOST = str(values1["-HOST_IP-"])
    SERVER_PORT = int(values1["-PORT-"])
    print (SERVER_HOST,SERVER_PORT)

if __name__ == "__main__":  
    client.bind((HOST, PORT))
    client.connect((SERVER_HOST, SERVER_PORT))
    port_window.hide()
    
    while True:
        from time import sleep
        if event1 == "Submit":
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            elif event == "Submit":
                message = values["-CLIENT_MESSAGE-"]
                if not message:
                    client.send(" ".encode("utf-8"))
                else:
                    client.send(message.encode("utf-8"))
                    sleep(1)