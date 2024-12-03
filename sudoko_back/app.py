from flask import Flask, request, jsonify
from flask_cors import CORS
from sudoku_solver import SudokuSolver
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/solve', methods=['POST'])
def solve_sudoku():
    data = request.json
    grid = data.get('grid')
    algorithm = data.get('algorithm', 'backtracking')

    solver = SudokuSolver(grid)

    try:
        solved = solver.solve(algorithm)
        if solved:
            return jsonify({
                'success': True,
                'solution': solver.get_solution()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No solution found'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run()
