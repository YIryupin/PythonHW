from abc import ABC, abstractmethod

#Модель простого заказа

#Абстрактный класс Пользователь
class User(ABC):
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    @abstractmethod
    def get_info(self):
        pass

#Класс - Клиент
class Customer(User):
    def __init__(self, name: str, email: str, address: str):
        super().__init__(name, email)
        self.address = address
    def get_info(self):
        return 'Customer: ' + self.name + ', address: ' + self.address

#Класс - Курьер
class Courier(User):
    def __init__(self, name: str, email: str, vehicle: str):
        super().__init__(name, email)
        self.vehicle = vehicle
    def get_info(self):
        return 'Courier: ' + self.name + ', vehicle: ' + self.vehicle

#Класс - строка заказа
class OrderLine():
    def __init__(self, itemName: str, qty: int, itemPrice: float):
        if qty < 0: raise ValueError('Кол-во не может быть отрицательном!')  
        if itemPrice < 0: raise ValueError('Цена не может быть отрицательной!')  
        self.ItemName = itemName
        self.ItemPrice = itemPrice
        self.Qty = qty
        self.Amount = qty*itemPrice
    #Обновление кол-ва в строке заказа, в большу и меньшую сторону, уменьшение меньше нуля равнозначно обнулению кол-ва
    def updateQty(self, qtyAdd: int): 
        self.Qty += qtyAdd
        if self.Qty < 0: self.Qty = 0
        self.Amount = self.Qty*self.ItemPrice
    def get_info(self):
        return self.ItemName + '  ' + str(self.Qty) + '  ' + str(self.ItemPrice) + '   ' + str(self.Amount)

#Класс заказа
class Order():
    #Определяю типы приватных переменных:
    __ID: int
    __Cust: Customer
    __OrderLines: dict[str, OrderLine]
    __DiscountPercent: int
    __Cour: Courier
    __OrderAmount: float
    __OrderAmountDisc: float
    __OrderAmountWDisc: float

    def __init__(self, id: int, customer: Customer):
        self.__ID = id
        self.__Cust = customer
        self.__OrderLines = dict()
        self.__DiscountPercent = 0
        self.__Cour = None
        self.__OrderAmount = 0
        self.__OrderAmountDisc = 0
        self.__OrderAmountWDisc = 0
    def getId(self) -> int:
        return self.__ID
    def getCustomer(self) -> Customer:
        return self.__Cust
    def setCourier(self, cour: Courier):
        self.__Cour = cour
    def getCourier(self) -> Courier:
        return self.__Cour
    #Публичный Метод для добавления новой строки или обновления кол-ва в существующей: 
    def OrderLine_AddOrUpd(self, itemName: str, qty: int, itemPrice: float):
        if itemName in self.__OrderLines:
            self.__OrderLines.get(itemName).updateQty(qty)
        else:
            newLine = OrderLine(itemName, qty, itemPrice)
            self.__OrderLines[itemName] = newLine
        self.__calcOrderAmounts()
    #Публичный метод удаления строки заказа
    def OrderLine_Delete(self, itemName: str):
        del self.__OrderLines[itemName]
        self.__calcOrderAmounts()
    #Приватный метод для обновления итоговых сумм по заказу, вызывается каждый раз при изменении в строках заказа
    #или при изменении скидки по заказу
    def __calcOrderAmounts(self):
        currLine: OrderLine
        sumTmp = 0
        for currLine in self.__OrderLines.values():
            sumTmp += currLine.Amount
        self.__OrderAmount = sumTmp
        self.__OrderAmountDisc = self.__OrderAmount*self.__DiscountPercent/100
        self.__OrderAmountWDisc = self.__OrderAmount - self.__OrderAmountDisc
    #Метод для установки скидки в целом на заказ
    def setDiscountPercent(self, disc: int):
        self.__DiscountPercent = disc
        self.__calcOrderAmounts()
    def getOrderAmmount(self) -> float:
        return self.__OrderAmount
    def getOrderAmmountDisc(self) -> float:
        return self.__OrderAmountDisc
    def getOrderAmmountWDisc(self) -> float:
        return self.__OrderAmountWDisc
    def printOrder(self):
        print('============================================================================')
        print('Order №', self.__ID)
        print(self.__Cust.get_info())
        if self.__Cour is not None:
            print(self.__Cour.get_info())
        else: 
            print('Courier in not defined yet!')
        print('ORDER LINES:')
        currLine: OrderLine
        for currLine in self.__OrderLines.values():
            print(currLine.get_info())
        print('TOTALS: Order ammount - ', self.__OrderAmount, ' Discount - ', self.__OrderAmountDisc, ' Order amount without discount - ', self.__OrderAmountWDisc)
        print('============================================================================')

TestCust = Customer('Alice', 'test@google.com', 'Baker Street 221B')
TestCour = Courier('Bob', 'test2@google.com', 'bike')
TestOrder = Order(1, TestCust)
TestOrder.OrderLine_AddOrUpd('pizza', 1, 100.5)
TestOrder.OrderLine_AddOrUpd('cola', 1, 50.2)
TestOrder.OrderLine_AddOrUpd('dessert', 1, 150.3)
TestOrder.printOrder()
TestOrder.setDiscountPercent(10)
TestOrder.printOrder()
TestOrder.OrderLine_AddOrUpd('pizza', 1, 100.5)
TestOrder.printOrder()
TestOrder.OrderLine_Delete('dessert')
TestOrder.setCourier(TestCour)
TestOrder.printOrder()
TestOrder.OrderLine_AddOrUpd('dessert', 1, -150.3)
