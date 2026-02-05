import random
from typing import Tuple, List
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

# ---------------------------- Ajudantes ----------------------------

# helper robusto para extrair a grade do estado/board
def _extract_grid(state):
    """
    Retorna uma lista de 8 listas (linhas) com caracteres 'B','W','.'.
    Aceita receber um GameState ou um Board diretamente.
    """
    board_obj = getattr(state, "board", state)

    grid = None
    if hasattr(board_obj, "board"):
        grid = getattr(board_obj, "board")
    elif hasattr(board_obj, "grid"):
        grid = getattr(board_obj, "grid")
    else:
        try:
            grid = list(board_obj)
        except Exception:
            grid = None

    if grid is None:
        try:
            s = str(board_obj)
            lines = [line.rstrip() for line in s.splitlines() if line.strip()]
            candidate = [list(line) for line in lines if len(line) >= 1]
            if len(candidate) >= 8:
                return [ [c for c in row[:8]] for row in candidate[:8] ]
        except Exception:
            pass
        raise AttributeError("Could not extract board grid from GameState/Board object")

    processed = []
    for row in grid:
        if isinstance(row, str):
            processed.append(list(row[:8]))
        else:
            # row pode ser um iterável de células; converter cada célula para string e pegar 1º caractere
            processed.append([str(cell)[0] if len(str(cell))>0 else '.' for cell in list(row)[:8]])
    processed8 = []
    for r in range(8):
        if r < len(processed):
            row = processed[r]
            if len(row) < 8:
                row = row + ['.'] * (8 - len(row))
            else:
                row = row[:8]
        else:
            row = ['.'] * 8
        processed8.append(row)
    return processed8

def _normalize_cell(cell):
    if cell is None:
        return '.'
    s = str(cell).strip()
    if s == '' or s in ('.', '-', '_', '0'):
        return '.'
    s_up = s.upper()
    if s_up[0] == 'B':
        return 'B'
    if s_up[0] == 'W':
        return 'W'
    try:
        v = float(s)
        if v == 0:
            return '.'
        return 'B' if v > 0 else 'W'
    except Exception:
        c = s_up[0]
        if c in ('B','W'):
            return c
        return '.'

# ---------------------------- MASK HEURISTIC ----------------------------

# mask template adjusted from https://web.fe.up.pt/~eol/IA/MIA0203/trabalhos/Damas_Othelo/Docs/Eval.html
# DO NOT CHANGE!
EVAL_TEMPLATE = [
    [100, -30, 6, 2, 2, 6, -30, 100],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [100, -30, 6, 2, 2, 6, -30, 100]
]


def make_move(state) -> Tuple[int, int]:
    legal = state.legal_moves()
    n = len(legal) if legal is not None else 0
    if n >= 20:
        max_depth = 3
    elif n >= 10:
        max_depth = 4
    else:
        max_depth = 5

    move = minimax_move(state, max_depth, evaluate_mask)
    return move


def evaluate_mask(state: GameState, player: str) -> float:
    """Evaluate by summing positional values from EVAL_TEMPLATE for player minus opponent.
    If the state is terminal, returns the piece-difference utility (consistent with evaluate_count).
    """
    # If a dedicated utility exists, prefer to use it for terminal states
    try:
        util = getattr(state, "utility", None)
        if callable(util) and state.is_terminal():
            try:
                return float(util(player))
            except TypeError:
                return float(util())
    except Exception:
        pass

    grid = _extract_grid(state)
    p = player.upper()
    opp = "B" if p == "W" else "W"

    rows = min(len(grid), 8)
    cols = 8
    score_p = 0.0
    score_o = 0.0

    for r in range(rows):
        row = grid[r]
        for c in range(min(len(row), cols)):
            cell = _normalize_cell(row[c])
            val = EVAL_TEMPLATE[r][c]
            if cell == p:
                score_p += val
            elif cell == opp:
                score_o += val

    return float(score_p - score_o)
