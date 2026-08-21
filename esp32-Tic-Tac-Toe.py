import socket
import time
from network import WLAN # type: ignore
import time
import gc


# Turn on WiFi AP
ap = WLAN(WLAN.IF_AP)
ap.active(False)
time.sleep(1)
ap.active(True)
ap.config(essid="test")

board = ["⬜"] * 9

#socket info ip adress of server and port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("192.168.4.1", 8080))
s.listen(2)
print("Server working, Go to http://192.168.4.1:8080 to test")

#Board for visual and for server
def print_board():
    print(board[0], board[1], board[2])
    print(board[3], board[4], board[5])
    print(board[6], board[7], board[8])
    
#check win on server board player1
def check_win_p1():
    if ((board[0] == "❌" and board[1] == "❌" and board[2] == "❌")
        or (board[3] == "❌" and board[4] == "❌" and board[5] == "❌")
        or (board[6] == "❌" and board[7] == "❌" and board[8] == "❌")
        or (board[0] == "❌" and board[3] == "❌" and board[6] == "❌")
        or (board[1] == "❌" and board[4] == "❌" and board[7] == "❌")
        or (board[2] == "❌" and board[5] == "❌" and board[8] == "❌")
        or (board[0] == "❌" and board[4] == "❌" and board[8] == "❌")
        or (board[2] == "❌" and board[4] == "❌" and board[6] == "❌")):
        print("player1 wins")
        return True 
    return False

#check win on server board player2
def check_win_p2():
    if ((board[0] == "⭕" and board[1] == "⭕" and board[2] == "⭕")
        or (board[3] == "⭕" and board[4] == "⭕" and board[5] == "⭕")
        or (board[6] == "⭕" and board[7] == "⭕" and board[8] == "⭕")
        or (board[0] == "⭕" and board[3] == "⭕" and board[6] == "⭕")
        or (board[1] == "⭕" and board[4] == "⭕" and board[7] == "⭕")
        or (board[2] == "⭕" and board[5] == "⭕" and board[8] == "⭕")
        or (board[0] == "⭕" and board[4] == "⭕" and board[8] == "⭕")
        or (board[2] == "⭕" and board[4] == "⭕" and board[6] == "⭕")):
        print("player2 wins")
        return True 
    return False

#html pages, this one is actual board
html_page = """<div class="game-wrapper">
  <h1>Tic-Tac-Toe</h1>
  <div id="status-text" style="margin-bottom: 15px; font-weight: bold; font-size: 1.2rem; color: #333;">Connecting...</div>
  <div class="grid">
      <div class="thic-board">
          <button type="button" data-cell="0" class="btn">_</button>
          <button type="button" data-cell="1" class="btn">_</button>
          <button type="button" data-cell="2" class="btn">_</button><br>
          <button type="button" data-cell="3" class="btn">_</button>
          <button type="button" data-cell="4" class="btn">_</button>
          <button type="button" data-cell="5" class="btn">_</button><br>
          <button type="button" data-cell="6" class="btn">_</button>
          <button type="button" data-cell="7" class="btn">_</button>
          <button type="button" data-cell="8" class="btn">_</button>
      </div>
  </div>
  <button id="reset-btn" type="button" style="margin-top: 15px; padding: 10px 20px; font-size: 1rem; cursor: pointer;">Play Again</button>
</div>"""


waiting_lob = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tic-Tac-Toe Lobby</title>
    <style>
      body {
        font-family: system-ui, -apple-system, sans-serif;
        text-align: center;
        background-color: #f0f0f0;
        margin-top: 50px;
      }
      .btn {
        width: 80px;
        height: 80px;
        font-size: 28px;
        font-weight: bold;
        margin: 4px;
        cursor: pointer;
      }
      .thic-board {
        margin: 20px auto;
      }
    </style>
  </head>
  <body>
    <div id="game-container">
      <h1>Tic-Tac-Toe</h1>
      <h2>Waiting for second player to join...</h2>
    </div>

    <script>
      let playerId = null;

      function joinGame() {
        fetch('/join')
          .then(res => res.text())
          .then(id => {
            playerId = id.trim();
            checkLobbyStatus();
          })
          .catch(() => setTimeout(joinGame, 1000));
      }

      function checkLobbyStatus() {
        fetch('/is-game-ready')
          .then(res => {
            if (res.ok) {
              loadRealSite();
            } else {
              setTimeout(checkLobbyStatus, 1000);
            }
          })
          .catch(() => setTimeout(checkLobbyStatus, 1000));
      }

      function loadRealSite() {
        fetch('/get-board')
          .then(res => res.text())
          .then(gameHtml => {
            // Swap lobby for board layout
            document.getElementById('game-container').innerHTML = gameHtml;
            document.body.style.backgroundColor = "#ffffff";

            // Board click handlers
            document.querySelectorAll('.btn').forEach(button => {
              button.addEventListener('click', function(event) {
                event.preventDefault(); 
                if (this.innerText.trim() !== '_' && this.innerText.trim() !== '') return;

                let cellIndex = this.getAttribute('data-cell');

                fetch('/send-data', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                  body: 'player=' + playerId + '&input_x_y=' + cellIndex
                })
                .then(response => response.text())
                .then(textFromPython => {
                  let resText = textFromPython.trim();
                  if (resText === 'X' || resText === 'O') {
                    this.innerText = resText;
                  }
                });
              });
            });

            // Reset button listener
            let resetBtn = document.getElementById('reset-btn');
            if (resetBtn) {
              resetBtn.addEventListener('click', function() {
                fetch('/reset')
                  .then(res => res.text())
                  .then(status => {
                    if (status.trim() === 'RESET_OK') {
                      location.reload();
                    } else {
                      alert('Can only reset when board is full or game is over!');
                    }
                  });
              });
            }

            // Start move polling after DOM nodes are injected
            startMoveSync();
          });
      }

      function startMoveSync() {
        setInterval(() => {
          fetch('/get-last-move')
            .then(res => res.text())
            .then(data => {
              let trimmedData = data.trim();
              if (trimmedData && trimmedData.includes(',')) {
                let parts = trimmedData.split(',');
                let cellIndex = parts[0];
                let symbol = parts[1];
                let state = parts[2];
                let turn = parts[3];

                // Update board square
                if (cellIndex !== 'None') {
                  let targetBtn = document.querySelector('.btn[data-cell="' + cellIndex + '"]');
                  if (targetBtn && symbol) {
                    targetBtn.innerText = symbol;
                  }
                }

                // Safely update status text element
                let statusText = document.getElementById('status-text');
                if (statusText) {
                  if (state === 'WIN_P1') {
                    statusText.innerText = '🏆 Player 1 Wins!';
                  } else if (state === 'WIN_P2') {
                    statusText.innerText = '🏆 Player 2 Wins!';
                  } else if (state === 'DRAW') {
                    statusText.innerText = '🤝 Game Draw!';
                  } else {
                    statusText.innerText = (turn === playerId) ? 'Your Turn!' : "Opponent's Turn...";
                  }
                }
              }
            })
            .catch(() => {});
        }, 1000);
      }

      joinGame();
    </script>
  </body>
</html>"""


def reset_game():
    global board, current_turn, last_move_symbole, last_move_cell, game_state
    board = ["⬜"] * 9 
    current_turn = "player1"
    last_move_cell= None
    last_move_symbole= None
    game_state = "PLAYING"
    print("Server Game Reset")

def is_board_full():
    return "⬜" not in board
                
def place_player1(cords_x):
    print("cords enterd player1")
    if board[cords_x] == "⬜":
        board[cords_x] = "❌" 
        return True
    else:
        print("Cannot place it there, try again")  

def place_player2(cords_o):
    print("cords entered player2")
    if board[cords_o] == "⬜":
        board[cords_o] = "⭕"
        return True
    else:
        print("Cannot place it there, try again!")
        
# data for socket and more
connected_ip = []
number_of_board_from_website= []
p1_waiting_socket = None
#Global variables
current_turn = "player1"
last_move_symbole=None
last_move_cell= None
game_state = "PLAYING"
board = ["⬜"] * 9

#while true loop runs server and game
while True:
    conn = None
    try:
        conn, addr = s.accept()
        ip = addr[0]

        request = conn.recv(1024)

        request_decode = request.decode("utf-8")

        # Initial connection
        if "GET / " in request_decode or "GET /index" in request_decode:
            if ip not in connected_ip:
                if len(connected_ip) < 2:
                    connected_ip.append(ip)
                    print("Connection, IP:", ip)
                else:
                    conn.send(b"HTTP/1.1 503 Service Unavailable\r\nConnection: close\r\n\r\n<h1>Game Full!</h1>")
                    conn.close()
                    continue

            response = ("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n"+ waiting_lob)
            conn.send(response.encode("utf-8"))
            conn.close()
            
        #unique ids player 1 and two based on who connectes
        elif "/join" in request_decode:
            if len(connected_ip) == 1:
                conn.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\nplayer1")
                conn.close()
                print("Player1")
            elif len(connected_ip) == 2:
                conn.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\nplayer2")
                conn.close()
                print('Player2')

        # Handle lobby status polling
        elif "/is-game-ready" in request_decode:
            if len(connected_ip) < 2:
                p1_waiting_socket = conn
            else:
                conn.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nREADY")
                conn.close()

                if p1_waiting_socket:
                    p1_waiting_socket.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nREADY")
                    p1_waiting_socket.close()
                    p1_waiting_socket = None

        # Handle board request
        elif "/get-board" in request_decode:
            print("Player1 and 2 are recieving the final html")
            response = ("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n"+ html_page)
            conn.send(response.encode("utf-8"))
            conn.close()

        # Handle move
        elif "POST" in request_decode:
            # Extract cell index from request
            if "player=player1" in request_decode:
                number_of_board_from_website = request_decode.split("input_x_y=")
                print(number_of_board_from_website[1])
                if current_turn == "player1":
                    if place_player1(int(number_of_board_from_website[1])):
                        last_move_cell = number_of_board_from_website[1]
                        move_val = "X"
                        last_move_symbole="X"
                        current_turn = "player2"
                        print("----------")
                        print_board()
                        print("----------")
                        if check_win_p1():
                            game_state = "WIN_P1"
                        elif is_board_full():
                            game_state= "DRAW"
                        else:
                            game_state= "PLAYING"
                    else:
                        move_val ="WAIT"
                else:
                    move_val = "WAIT"
                #send cell X too player1 or wait
                response = ("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\n"+ move_val)
                conn.send(response.encode("utf-8"))
                conn.close()
            else:
                number_of_board_from_website = request_decode.split("input_x_y=")
                print(number_of_board_from_website[1])
                if current_turn == "player2":
                    if place_player2(int(number_of_board_from_website[1])) is True:
                        last_move_cell = number_of_board_from_website[1]
                        move_val = "O"
                        last_move_symbole = "O"
                        current_turn="player1"
                        print("----------")
                        print_board()
                        print("----------")
                        if check_win_p2():
                            game_state = "WIN_P2"
                        elif is_board_full():
                            game_state= "DRAW"
                        else:
                            game_state= "PLAYING"
                    else:
                        move_val="WAIT"
                else:
                    move_val="WAIT"
                #send cell O too player2 or wait
                response = ("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\n"+ move_val)
                conn.send(response.encode("utf-8"))
                conn.close()
                
        elif "/get-last-move" in request_decode:
            body = f"{last_move_cell},{last_move_symbole},{game_state},{current_turn}"
            response=("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\n"+ body)
            conn.send(response.encode("utf-8"))
            conn.close()


        elif "/reset" in request_decode:
            if is_board_full() or game_state != "PLAYING":
                reset_game()
                msg = "RESET_OK"
            else:
                msg = "NOT_FULL"
            response=("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\n"+ msg)
            conn.send(response.encode("utf-8"))
            conn.close()

        gc.collect()

    except OSError as e:
        print("Socket error:", e)
        if conn:
            conn.close()
