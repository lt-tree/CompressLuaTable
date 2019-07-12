"""
Compress Lua table
    
- author: ltree98
- version: 0.0.2

- need:
python 3.x

- input:
-s source folder
-d dest folder[default is  ./temp/]

"""

# -*- coding: utf-8 -*-

import os
import sys
import codecs
import shutil
import optparse
from BEBase import BEConvert as convert
from BEBase import BEOutput as output


###################################################################
##
##  config
##

REPEAT_KEY_PREFIX = "__rt"
DEFAULT_TABLE_NAME = "__default_table"
LOCAL_TABLE_MAX = 190

default_dst_path = os.getcwd() + "\\temp"

IGNORE_FILE_LIST = {
    #file name without suffix
}

###################################################################
##
##  tools
##

def count_dict_deep(dict_temp):
    deep = 0
    for item in dict_temp.values():
        if isinstance(item, dict):
            temp_deep = count_dict_deep(item)
            if temp_deep > deep:
                deep = temp_deep

    return deep+1

def calc_weight(obj1):
    dict1 = eval(obj1[0])
    times1 = obj1[1]

    deep1 = count_dict_deep(dict1)
    ans = deep1 + 1/times1

    return ans

def get_dict_str(dict):
    dict_str = '{'
    for key, value in sorted(dict.items()):
        if isinstance(key, str):
            dict_str = dict_str + '\'' + key + '\': '
        else:
            dict_str = dict_str + str(key) + ':'

        if isinstance(value, str):
            dict_str = dict_str + '\'' + value + '\', '
        else:
            dict_str = dict_str + str(value) + ','
    dict_str = dict_str + '}'

    return dict_str

def get_final_frequency_item(dict_frequency):
    """Get final frequency item
        
        Different python version have different process for same frequency.
        At first, get most freqency items then sort keys to find out final most frequency item
        
        Args:
            dict_frequency: dict
        Returns:
            string: final most frequency item
    """

    most_frequency_items = {}
    most_frequency = -1
    for key, value in sorted(dict_frequency.items(), key=lambda item:item[1], reverse=True):
        if most_frequency == -1:
            most_frequency = value
            most_frequency_items[key] = value
        elif most_frequency == value:
            most_frequency_items[key] = value

    return sorted(most_frequency_items.items(), key=lambda item:str(item[0]))[0][0]

def count_table_frequency(unit_dict, dict_frequency):
    """Count table frequency
        
        Count table frequency and record as {table string: times}

        Args:
            unit_dict: dict, need analyse data
            dict_frequency: dict, the record's set
    """

    unit_str = get_dict_str(unit_dict)
    if unit_str in dict_frequency:
        dict_frequency[unit_str] = dict_frequency[unit_str] + 1
    else:
        dict_frequency[unit_str] = 1

    # traversing sub dict
    for item in unit_dict.values():
        if isinstance(item, dict):
            count_table_frequency(item, dict_frequency)


def count_table_value_frequency(key, value, item_frequency):
    """Count table value frequency

        Count every excel column element appear times.
        Record as {
                    key1 : {element1 : times, element2: times, ...}
                    key2 : {element1 : times, element2: times, ...}
                    ...
                    }

        Args:
            key: string
            value: string or dict
            item_frequency: dict, the record's set
    """

    if isinstance(value, dict):
        value = str(value)

    if key in item_frequency.keys():
        if value in item_frequency[key].keys():
            item_frequency[key][value] = item_frequency[key][value] + 1
        else:
            item_frequency[key][value] = 1
    else:
        item_frequency[key] = {}
        item_frequency[key][value] = 1


def traverse_table(excel_dict, dict_frequency, item_frequency):
    """Traverse table.
        
        Analyse lua table.

        Args:
            excel_dict: dict
            dict_frequency: dict
            item_frequency: dict
    """

    for key in sorted(excel_dict):
        if isinstance(excel_dict[key], dict):
            count_table_frequency(excel_dict[key], dict_frequency)

            for k, v in sorted(excel_dict[key].items()):
                count_table_value_frequency(k, v, item_frequency)


def check_repeat_dict(item_dict, repeat_dict):
    """Check repeat dict
        
        Check repeat dict and return the repeat index, if not exist in repeat dict return -1.

        Args:
            item_dict: dict
            repeat_dict: dict

        Returns:
            int
    """

    for repeat_item in repeat_dict.keys():
        item = eval(repeat_item)
        if item == item_dict:
            return repeat_dict[repeat_item]    
    return -1


def replace_repeat_dict(item_dict, repeat_dict, cur_index = -1):
    """Replace repeat dict

        Check if element exist in repeat dict and replace by designation string.
    
        Args:
            item_dict: dict
            repeat_dict: dict
    """

    cur_index = -1

    for key, value in item_dict.items():
        if isinstance(value, dict):
            index = check_repeat_dict(value, repeat_dict)
            if index != -1 and (index < cur_index or cur_index == -1):
                if index > 190:
                    item_dict[key] = REPEAT_KEY_PREFIX + '[' + str(index - LOCAL_TABLE_MAX) + ']'
                else:
                    item_dict[key] = REPEAT_KEY_PREFIX + str(index)
            else:
                replace_repeat_dict(value, repeat_dict, cur_index)



def output_file(table_name, file_path, repeat_dict, final_dict, default_dict):
    """Output file

        Args:
            table_name: string
            file_path: path
            repeat_dict: dict
            final_dict: dict
            default_dict: dict
    """

    file_handler = codecs.open(file_path, 'a', encoding='utf-8')

    # output repeat dict
    for dictStr, index in sorted(repeat_dict.items(), key=lambda item:item[1]):
        # replace repeat item by repeat_dict 
        repeat_dict_item = eval(dictStr)
        replace_repeat_dict(repeat_dict_item, repeat_dict, index)

        if index <= LOCAL_TABLE_MAX:
            # file_handler.write("local %s = {\n" % (REPEAT_KEY_PREFIX + str(index)))
            file_handler.write("local %s = {\n" % (REPEAT_KEY_PREFIX + str(index)))
            convert.convert_dict_lua_file(file_handler, repeat_dict_item, 1)
            file_handler.write("}\n")
        else:
            if index == (LOCAL_TABLE_MAX + 1):
                file_handler.write("\nlocal __rt = createtable and createtable(%d, 0) or {}\n" % (len(repeat_dict)-LOCAL_TABLE_MAX))
            
            file_handler.write("__rt[%d] = {\n" % (index - LOCAL_TABLE_MAX))
            convert.convert_dict_lua_file(file_handler, repeat_dict_item, 1)
            file_handler.write("}\n")       

    # output final dict
    replace_repeat_dict(final_dict, repeat_dict)
    file_handler.write("\nlocal %s = {\n" % (table_name))
    convert.convert_dict_lua_file(file_handler, final_dict, 1)
    file_handler.write("}\n")

    # output default dict
    replace_repeat_dict(default_dict, repeat_dict)
    file_handler.write("\nlocal %s = {\n" % (DEFAULT_TABLE_NAME))
    convert.convert_dict_lua_file(file_handler, default_dict, 1)
    file_handler.write("}\n")

    # set metatable and read-only
    file_handler.write("\ndo\n")
    file_handler.write("\tlocal base = {__index = %s, __newindex = function() error(\"Attempt to modify read-only table\") end}\n" % (DEFAULT_TABLE_NAME))
    file_handler.write("\tfor k, v in pairs(%s) do\n" % (table_name))
    file_handler.write("\t\tsetmetatable(v, base)\n")
    file_handler.write("\tend\n")
    file_handler.write("\tbase.__metatable = false\n")
    file_handler.write("end\n")

    file_handler.write("\nreturn %s\n" % (table_name))
    file_handler.close()
    

###################################################################
##
##  structure method
##

def structure_repeat_dict(dict_frequency):
    """Structure frequency dict

        Select frequency > 1 element to structure dict.

        Args:
            dict_frequency: dict

        Returns:
            dict; {dict's string : repeat index}
    """

    repeat_frequency_dict = {}
    for key, value in sorted(dict_frequency.items(), key=lambda x:calc_weight(x)):
        if value > 1:
            if value not in repeat_frequency_dict.keys():
                repeat_frequency_dict[value] = []
            repeat_frequency_dict[value].append(key)

    repeat_dict = {}
    repeat_index = 1
    for frequency, keys in sorted(repeat_frequency_dict.items(), key=lambda item:item[0], reverse=True):
        for key in sorted(keys):
            repeat_dict[key] = repeat_index
            repeat_index = repeat_index + 1

    return repeat_dict


def structure_default_dict(excel_dict, all_item_frequency):
    """Structure default dict
        
        Args:
            excel_dict: dict
            all_item_frequency: dict

        Returns:
            dict; {key : most frequently value}
    """

    excel_item = {}
    for key, item in sorted(excel_dict.items()):
        excel_item = item
        break

    default_dict = {}
    for key, value in sorted(excel_item.items()):
        item_frequency = get_final_frequency_item(all_item_frequency[key])
        if isinstance(value, dict):
            default_dict[key] = eval(item_frequency)
        else:
            default_dict[key] = item_frequency

    return default_dict


def structure_final_dict(excel_dict, default_dict):
    """Structure final dict
        
        Structure final dict by default_dict and excel_dict.

        Args:
            excel_dict: dict
            default_dict: dict

        Returns:
            dict
    """

    final_dict = {}
    for key, value in sorted(excel_dict.items()):
        final_dict[key] = {}

        if isinstance(value, dict):
            for k, v in sorted(value.items()):
                if default_dict[k] != v:
                    final_dict[key][k] = v
        else:
            final_dict[key] = value

    return final_dict



def process_file(src_path, dst_path, file_name):
    dict_frequency_statistics = {}
    all_item_frequency_statistics = {}

    # conver lua table to python dict
    file_dict = convert.convert_lua_table_dict(src_path)

    # analyse dict
    traverse_table(file_dict, dict_frequency_statistics, all_item_frequency_statistics)

    # get repeat dict
    repeat_dict = structure_repeat_dict(dict_frequency_statistics)

    # get default dict
    default_dict = structure_default_dict(file_dict, all_item_frequency_statistics)

    # structure final dict
    final_dict = structure_final_dict(file_dict, default_dict)

    output_file(file_name, dst_path, repeat_dict, final_dict, default_dict)



def parseargs():
    parser = optparse.OptionParser()
    parser.add_option(
        "-s",
        action  = "store",
        dest    = "src_path",
        default = "",
        help    = "Set src path"
    )
    parser.add_option(
        "-d",
        action  = "store",
        dest    = "dst_path",
        default = default_dst_path,
        help    = "Set dest directory path"
    )
    return parser.parse_args()


if __name__ == "__main__":
    (opts, args) = parseargs()

    if opts.src_path != "":

        # check if folder exist
        if not os.path.exists(opts.dst_path):
            os.makedirs(opts.dst_path)

        files = os.listdir(opts.src_path)
        for file in files:
            file_name, file_extension = os.path.splitext(file)
            src_path = opts.src_path + '\\' + file
            dst_path = opts.dst_path + '\\' + file

            if file_name not in IGNORE_FILE_LIST:
                print('====> Start process file: ' + file)
                process_file(src_path, dst_path, file_name)
            else:
                print('!!!!> not process file: ' + file_name + ', in the IGNORE_FILE_LIST')
                shutil.copyfile(src_path, dst_path)

    
