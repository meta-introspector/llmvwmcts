import llm

from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo

from lang import score_func, can_be_solution

from prompts import prompt, expansion_count, min_lines, check_func
from common import limit_depth, max_completion_depth

montecarlo = MonteCarlo(Node(prompt))

def generate_complete(text, montecarlo):
    text = llm.generate(text, 1)[0]
    score = score_func(text)
    if score is not None:
        if score < 0:
            return (None, score)
        else:
            if can_be_solution(text, min_lines, check_func):
                montecarlo.solution = text
            return (text, score)
    else:
        return (text, 0.3)


def child_finder(node, montecarlo):
    if limit_depth(node):
        return

    (text, score) = generate_complete(node.state, montecarlo)
    if text is None:
        node.update_win_value(-1)
    else:
        child = Node(text)
        node.add_child(child)
        child.update_win_value(score)
        child.update_policy_value(score)

        child = Node(node.state)
        node.add_child(child)
        child.update_policy_value(0.2)

montecarlo.child_finder = child_finder

montecarlo.simulate(expansion_count)

print('CHOSEN SOLUTION')
print(montecarlo.solution)