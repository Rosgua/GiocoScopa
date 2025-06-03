import abc

class Observer(metaclass= abc.ABCMeta):
    """Interfaccia astratta per gli oggetti Observer.
    Gli observer vengono notificati quando si verifica 
    un cambiamento nello Subject."""
    @abc.abstractmethod
    def notify(self):
        pass

class Subject(metaclass= abc.ABCMeta):
    """Interfaccia astratta per gli oggetti Subject.
    I Subject gestiscono una lista di Observer e 
    li notificano quando il loro stato cambia."""
    @abc.abstractmethod
    def notifyAll(self):
        pass

    @abc.abstractmethod
    def register(self, ob):
        pass