# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util
from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount=0.9, iterations=100): 
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() 

        # Percorre todos os estados do MDP
        for i in range(self.iterations):
            newValues = util.Counter() # guarda os valores calculados para a próxima iteração

            for state in self.mdp.getStates(): #percorre todos os estados do MDP
                if self.mdp.isTerminal(state):
                    
                    newValues[state] = 0
                    continue

                actions = self.mdp.getPossibleActions(state)
                if not actions:
                    newValues[state] = 0
                    continue

                # usado para estado não-terminal, calculando o máximo em relação às ações: max_a Q(s,a)
                maxQ = float('-inf')
                for action in actions:
                    q = self.computeQValueFromValues(state, action)
                    if q > maxQ:
                        maxQ = q
                newValues[state] = maxQ

            # atualização síncrona: só é substituída após calcular os novos valores para todos os estados
            self.values = newValues


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
            Computa o Q-valor de (state, action) usando a função de valores
            armazenada em self.values.


            Fórmula usada:
            Q(s,a) = sum_{s'} P(s'|s,a) * [R(s,a,s') + gamma * V(s')]


            Comentários importantes sobre a implementação:
                - Percorremos todos os pares (nextState, prob) retornados por
                    getTransitionStatesAndProbs(state, action).
                - Para cada transição acumulamos prob * (recompensa + discount * V(nextState)).
                - Usamos self.values (valores da iteração atual) — isto é coerente
                    com a iteração de valor síncrona implementada no __init__.
        """
        qValue = 0.0
        # getTransitionStatesAndProbs retorna uma lista de (nextState, prob)
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            # obtemos a recompensa para a transição (s,a,nextState)
            reward = self.mdp.getReward(state, action, nextState)
            # acumulamos a contribuição desta transição para o Q(s,a)
            qValue += prob * (reward + self.discount * self.values[nextState])
        return qValue

    def computeActionFromValues(self, state):
        """
            Retorna a melhor ação no estado dado, de acordo com os valores
            atualmente armazenados em self.values (a política implícita).


            Comportamentos especíﬁcos implementados:
                - Se o estado for terminal, retornamos None.
                - Se não houver ações legais, retornamos None.
                - Em caso de empate entre ações com mesmo Q-valor, escolhemos a
                    primeira encontrada (que depende da ordem retornada pelo MDP).
                    Se você quiser um tie-break determinístico diferente, podemos
                        ordenar a lista de ações (por exemplo, sorted(actions)) antes de iterar.
        """
        if self.mdp.isTerminal(state):
            return None

        actions = self.mdp.getPossibleActions(state)
        if not actions:
            return None

        bestAction = None
        bestValue = float('-inf')
        for action in actions:
            q = self.computeQValueFromValues(state, action)
            if q > bestValue:
                bestValue = q
                bestAction = action

        return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
