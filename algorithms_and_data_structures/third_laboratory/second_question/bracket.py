def is_balanced(sequence: str) -> bool:
    stack = []
    bracket_map = {')': '(', '}': '{', ']': '['}

    for char in sequence:
        if char in bracket_map.values():
            stack.append(char)
        elif char in bracket_map:
            if not stack or stack[-1] != bracket_map[char]:
                return False
            stack.pop()

    return len(stack) == 0


