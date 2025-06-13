from Subject.Subject import Observer

class TextDatabase(Observer):
    def __init__(self, bible_name):
        self.filename = f"{bible_name}.txt"
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write("")

    def update(self, data):
        line = f"{data['chap abv']} {data['chapter number']}:{data['verse number']}\t{data['verse content']}\n"
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(line)
