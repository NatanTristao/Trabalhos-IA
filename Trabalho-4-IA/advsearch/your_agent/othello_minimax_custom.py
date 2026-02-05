import random
from typing import Tuple, List, Iterable, Optional, Any
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

EVAL_TEMPLATE = [
    [100, -30, 6, 2, 2, 6, -30, 100],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [6, 1, 1, 1, 1, 1, 1, 6],
    [2, 1, 1, 3, 3, 1, 1, 2],
    [2, 1, 1, 3, 3, 1, 1, 2],
    [6, 1, 1, 1, 1, 1, 1, 6],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [100, -30, 6, 2, 2, 6, -30, 100]
]

def _is_grid_like(obj: Any) -> bool:
    try:
        if not isinstance(obj, (list, tuple)):
            return False
        if len(obj) < 1:
            return False
        for row in obj:
            if not isinstance(row, (list, tuple, str)):
                return False
            if len(row) < 1:
                return False
        return True
    except Exception:
        return False

def _normalize_grid_obj(obj: Any) -> List[List[str]]:
    processed = []
    for row in obj:
        if isinstance(row, str):
            processed.append(list(row))
        else:
            processed.append([str(cell) for cell in row])
    return processed

def _find_board_in_object(obj: Any, depth: int = 2) -> Optional[List[List[str]]]:
    if depth < 0 or obj is None:
        return None

    if _is_grid_like(obj):
        return _normalize_grid_obj(obj)

    attrs_to_try = ("board", "grid", "state", "position", "board_state", "game_state")
    for attr in attrs_to_try:
        try:
            val = getattr(obj, attr, None)
            if val is not None:
                if _is_grid_like(val):
                    return _normalize_grid_obj(val)
                if hasattr(val, "board") or hasattr(val, "grid"):
                    inner = getattr(val, "board", None) or getattr(val, "grid", None)
                    if inner is not None and _is_grid_like(inner):
                        return _normalize_grid_obj(inner)
        except Exception:
            pass

    if isinstance(obj, dict):
        for v in obj.values():
            try:
                res = _find_board_in_object(v, depth - 1)
                if res is not None:
                    return res
            except Exception:
                pass

    try:
        if hasattr(obj, "__dict__"):
            for k, v in vars(obj).items():
                try:
                    if _is_grid_like(v):
                        return _normalize_grid_obj(v)
                    res = _find_board_in_object(v, depth - 1)
                    if res is not None:
                        return res
                except Exception:
                    pass
    except Exception:
        pass

    try:
        s = str(obj)
        lines = [line.rstrip() for line in s.splitlines() if line.strip()]
        candidate = [list(line) for line in lines if len(line) >= 8]
        if len(candidate) >= 8:
            return candidate[:8]
    except Exception:
        pass

    return None

def _extract_grid(state: Any) -> List[List[str]]:
    if state is None:
        return [["."] * 8 for _ in range(8)]

    try:
        if _is_grid_like(state):
            return _normalize_grid_obj(state)
    except Exception:
        pass

    try:
        b = getattr(state, "board", None)
        if b is not None:
            if _is_grid_like(b):
                return _normalize_grid_obj(b)
            inner = getattr(b, "board", None) or getattr(b, "grid", None)
            if inner is not None and _is_grid_like(inner):
                return _normalize_grid_obj(inner)
    except Exception:
        pass

    try:
        g = getattr(state, "grid", None)
        if g is not None and _is_grid_like(g):
            return _normalize_grid_obj(g)
    except Exception:
        pass

    try:
        found = _find_board_in_object(state, depth=3)
        if found is not None:
            return found
    except Exception:
        pass

    try:
        print("WARNING: não foi possível extrair grade do state passado ao evaluate; usando grade vazia.")
    except Exception:
        pass
    return [["."] * 8 for _ in range(8)]

def _normalize_cell(cell: object) -> str:
    if cell is None:
        return "."
    s = str(cell).strip()
    if not s:
        return "."
    s_up = s.upper()
    if s_up.startswith("B"):
        return "B"
    if s_up.startswith("W"):
        return "W"
    if s in ("0", ".", "-", "_"):
        return "."
    try:
        v = float(s)
        if v == 0:
            return "."
        return "B" if v > 0 else "W"
    except Exception:
        pass
    c = s_up[0]
    if c in ("B", "W"):
        return c
    return "."

def _ensure_legal_list(lm: Optional[Iterable]) -> List:
    if lm is None:
        return []
    if isinstance(lm, (list, tuple)):
        return list(lm)
    try:
        return list(lm)
    except Exception:
        return [lm]

def _frontier_count(grid: List[List[str]], player: str) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    f = 0
    for r in range(rows):
        for c in range(cols):
            if _normalize_cell(grid[r][c]) != player:
                continue
            for dr,dc in dirs:
                rr, cc = r+dr, c+dc
                if 0 <= rr < rows and 0 <= cc < cols:
                    if _normalize_cell(grid[rr][cc]) == ".":
                        f += 1
                        break
    return f

def _positional_score(grid: List[List[str]], player: str) -> float:
    score = 0.0
    rows = min(len(grid), 8)
    for r in range(rows):
        for c in range(min(len(grid[r]), 8)):
            cell = _normalize_cell(grid[r][c])
            val = EVAL_TEMPLATE[r][c]
            if cell == player:
                score += val
            elif cell == ("B" if player == "W" else "W"):
                score -= val
    return score

def evaluate_custom(state, player: str) -> float:
    """
    Heurística combinada.
    """
    try:
        if getattr(state, "is_terminal", lambda: False)():
            util = getattr(state, "utility", None)
            if callable(util):
                try:
                    return float(util(player))
                except TypeError:
                    try:
                        return float(util())
                    except Exception:
                        pass
    except Exception:
        pass

    grid = _extract_grid(state)
    p = (player or "B").upper()
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
    total = p_count + o_count

    piece_diff = 0.0
    if total > 0:
        piece_diff = 100.0 * (p_count - o_count) / total

    try:
        my_moves = len(_ensure_legal_list(state.legal_moves()))
    except Exception:
        my_moves = 0
    try:
        opp_moves = 0
        try:
            opp_moves = len(_ensure_legal_list(state.legal_moves(opp)))
        except TypeError:
            try:
                copy = state.copy()
                if hasattr(copy, "player"):
                    copy.player = opp
                elif hasattr(copy, "to_move"):
                    copy.to_move = opp
                opp_moves = len(_ensure_legal_list(copy.legal_moves()))
            except Exception:
                opp_moves = 0
    except Exception:
        opp_moves = 0

    mobility = 0.0
    if (my_moves + opp_moves) > 0:
        mobility = 100.0 * (my_moves - opp_moves) / (my_moves + opp_moves)

    corners = [(0,0),(0,7),(7,0),(7,7)]
    corner_score = 0
    rows = len(grid)
    cols = len(grid[0]) if rows>0 else 0
    for (r,c) in corners:
        if 0 <= r < rows and 0 <= c < cols:
            cell = _normalize_cell(grid[r][c])
            if cell == p:
                corner_score += 25
            elif cell == opp:
                corner_score -= 25

    precorner_pos = [(0,1),(1,0),(1,1),(0,6),(1,7),(1,6),(6,0),(7,1),(6,1),(6,6),(6,7),(7,6)]
    prec = 0
    for (r,c) in precorner_pos:
        if 0 <= r < rows and 0 <= c < cols:
            cell = _normalize_cell(grid[r][c])
            if cell == p:
                prec -= 8
            elif cell == opp:
                prec += 8

    p_frontier = _frontier_count(grid, p)
    o_frontier = _frontier_count(grid, opp)
    frontier = 0.0
    if (p_frontier + o_frontier) > 0:
        frontier = 100.0 * (o_frontier - p_frontier) / (p_frontier + o_frontier)

    positional = _positional_score(grid, p)

    if total <= 20:
        w_piece = 0.6
        w_mob = 2.0
        w_corner = 3.0
        w_prec = -1.5
        w_front = 0.8
        w_pos = 1.5
    elif total <= 58:
        w_piece = 1.0
        w_mob = 1.5
        w_corner = 4.0
        w_prec = -2.0
        w_front = 1.0
        w_pos = 1.2
    else:
        w_piece = 3.0
        w_mob = 0.8
        w_corner = 5.0
        w_prec = -2.5
        w_front = 0.6
        w_pos = 0.8

    score = (
        w_piece * piece_diff +
        w_mob * mobility +
        w_corner * corner_score +
        w_prec * prec +
        w_front * frontier +
        w_pos * positional
    )

    try:
        return float(score)
    except Exception:
        return 0.0

def make_move(state) -> Tuple[int, int]:
    """
    Chama minimax_move com evaluate_custom.
    """
    legal = _ensure_legal_list(state.legal_moves() if hasattr(state, "legal_moves") else None)
    n_legal = len(legal)

    if n_legal >= 20:
        max_depth = 3
    elif n_legal >= 10:
        max_depth = 4
    else:
        max_depth = 5

    move = None
    try:
        move = minimax_move(state, max_depth, evaluate_custom)
    except TypeError:
        try:
            move = minimax_move(state, evaluate_custom, max_depth)
        except Exception:
            move = None
    except Exception:
        move = None

    if move is None and legal:
        return random.choice(legal)
    return move
