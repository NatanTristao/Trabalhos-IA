import random
from typing import Tuple, Iterable, Any
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

# ---------------------------- Helper utilities ----------------------------

def _extract_grid(state) -> list:
    """
    Retorna uma lista 8x8 (linhas) com caracteres ou strings representando células.
    Aceita um GameState ou um Board já.
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
                return [row[:8] for row in candidate[:8]]
        except Exception:
            pass
        raise AttributeError("Não foi possível extrair a grade do GameState/Board")

    processed = []
    for row in grid:
        if isinstance(row, str):
            processed.append(list(row[:8]))
        else:
            try:
                row_list = list(row)
                processed.append([row_list[i] if i < len(row_list) else '.' for i in range(min(8, len(row_list)))])
            except Exception:
                processed.append(['.'] * 8)

    processed8 = []
    for r in range(8):
        if r < len(processed):
            row = processed[r]
            row_s = [elem for elem in row]
            if len(row_s) < 8:
                row_s = row_s + ['.'] * (8 - len(row_s))
            else:
                row_s = row_s[:8]
        else:
            row_s = ['.'] * 8
        processed8.append(row_s)
    return processed8

def _normalize_cell(cell) -> str:
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
        if c in ('B', 'W'):
            return c
        return '.'

def make_move(state: GameState) -> Tuple[int, int]:
    """
    Retorna um movimento usando poda alfa-beta limitada em profundidade,
    avaliando com evaluate_count.
    Ajuste `max_depth` conforme seu limite de tempo (5s).
    """
    # profundidade padrão — ajuste conforme sua máquina/tempo.
    max_depth = 4
    move = minimax_move(state, max_depth, evaluate_count)
    if move is None:
        legal = state.legal_moves()
        return random.choice(legal) if legal else None
    return move

def evaluate_count(state: GameState, player: str) -> float:
    """
    Heurística simples: diferença entre a quantidade de peças do `player`
    e do oponente (player_count - opponent_count).
    Retorna SEMPRE a diferença numérica como float — mesmo para estados terminais,
    para ser compatível com os testes que esperam o valor numérico.
    """
    # tentar extrair grade robustamente
    try:
        grid = _extract_grid(state)
    except Exception:
        if hasattr(state, "counts") and callable(getattr(state, "counts")):
            counts = state.counts()
            opponent = "B" if player == "W" else "W"
            if isinstance(counts, dict):
                return float(counts.get(player, 0) - counts.get(opponent, 0))
        return 0.0

    p = player.upper()
    opp = "B" if p == "W" else "W"

    p_count = 0
    o_count = 0
    for row in grid:
        for cell in row:
            c = _normalize_cell(cell)
            if c == p:
                p_count += 1
            elif c == opp:
                o_count += 1

    return float(p_count - o_count)
