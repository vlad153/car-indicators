from .core_dal import CoreDAL
from .user.manager import MangerUserDAL


class GlobalDAL(MangerUserDAL, CoreDAL):
    pass
