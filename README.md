# CompressLuaTable

Python Script to compress lua table.

detail in:  [lt-tree for Lua表存储优化](<http://www.lt-tree.com/2019/05/12/Lua%E8%A1%A8%E5%AD%98%E5%82%A8%E4%BC%98%E5%8C%96/>)



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
	},
	[2] = {
		id = 2,
		name = 'Alice',
		sex = 'F',
	},
	[3] = {
		id = 3,
		name = 'Paul',
		age = 16,
		des = {
			[1] = 'aaaaaa',
			[2] = 'cccccc',
		},
	},
	[4] = {
		id = 4,
		name = 'Tom',
		des = {
			[1] = 'cccccc',
		},
	},
	[5] = {
		id = 5,
		name = 'Jerry',
		age = 10,
		des = __rt2,
	},
	[6] = {
		id = 6,
		name = 'Amy',
		sex = 'F',
		age = 17,
	},
	[7] = {
		id = 7,
		name = 'Henry',
		des = __rt2,
	},
	[8] = {
		id = 8,
		name = 'David',
		des = {
			[1] = 'bbbbbb',
		},
	},
	[9] = {
		id = 9,
		name = 'Cersei',
		sex = 'F',
		age = 20,
		des = {
			[1] = 'aaaaaa',
		},
	},
	[10] = {
		id = 10,
		name = 'Joffery',
		des = __rt2,
	},
	[11] = {
		id = 11,
		name = 'Alayaya',
		sex = 'F',
		age = 11,
	},
}

local __default_table = {
	id = 1,
	name = 'Lucas',
	sex = 'M',
	age = 12,
	des = __rt1,
}

do
	local base = {__index = __default_table, __newindex = function() error("Attempt to modify read-only table") end}
	for k, v in pairs(personal_info) do
		setmetatable(v, base)
	end
	base.__metatable = __default_table
end

return personal_info

```

