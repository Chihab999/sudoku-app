'use client'
import React, { useState } from 'react';

const SudokuSolver = () => {
  const [grid, setGrid] = useState(Array(9).fill(0).map(() => Array(9).fill(0)));
  const [solution, setSolution] = useState<number[][] | null>(null);
  const [algorithm, setAlgorithm] = useState('backtracking');
  const [error, setError] = useState(null);

  const updateCell = (row : any, col : any, value : any) => {
    const newGrid = [...grid];
    newGrid[row][col] = value === '' ? 0 : parseInt(value);
    setGrid(newGrid);
  };

  const solveSudoku = async () => {
    try {
      const response = await fetch('http://localhost:5000/solve', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          grid: grid,
          algorithm: algorithm 
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to solve Sudoku');
      }

      const data = await response.json();
      setSolution(data.solution);
      setError(null);
    } catch (error : any) {
      console.error('Error solving Sudoku:', error);
      setError(error.message);
      setSolution(null);
    }
  };

  const clearGrid = () => {
    setGrid(Array(9).fill(0).map(() => Array(9).fill(0)));
    setSolution(null);
    setError(null);
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Sudoku Solver</h1>
      
      {/* Sudoku Grid */}
      <div className="grid grid-cols-9 gap-1 mb-4">
        {grid.map((row : any , rowIndex : any) => 
          row.map((cell : any, colIndex : any) => (
            <input
              key={`${rowIndex }-${colIndex}`}
              type="number"
              min="0"
              max="9"
              value={cell || ''}
              onChange={(e) => updateCell(rowIndex, colIndex, e.target.value)}
              className="w-10 h-10 text-center border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          ))
        )}
      </div>

      {/* Algorithm Selection */}
      <div className="mb-4">
        <label className="block mb-2">Select Solving Algorithm:</label>
        <select 
          value={algorithm} 
          onChange={(e) => setAlgorithm(e.target.value)}
          className="w-full p-2 border rounded"
        >
          <option value="backtracking">Backtracking</option>
          <option value="bfs">Breadth-First Search (BFS)</option>
          <option value="dfs">Depth-First Search (DFS)</option>
        </select>
      </div>

      {/* Error Handling */}
      {error && (
        <div className="mb-4 p-2 bg-red-100 text-red-800 rounded">
          {error}
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex space-x-2">
        <button 
          onClick={solveSudoku}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Solve Sudoku
        </button>
        <button 
          onClick={clearGrid}
          className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300"
        >
          Clear Grid
        </button>
      </div>

      {/* Solution Display */}
      {solution && (
        <div className="mt-4">
          <h2 className="text-xl font-semibold mb-2">Solution:</h2>
          <div className="grid grid-cols-9 gap-1">
            {solution.map((row : any, rowIndex : any) => 
              row.map((cell : any, colIndex : any) => (
                <div
                  key={`${rowIndex}-${colIndex}`}
                  className="w-10 h-10 text-center border border-gray-300 bg-green-100"
                >
                  {cell}
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default SudokuSolver;