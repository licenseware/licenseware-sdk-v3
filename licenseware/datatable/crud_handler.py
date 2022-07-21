from abc import ABCMeta, abstractmethod



class CrudHandler(metaclass=ABCMeta): # pragma no cover
    
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def post(self):
        pass

    @abstractmethod
    def put(self):
        pass

    @abstractmethod
    def delete(self):
        pass