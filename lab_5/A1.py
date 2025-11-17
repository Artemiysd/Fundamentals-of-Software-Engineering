def remove_parentheses(text):
    while True:
        left = text.find('(')
        right = text.find(')', left)

        if left == -1 or right == -1:
            break

        text = text.replace(text[left:right + 1], '', 1)

    return text.strip()
print(remove_parentheses("(()()()()()()()()()()asdasd"))