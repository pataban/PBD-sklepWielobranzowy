class ShopService:  # future facade for all operations on shop database
    def __init__(self, articleRepository, workerRepository, clientRepository):
        self._articleRepository = articleRepository
        self._workerRepository = workerRepository
        self._clientRepository = clientRepository

    # there will be many, many operations available...
