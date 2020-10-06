import os


class Environment:
    def __init__(self):
        import sys
        self.file = os.path.join(sys.path[0], '.env')
        if not self.file_exists():
            self.create_file()

    def file_exists(self):
        return os.path.exists(self.file)

    def create_file(self):
        open(self.file, 'w').close()

    def line_key(self, line):
        return line.split('=')[0].strip()

    def line_value(self, line):
        return line.split('=')[-1].strip()

    def get(self, *args):
        if not args:
            return None
        result = [None for x in range(0, len(args))]
        with open(self.file, 'r+') as fp:
            for line in fp:
                for i, arg in enumerate(args, 0):
                    if arg in line:
                        key = self.line_key(line)
                        if key == arg:
                            result[i] = self.line_value(line)

        return result[0] if len(args) == 1 else result

    def set(self, key, value):

        with open(self.file, 'r') as fp:
            all_lines = fp.readlines()

        found = False
        with open(self.file, 'w') as fp:
            for line in all_lines:
                if '=' in line:
                    if self.line_key(line) == key:
                        fp.writelines(f'{key} = {value}\n')
                        found = True
                    else:
                        fp.writelines(line)

            if not found:
                fp.writelines(f'{key} = {value}\n')
        return self

    def remove(self, *keys):

        with open(self.file, 'r') as fp:
            all_lines = fp.readlines()

        with open(self.file, 'w+') as fp:
            for line in all_lines:
                if not self.line_key(line) in keys:
                    fp.writelines(line)
        return self

    def removeAll(self):
        open(self.file, 'w+').close()
        return self
