#RPC инвентарь
def add_item(inventory: list[str], item: str) -> list[str] | str:
    #if type(inventory) is not list[str]:
    if not isinstance(inventory, list):
        return 'Inventory must be list'
    if item == '':
        return 'item is empty'
    if item in inventory:
        return 'item already exists'
    inventory.append(item)
    return inventory

print(add_item(['bow'], 'arrow'))
print(add_item(['bow'], 'bow'))
print(add_item([], ''))
print(add_item('123', 'arrow'))