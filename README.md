# Echo-Server
Echo server capble handling multiple clients and with special commands, clients have gui. In python.

![image](https://github.com/Ultiboty/Echo-Server/assets/99267952/1bb6589b-745a-4594-a316-690322768453)


## Requirements
The app requires Python 3+ and the following libraries:
*scapy
*socket
*threading
*tkinter
*time
*select
*random
*string

Additionally, the app requires the following files:
*client.py: the client-side code
*server.py: the server-side code

## Usage
To use the chat room app, follow these steps:

1. Ensure that Python and the required libraries are installed on your machine.
2. Download the client.py, server.py files.
3. Open a command prompt or terminal and navigate to the directory where the files are located.
4. Run the server.py file by typing "python server.py" and pressing enter.
5. Open a new terminal window or run the client.py file on a different computer.
6. Run the client.py file by typing "python client.py" and pressing enter.
7. Begin communicating with other users within the session.

Note: If you want to run multiple clients on the same machine, each client must be run in a separate terminal window.

## Commands
The client have several commands that he can send to the server
1. "exit"- disconnecting the user.
2. "quit-password"- shutting server down and all users connected.
3. "Missions" - Sends a random mission for life improvement.
4. "Time" - Sends the current server time.
5. "People" - Sends the amount of people currently connected to the server.
6. "Run time" - Sends how long the server has been running.
