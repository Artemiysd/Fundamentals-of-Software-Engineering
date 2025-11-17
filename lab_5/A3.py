def make_abbreviation(text):
    words = text.split()
    result = []

    for w in words:
        if len(w) >= 3:
            result.append(w[0].upper())

    return "".join(result)


print(make_abbreviation("New York City"))
print(make_abbreviation("Yanka Kupala State University of Grodno"))