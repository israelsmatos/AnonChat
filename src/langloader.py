from pathlib import Path
from config import lang_dir

class Langloader:
    def __init__(self, lang_code_file_config=""):
        self.lanfilcod: str = lang_code_file_config
        self.langs = Path(lang_dir)
        self.available_langs = []

    def __call__(self):
        self.translated = {}
        for lang in self.langs.iterdir():
            self.available_langs.append(lang.stem)
            self.translated[lang.stem] = self.initialise(lang)
        return self.translated

    def count_t(self, target, text) -> int:
        counter = 0
        for i in text:
            if target == i:
                counter += 1
            else:
                return counter
    
    def initialise(self, lang_file: str, identation: int =4) -> dict:
        with open(lang_file, "r") as f:
            key, fkey, text = "", "", ""
            main_dict = {}
            for i, line in enumerate(f):
                if "//" in line:
                    continue

                start = self.count_t(" " or "\t", line) # identation counter
                
                if start == 0 and not line == "\n":
                    key = line.replace("\n", "")
                    main_dict[key] = {}
                
                if int(start // identation) == 1:
                    fkey = line.replace("\n", "").replace(" ", "").strip()
                    main_dict[key][fkey] = ""

                if int(start // identation) == 2:
                    text = line.strip(" ")
                    main_dict[key][fkey] += text
                
            return main_dict



if __name__ == "__main__":
    obj = Langloader()
    print(obj())
