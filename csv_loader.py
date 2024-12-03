import os
import re
import folder_paths

#ARTISTS

class CharactersLoader:
    """
    Loads csv file with characters. For migration purposes from automatic11111 webui.
    """
    
    @staticmethod
    def load_characters_csv(characters_path: str):
        """Loads csv file with characters. It has only one column.
        Ignore the first row (header).
        characters_prompt are strings separated by comma. Each string is a prompt.
        clothes_prompt are strings separated by comma. Each string is a prompt.

        Returns:
            list: List of characters. Each style is a dict with keys: style_name and value: [characters_prompt, clothes_prompt]
        """
        characters = {"Error loading characters.csv, check the console": ["",""]}
        if not os.path.exists(characters_path):
            print(f"""Error. No characters.csv found. Put your characters.csv in the custom_nodes-ComfyUI_Loader-CSV directory of ComfyUI. Then press "Refresh".
                  Your current root directory is: {folder_paths.base_path}
            """)
            return characters
        try:
            with open(characters_path, "r", encoding="utf-8") as f:    
                characters = [[x.replace('"', '').replace('\n','') for x in re.split(',(?=(?:[^"]*"[^"]*")*[^"]*$)', line)] for line in f.readlines()[1:]]
                characters = {x[0]: [x[1],x[2]] for x in characters}
        except Exception as e:
            print(f"""Error loading characters.csv. Make sure it is in the custom_nodes-ComfyUI_Loader-CSV directory of ComfyUI. Then press "Refresh".
                    Your current root directory is: {folder_paths.base_path}
                    Error: {e}
            """)
        return characters
        
    @classmethod
    def INPUT_TYPES(cls):
        cls.characters_csv = cls.load_characters_csv(os.path.join(folder_paths.base_path, "custom_nodes\\ComfyUI-CSV-Loader\\CSV\\VirtuaRealCharacters.csv"))
        return {
            "required": {
                "characters": (list(cls.characters_csv.keys()),),
            },
                                
        }

    RETURN_TYPES = ("STRING","STRING")
    RETURN_NAMES = ("角色特征", "服装特征")
    FUNCTION = "execute"
    CATEGORY = "CSV Loaders"   

    def execute(self, characters):
            return (self.characters_csv[characters][0], self.characters_csv[characters][1])


#NODE NAMING

NODE_CLASS_MAPPINGS = {
    "Load VirtuaRealCharacters Selector": CharactersCSVLoader,

}
NODE_DISPLAY_NAME_MAPPINGS = {
    "CharactersLoader": "选择预设角色",
    
}
