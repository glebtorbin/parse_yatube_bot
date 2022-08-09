class ConnectionError(Exception):
    '''Сбой подключения'''
    pass


class CookieError(Exception):
    '''Не плдучается подключить Куки файлы'''
    pass


class ConstantError(Exception):
    '''Отсутствует какая либо переменная'''
    pass
