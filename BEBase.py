"""Basic method 
    
method list
BEParseError : 
BEConvert : Convert Method
BEOutput : Formatted output

"""

import json
import codecs
from slpp import slpp as lua

SPECIAL_CHAR_LIST = [
    '$',
    '-'
]

class BEParseError(Exception):
    pass

class BEConvert(object):
    def __init__(self):
        pass

    def convert_lua_table_dict(self, file_path):
        """Convert lua table to python dict.
                    
            This method parses lua file by intercepting the first '{' and last '}'.
            Make sure there is only one table in the file.
            Any other information previous the first '{' and after the last '}' will be ignored.

            Args:
                file_path: lua table file path.

            Returns:
                A dict converted by file.
        """
        
        file_handler = codecs.open(file_path, 'r', encoding='utf-8')
        file_content = file_handler.read()
        file_handler.close()
        
        file_content = file_content[file_content.find('{') : file_content.rfind('}') + 1]
        py_dict = lua.decode(file_content)

        return py_dict


    def __have_special_char(self, check_str):
        """Check have special char

            Check if have special char the char list is SPECIAL_CHAR_LIST.
            lua key can't recognize special char for key like $, - 

            Args:
                check_str: string, need check string

            Returns:
                int, the char in string index, return -1 if not exist
        """

        for char in SPECIAL_CHAR_LIST:
            if check_str.find(char) != -1:
                return True

        return False


    def convert_dict_lua_file(self, file_handler, lua_dict, deep):
        """Convert dict to lua file

            Output dict in file by lua table format.
            Special process value string '__rt'

            Args:
                file_handler: file handler
                lua_dict: dict
                deep: int
        """

        prefix_tab = "\t" * deep
        for key, value in lua_dict.items():
            if isinstance(key, int):
                file_handler.write("%s[%s] = " % (prefix_tab, key))
            elif isinstance(key, str):
                if self.__have_special_char(key):
                    file_handler.write("%s[\"%s\"] = " % (prefix_tab, key))
                else:
                    file_handler.write("%s%s = " % (prefix_tab, key))
            else:
                print('ERROR!  Wrong key type!')
                raise SystemExit

            if isinstance(value, dict):
                file_handler.write("{\n")
                self.convert_dict_lua_file(file_handler, value, deep + 1)
                file_handler.write("%s},\n" % (prefix_tab))
            elif isinstance(value, str):
                if value.find("__rt") != -1:
                    file_handler.write("%s,\n" % (value))
                else:
                    file_handler.write("\'%s\',\n" % (value))
            else:
                file_handler.write("%s,\n" % (value))




class BEOutput(object):
    def __init__(self):
        pass

    def format_show(self, content):
        """Format show variable

        """
        
        print(json.dumps(content, indent=4, ensure_ascii=False))


BEOutput = BEOutput()
BEConvert = BEConvert()

__all__ = ['BEOutput']
__all__ = ['BEConvert']