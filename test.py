globalsymboltable = {}

stack = []

globalsymboltable['a'] = {}
globalsymboltable['a']['type'] = 'int'
mainsymboltable = {}
globalsymboltable['main'] = {}
globalsymboltable['main']['symbol'] = mainsymboltable

stack.append(globalsymboltable)