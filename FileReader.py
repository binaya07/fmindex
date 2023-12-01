import sys

class FileReader(object):
    def __init__(self, filename):
        self.character = []
        self.__read_file(filename)

    def __read_file(self, filename):
        if filename is None:
            print("No filename provided.")
            return
        try:
            with open(filename, 'r') as f:
                for line in f:
                    for c in line.strip('\n'):  # This will exclude line breaks
                        self.character.append(c)
            print("Read %i characters successfully" % len(self.character))
        except IOError as e:
            print(f"I/O error({e.errno}): {e.strerror}")
            raise
        except Exception as e:  # More specific than generic 'except'
            print(f"Unexpected error: {e}")
            raise

    def get_characters(self):
        return self.character if self.character else None

    def get_text(self):
        return "".join(self.character) if self.character else None

    def is_read(self):
        return bool(self.character)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        file_reader = FileReader(filename)
    else:
        print("Please provide a filename as an argument.")

