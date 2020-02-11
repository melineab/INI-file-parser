class GetInfo:
    def __init__(self, file):
        self.file = file
        self.dict = {}

        if self.file.split('.')[1].upper() != 'INI':
            raise Exception('Extension Error')

    def file_reader(self) -> dict:
        self.key = 'DEFAULT'
        self.inner_dict = {}

        with open(self.file, 'r') as f:
            for line, value in enumerate(f):
                values = value.split()
                if value[0] == ('#' or ';') or len(values) == 0:
                    continue

                if '=' in value:
                    section_list = value.split('=')
                    self.inner_dict[section_list[0].strip()
                                    ] = section_list[1].strip()
                    self.dict[self.key] = self.inner_dict
                    del section_list

                if values != [] and line == 0 and values[0][0] != '[':
                    key = self.key

                if values != [] and values[0][0] == '[':
                    self.key = values[0][1:-1]
                    self.dict[self.key] = self.inner_dict
                    self.inner_dict = {}

        return self.dict


class Parser:
    def __init__(self, file):
        self.file = file
        self.dict = GetInfo(self.file).file_reader()

    def __getitem__(self, keys):
        sec_key, dict_key = keys
        return self.dict[sec_key][dict_key]

    def config(self) -> dict:
        return self.dict

    def section_dicts(self):
        value_list = []
        key_value = self.dict
        for val in key_value.values():
            value_list.append(val)
        return value_list

    def sections(self) -> list:
        print('Configuration file sections:')
        return list(self.dict.keys())


if __name__ == '__main__':
    file = 'sample.ini'
    parser = Parser(file)
    print(parser.sections())
    print(parser.config())
    print(parser.config()['mysql1']['host'])
    print(parser['myserver', 'os'])
