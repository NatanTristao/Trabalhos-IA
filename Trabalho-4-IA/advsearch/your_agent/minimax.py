from typing import Callable, Tuple

def minimax_move(state, max_depth: int, eval_func: Callable) -> Tuple[int, int]:

    root_player = state.player

    # Minimax com poda alfa-beta
    def alphabeta(node, depth, alpha, beta, maximizing_player):
        # Terminal
        if node.is_terminal() or (max_depth != -1 and depth == max_depth):
            return eval_func(node, root_player)

        moves = node.legal_moves()

        # Se não há jogadas, o jogador passa a vez
        if not moves:
            passed = node.copy()
            passed.player = 'B' if node.player == 'W' else 'W'
            return alphabeta(passed, depth + 1, alpha, beta, not maximizing_player)

        if maximizing_player:
            value = float("-inf")
            for move in moves:
                child = node.next_state(move)
                value = max(value, alphabeta(child, depth + 1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float("inf")
            for move in moves:
                child = node.next_state(move)
                value = min(value, alphabeta(child, depth + 1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    # Escolher a melhor jogada para o jogador raiz
    legal = state.legal_moves()
    if not legal:
        return None

    best_move = None
    best_value = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    for move in legal:
        child = state.next_state(move)
        value = alphabeta(child, 1, alpha, beta, False)

        if value > best_value:
            best_value = value
            best_move = move

        alpha = max(alpha, best_value)

    return best_move
