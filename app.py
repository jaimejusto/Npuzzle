from flask import Flask, render_template, request, url_for, redirect
import json
import os
import puzzleEngine

# Configuration

app = Flask(__name__)
game = puzzleEngine.PuzzleGame()

def shuffle_board():
    game.new_game()

# Routes
@app.route('/', methods=['POST', 'GET'])
def root():
    if request.method == 'POST':
        if game.game_state == 'Not Solved':
            move = request.form['move']
            row_tile, col_tile = game.get_move(move)
            validity = game.verify_move(row_tile, col_tile)
            if validity is False:
                invalid_move_msg = "Move is invalid, please select a different tile."
                game_board = game.get_game_board()
                return render_template('main.j2', board=game_board, msg=invalid_move_msg)

            game.make_move(row_tile, col_tile)
            game_board = game.get_game_board()
            solved = game.verify_certificate()
            if solved:
                game.game_state = 'Solved'
                solved_msg = 'You solved the puzzle!'
                return render_template('main.j2', board=game_board, msg=solved_msg)

            return render_template('main.j2', board=game_board)
        if game_state == "Solved":
            solved_msg = 'You solved the puzzle!'
            return render_template('main.j2', board=game_board, msg=solved_msg)

    else:
        game_board = game.get_game_board()
        return render_template('main.j2', board=game_board)


@app.route('/newGame/')
def newGame():
    shuffle_board()
    return redirect(url_for('root'))

@app.route('/verify/', methods=['POST', 'GET'])
def verify():
    if request.method == 'POST':
        cert = request.form['cert']
        cert_list = list([int(val) for val in cert if val.isnumeric()])
        print(cert_list)
        results = game.verify_certificate(cert_list)
        return render_template('verify.j2', results=results)

    else:
        return render_template('verify.j2')


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 1738))     
    app.run(port=port, debug=True) 