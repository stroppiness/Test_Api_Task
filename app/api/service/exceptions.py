class WalletNotFoundError(Exception):
    pass


class InvalidAmountError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


class WalletAlreadyExistsError(Exception):
    pass


class WalletSaveError(Exception):
    pass
