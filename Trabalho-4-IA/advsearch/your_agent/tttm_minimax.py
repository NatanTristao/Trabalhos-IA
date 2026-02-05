import random
from typing import Tuple, List, Optional
from ..tttm.gamestate import GameState
from ..tttm.board import Board
from .minimax import minimax_move

# ----------------- Ajudantes -----------------

def _extract_ttt_grid(state) -> List[List[str]]:
    """
    Extrai a grade 3x3 com valores normalizados 'X','O' ou '.'.
    """
    board_obj = getattr(state, "board", state)

    # tentar atributos comuns
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
            lines = [line.strip() for line in s.splitlines() if line.strip()]
            candidate = [list(line) for line in lines if len(line) >= 1]
            if len(candidate) >= 3:
                grid = [row[:3] for row in candidate[:3]]
        except Exception:
            grid = None

    if grid is None:
        return [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]

    # passa para 3x3
    processed: List[List[str]] = []
    for r in range(3):
        if r < len(grid):
            row = grid[r]
            if isinstance(row, str):
                cells = list(row)
            else:
                try:
                    cells = list(row)
                except Exception:
                    cells = [str(row)]
            proc_row = []
            for c in range(3):
                if c < len(cells):
                    proc_row.append(_normalize_ttt_cell(cells[c]))
                else:
                    proc_row.append('.')
        else:
            proc_row = ['.','.', '.']
        processed.append(proc_row)
    return processed

def _normalize_ttt_cell(cell) -> str:
    """
    Converte a célula para um único caractere: 'X','O' ou '.'.
    Suporta 'X'/'O', 'B'/'W', numeric (1/-1/0), None, '.' etc.
    """
    if cell is None:
        return '.'
    s = str(cell).strip()
    if s == '' or s in ('.','-', '_', '0'):
        return '.'
    su = s.upper()
    # preferir X/O se presentes
    if su[0] in ('X','O'):
        return su[0]
    if su[0] in ('B','W'):
        # mapear B->X, W->O (apenas para uniformizar)
        return 'X' if su[0] == 'B' else 'O'
    # tentar interpretação numérica
    try:
        v = float(s)
        if v == 0:
            return '.'
        return 'X' if v > 0 else 'O'
    except Exception:
        # fallback: primeiro caractere se for legível
        c = su[0]
        if c in ('X','O'):
            return c
        return '.'

def _find_winner(grid: List[List[str]]) -> Optional[str]:
    """
    Retorna 'X' ou 'O' se algum dos dois tem 3 em linha; caso contrário None.
    """
    lines = []
    
    for r in range(3):
        lines.append([grid[r][0], grid[r][1], grid[r][2]])
    
    for c in range(3):
        lines.append([grid[0][c], grid[1][c], grid[2][c]])
    
    lines.append([grid[0][0], grid[1][1], grid[2][2]])
    lines.append([grid[0][2], grid[1][1], grid[2][0]])

    for line in lines:
        if line[0] != '.' and line[0] == line[1] == line[2]:
            return line[0]
    return None


def make_move(state: GameState) -> Tuple[int, int]:
    """
    Retorna uma jogada calculada pelo minimax (poda alpha-beta) sem limite de profundidade.
    Usa `utility` como função de avaliação para estados terminais.
    """
    move = minimax_move(state, -1, utility)
    if move is None:
        legal = state.legal_moves()
        if not legal:
            return None
        return random.choice(list(legal))
    return move

def utility(state, player: str) -> float:
    """
    Avalia estados terminais do Tic-Tac-Toe misère
    - Se houver 3 em linha, quem formou a linha PERDE.
      Então utility(player) = -1.0 se player formou a linha, +1.0 se o oponente formou.
    - Se empate (tabuleiro cheio, sem 3 em linha), retorna 0.0.
    Observação: minimax chama essa função apenas para estados terminais, mas
    aqui fazemos verificação segura caso seja chamada em não-terminais (retorna 0).
    """
    try:
        if hasattr(state, "is_terminal") and state.is_terminal():
            if hasattr(state, "utility"):
                try:
                    return float(state.utility(player))
                except TypeError:
                    try:
                        return float(state.utility())
                    except Exception:
                        pass
    except Exception:
        pass

    grid = _extract_ttt_grid(state)
    winner = _find_winner(grid)

    p = player.upper()
    if p in ('B','W'):
        p = 'X' if p == 'B' else 'O'

    if winner is not None:
        if winner == p:
            return -1.0
        else:
            return 1.0

    # sem vencedor: empate terminal ou estado não-terminal
    # se terminal (e sem vencedor) -> empate -> 0.0
    # se não-terminal -> devolve 0.0 (seguro)
    return 0.0
