import ctypes

from xelib.lib import raw_api


class XelibError(Exception):
    '''
    An exception object for use by xelib
    '''
    pass


def validate(result, error_msg, ex=True):
    '''
    If result is false, raise XelibError with given message
    '''
    if not result and ex:
        raise XelibError(error_msg)


def get_string(callback, method=raw_api.GetResultString, error_msg='', ex=True):
    '''
    Helper for retrieving the string result of a callback function.

    In xedit-lib, many function that sounds like it would typically get a string
    value would expect you to pass in an integer by reference, and it will
    output the length of the string value onto the integer, and only return a
    success/fail boolean. You are then expected to pass the integer length to
    one of the more generic 'string getter' functions. These string getter
    functions typically take a string buffer and the expected length, and
    probably copies the string from a global location to the string buffer.

    This helper function takes the original function and runs through this
    whole process for you.
    '''
    error_prefix = f'{error_msg}: ' if error_msg else ''

    # need a c_int to pass by reference to the given callback
    len_ = ctypes.c_int()

    # run the callback, pass len_ into it by reference
    result = callback(ctypes.byref(len_))
    if not result and ex:
        raise XelibError(f'{error_prefix}Call to {repr(callback)} with '
                         f'parameter {repr(len_)} failed')

    # len_ should now contain the string length; if it does not look like the
    # length of a nonempty string, just return an empty string
    if len_.value < 1:
        return ''

    # otherwise, we will need a string buffer to copy the string onto; xedit-lib
    # strings are utf-16, so make sure to use a unicode buffer so that length
    # will exactly match
    buffer = ctypes.create_unicode_buffer(len_.value)

    # run the string getter method to copy string of the given length to the
    # given buffer, and return or error depending on boolean return value
    if method(buffer, len_):
        return buffer.value
    else:
        raise XelibError(f'{error_prefix}Failed to retrieve string via method '
                         f'{repr(method)}, buffer `{repr(buffer)}`, and '
                         f'length `{repr(len_)}`')


def get_handle(callback, error_msg='', ex=True):
    '''
    A 'handle' is a Cardinal value, which maps to c_uint. Methods that 'gets
    a handle' tend to want us to pass a c_uint by reference for it to put the
    handle there. This helper function takes care of this pattern.
    '''
    error_prefix = f'{error_msg}: ' if error_msg else ''

    res = ctypes.c_uint()
    if not callback(ctypes.byref(res)) and ex:
        raise XelibError(f'{error_prefix}Call to {repr(callback)} with '
                         f'parameter {repr(res)} failed')
    return res.value


def get_integer(callback, error_msg='', ex=True):
    error_prefix = f'{error_msg}: ' if error_msg else ''

    res = ctypes.c_int()
    if not callback(ctypes.byref(res)) and ex:
        raise XelibError(f'{error_prefix}Call to {repr(callback)} with '
                         f'parameter {repr(res)} failed')
    return res.value


def get_unsigned_integer(callback, error_msg='', ex=True):
    error_prefix = f'{error_msg}: ' if error_msg else ''

    res = ctypes.c_uint()
    if not callback(ctypes.byref(res)) and ex:
        raise XelibError(f'{error_prefix}Call to {repr(callback)} with '
                         f'parameter {repr(res)} failed')
    return res.value


def get_bool(callback, error_msg='', ex=True):
    error_prefix = f'{error_msg}: ' if error_msg else ''

    res = ctypes.c_bool()
    if not callback(ctypes.byref(res)) and ex:
        raise XelibError(f'{error_prefix}Call to {repr(callback)} with '
                         f'parameter {repr(res)} failed')
    return res.value


def get_double(callback, error_msg='', ex=True):
    error_prefix = f'{error_msg}: ' if error_msg else ''

    res = ctypes.c_double()
    if not callback(ctypes.byref(res)) and ex:
        raise XelibError(f'{error_prefix}Call to {repr(callback)} with '
                         f'parameter {repr(res)} failed')
    return res.value


def get_byte(callback, error_msg='', ex=True):
    '''
    A 'Byte' maps to c_ubyte. Methods that 'gets a byte' tend to want us to pass
    a c_ubyte by reference for it to put the byte data there. This helper
    function takes care of this pattern.
    '''
    error_prefix = f'{error_msg}: ' if error_msg else ''

    res = ctypes.c_ubyte()
    if not callback(ctypes.byref(res)) and ex:
        raise XelibError(f'{error_prefix}Call to {repr(callback)} with '
                         f'parameter {repr(res)} failed')
    return res.value


def get_array(callback, method=raw_api.GetResultArray, error_msg='', ex=True):
    '''
    Gets an array, similar pattern to how strings are gotten
    '''
    error_prefix = f'{error_msg}: ' if error_msg else ''

    # need a c_int to pass by reference to the given callback
    len_ = ctypes.c_int()

    # run the callback, pass len_ into it by reference
    result = callback(ctypes.byref(len_))
    if not result and ex:
        raise XelibError(f'{error_prefix}Call to {repr(callback)} with '
                         f'parameter {repr(len_)} failed')

    # len_ should now contain the array length; if it does not look like the
    # length of a nonempty array, just return an empty array
    if len_.value < 1:
        return []

    # otherwise, we will need a c_uint (Cardinal) buffer for the array to be
    # copied into, this buffer needs to be exactly the size of the expected
    # array
    buffer = (ctypes.c_uint * len_.value)()

    # run the array getter method to copy array of the given length to the
    # given buffer, return with a converted list of python ints; or error
    # if resulting boolean value indicates failure
    if method(buffer, len_):
        return [int(value) for value in buffer]
    else:
        raise XelibError(f'{error_prefix}Failed to retrieve array via method '
                         f'{repr(method)}, buffer `{repr(buffer)}`, and '
                         f'length `{repr(len_)}`')


def get_string_array(callback,
                     method=raw_api.GetResultString,
                     error_msg='',
                     ex=True):
    return get_string(callback,
                      method=method,
                      error_msg=error_msg,
                      ex=ex).splitlines()


def get_image_data(callback, error_msg=''):
    raise NotImplementedError


def get_dictionary(callback,
                   method=raw_api.GetResultString,
                   error_msg='',
                   ex=True):
    pairs = get_string_array(callback,
                             method=method,
                             error_msg=error_msg,
                             ex=ex)
    dictionary = {}
    for pair in pairs:
        key, value = pair.split('=', 1)
        dictionary[key] = value
    return dictionary