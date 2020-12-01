from algebra import *


expr= Product([Sum([1, 2, 3]), Sum([12, 13]), Sum([8, 9])])
print(expr.simplify())
