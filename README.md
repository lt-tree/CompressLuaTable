# CompressLuaTable

Python Script to compress lua table.

detail in:  [lt-tree for Lua表存储优化](<http://www.lt-tree.com/2019/05/12/Lua%E8%A1%A8%E5%AD%98%E5%82%A8%E4%BC%98%E5%8C%96/>)



<br/>

# 版本记录

## v0.0.1

- 添加文件
  - CompressLua.py  ： 数据压缩脚本文件
  - BEBase.py  ：基础模块文件
  - six.py  ：所需模块，作用：兼容Python2与Python3的库
  - slpp.py  ：所需模块，作用：将lua的table结构转化成 python的dictionary结构

## v0.0.2

- 修改：
  - CompressLua.py
    - 添加忽略文件列表
    - 修改输出的lua内部local变量引用错序问题

## v0.0.3

- 修改
  - CompressLua.py
    - 添加 获取对应key最频繁项方法
    - 对于遍历的部分均加排序
    - 
  - BEBase.py
    - 优化dict转lua文件方法：固定输出顺序，添加对bool类型及None类型的处理
    - 添加 输出到文件的方法

<br/>



ex:

```lua
-- personal_info.lua

local personal_info = {
    [1] = {
        id = 1,
        name = 'Lucas',
        sex = 'M';
        age = 10,
        des = {
            [1] = "aaaaaa",
            [2] = "bbbbbb",
            [3] = "cccccc",
        },
    },
    [2] = {
        id = 2,
        name = 'Alice',
        sex = 'F';
        age = 12,
        des = {
            [1] = "aaaaaa",
            [2] = "bbbbbb",
            [3] = "cccccc",
        },
    },
    [3] = {
        id = 3,
        name = 'Paul',
        sex = 'M';
        age = 16,
        des = {
            [1] = "aaaaaa",
            [2] = "cccccc",
        },
    },
    [4] = {
        id = 4,
        name = 'Tom',
        sex = 'M';
        age = 12,
        des = {
            [1] = "cccccc",
        },
    },
    [5] = {
        id = 5,
        name = 'Jerry',
        sex = 'M';
        age = 10,
        des = {
            [1] = "bbbbbb",
            [2] = "cccccc",
        },
    },
    [6] = {
        id = 6,
        name = 'Amy',
        sex = 'F';
        age = 17,
        des = {
            [1] = "aaaaaa",
            [2] = "bbbbbb",
            [3] = "cccccc",
        },
    },
    [7] = {
        id = 7,
        name = 'Henry',
        sex = 'M';
        age = 12,
        des = {
            [1] = "bbbbbb",
            [2] = "cccccc",
        },
    },
	[8] = {
        id = 8,
        name = 'David',
        sex = 'M';
        age = 12,
        des = {
            [1] = "bbbbbb",
        },
    },
    [9] = {
        id = 9,
        name = 'Cersei',
        sex = 'F';
        age = 20,
        des = {
            [1] = "aaaaaa",
        },
    },
    [10] = {
        id = 10,
        name = 'Joffery',
        sex = 'M';
        age = 12,
        des = {
            [1] = "bbbbbb",
            [2] = "cccccc",
        }
    },
    [11] = {
        id = 11,
        name = 'Alayaya',
        sex = 'F';
        age = 11,
        des = {
            [1] = "aaaaaa",
            [2] = "bbbbbb",
            [3] = "cccccc",
        }
    },
}

return personal_info
```



convert to:



```lua
local __rt1 = {
	[1] = 'aaaaaa',
	[2] = 'bbbbbb',
	[3] = 'cccccc',
}
local __rt2 = {
	[1] = 'bbbbbb',
	[2] = 'cccccc',
}

local personal_info = {
	[1] = {
		age = 10,
		name = 'Lucas',
	},
	[2] = {
		id = 2,
		name = 'Alice',
		sex = 'F',
	},
	[3] = {
		age = 16,
		des = {
			[1] = 'aaaaaa',
			[2] = 'cccccc',
		},
		id = 3,
		name = 'Paul',
	},
	[4] = {
		des = {
			[1] = 'cccccc',
		},
		id = 4,
		name = 'Tom',
	},
	[5] = {
		age = 10,
		des = __rt2,
		id = 5,
		name = 'Jerry',
	},
	[6] = {
		age = 17,
		id = 6,
		name = 'Amy',
		sex = 'F',
	},
	[7] = {
		des = __rt2,
		id = 7,
		name = 'Henry',
	},
	[8] = {
		des = {
			[1] = 'bbbbbb',
		},
		id = 8,
		name = 'David',
	},
	[9] = {
		age = 20,
		des = {
			[1] = 'aaaaaa',
		},
		id = 9,
		name = 'Cersei',
		sex = 'F',
	},
	[10] = {
		des = __rt2,
		id = 10,
		name = 'Joffery',
	},
	[11] = {
		age = 11,
		id = 11,
		sex = 'F',
	},
}

local __default_table = {
	age = 12,
	des = __rt1,
	id = 1,
	name = 'Alayaya',
	sex = 'M',
}

do
	local base = {__index = __default_table, __newindex = function() error("Attempt to modify read-only table") end}
	for k, v in pairs(personal_info) do
		setmetatable(v, base)
	end
	base.__metatable = false
end

return personal_info

```

