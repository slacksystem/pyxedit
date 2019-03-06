
class ElementValuesMethods:
    def name(self, id_):
        return self.get_string(
            lambda len_: self.raw_api.Name(id_, len_),
            error_msg=f'Name failed on {id_}')

    def long_name(self, id_):
        return self.get_string(
            lambda len_: self.raw_api.LongName(id_, len_),
            error_msg=f'LongName failed on {id_}')

    def display_name(self, id_):
        return self.get_string(
            lambda len_: self.raw_api.DisplayName(id_, len_),
            error_msg=f'DisplayName failed on {id_}')

    def placement_name(self, id_):
        rec = self.get_links_to(id_, 'NAME')
        return rec > 0 and f'Places {self.name(rec)}'

    def path(self, id_):
        return self.get_string(
            lambda len_: self.raw_api.Path(id_, True, False, len_),
            error_msg=f'Path failed on {id_}')

    def long_path(self, id_):
        return self.get_string(
            lambda len_: self.raw_api.Path(id_, False, False, len_),
            error_msg=f'Path failed on {id_}')

    def local_path(self, id_):
        return self.get_string(
            lambda len_: self.raw_api.Path(id_, False, True, len_),
            error_msg=f'Path failed on {id_}')

    def signature(self, id_):
        return self.get_string(
            lambda len_: self.raw_api.Signature(id_, len_),
            error_msg=f'Signature failed on {id_}')

    def sort_key(self, id_):
        return self.get_string(
            lambda len_: self.raw_api.SortKey(id_, len_),
            error_msg=f'SortKey failed on {id_}')

    def get_value(self, id_, path='', ex=False):
        return self.get_string(
            lambda len_: self.raw_api.GetValue(id_, path, len_),
            error_msg=f'Failed to get element value at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def set_value(self, id_, value, path=''):
        self.verify_execution(
            self.raw_api.SetValue(id_, path, value),
            error_msg=f'Failed to set element value at '
                      f'{self.element_context(id_, path)}')

    def get_int_value(self, id_, path='', ex=False):
        return self.get_integer(
            lambda res: self.raw_api.GetIntValue(id_, path, res),
            error_msg=f'Failed to get int value at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def set_int_value(self, id_, value, path=''):
        self.verify_execution(
            self.raw_api.SetIntValue(id_, path, value),
            error_msg=f'Failed to set int value at '
                      f'{self.element_context(id_, path)}')

    def get_uint_value(self, id_, path='', ex=False):
        return self.get_unsigned_integer(
            lambda res: self.raw_api.GetUIntValue(id_, path, res),
            error_msg=f'Failed to get uint value at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def set_uint_value(self, id_, value, path=''):
        self.verify_execution(
            self.raw_api.SetUIntValue(id_, path, value),
            error_msg=f'Failed to set uint value at '
                      f'{self.element_context(id_, path)}')

    def get_float_value(self, id_, path='', ex=False):
        return self.get_double(
            lambda res: self.raw_api.GetFloatValue(id_, path, res),
            error_msg=f'Failed to get float value at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def set_float_value(self, id_, value, path=''):
        self.verify_execution(
            self.raw_api.SetFloatValue(id_, path, value),
            error_msg=f'Failed to set uint value at '
                      f'{self.element_context(id_, path)}')

    def set_flag(self, id_, path, name, state):
        self.verify_execution(
            self.raw_api.SetFlag(id_, path, name, state),
            error_msg=f'Failed to set flag value at '
                      f'{self.flag_context(id_, path, name)} to {state}')

    def get_flag(self, id_, path, name):
        return self.get_bool(
            lambda res: self.raw_api.GetFlag(id_, path, name, res),
            error_msg=f'Failed to get flag value at: '
                      f'{self.flag_context(id_, path, name)}')

    def get_enabled_flags(self, id_, path=''):
        return self.get_string(
            lambda len_: self.raw_api.GetEnabledFlags(id_, path, len_),
            error_msg=f'Failed to get enabled flags at: '
                      f'{self.element_context(id_, path)}').split(',')

    def set_enabled_flags(self, id_, path, flags):
        self.verify_execution(
            self.raw_api.SetEnabledFlags(id_, path, ','.join(flags)),
            error_msg=f'Failed to set enabled flags at '
                      f'{self.element_context(id_, path)}')

    def get_all_flags(self, id_, path=''):
        return self.get_string(
            lambda len_: self.raw_api.GetAllFlags(id_, path, len_),
            error_msg=f'Failed to get all flags at: '
                      f'{self.element_context(id_, path)}')

    def get_enum_options(self, id_, path=''):
        return self.get_string(
            lambda len_: self.raw_api.GetEnumOptions(id_, path, len_),
            error_msg=f'Failed to get all enum options at '
                      f'{self.element_context(id_, path)}').split(',')

    def signature_from_name(self, name):
        return self.get_string(
            lambda len_: self.raw_api.SignatureFromName(name, len_),
            error_msg=f'Failed to get signature from name: {name}')

    def name_from_signature(self, sig):
        return self.get_string(
            lambda len_: self.raw_api.NameFromSignature(sig, len_),
            error_msg=f'Failed to get name from signature: {sig}')

    def get_signature_name_map(self):
        return self.get_dictionary(
            lambda len_: self.raw_api.GetSignatureNameMap(len_),
            error_msg=f'Failed to get signature name map')


class ElementValuesUtilsMethods:
    def safe_element_path(self, id_):
        '''
        Safely return a representative string of the given element path;
        protects from api errors (as this is typically used in output strings
        which may include error message strings)
        '''
        try:
            return self.path(self, id_)
        except self.XelibError:
            return str(id_)

    def element_context(self, id_, path=None):
        if path:
            return f'{self.safe_element_path(id_)}, "{path}"'
        else:
            return self.safe_element_path(id_)

    def flag_context(self, id_, path, name):
        return f'{self.safe_element_path(id_)}, "{path}\\{name}"'

    def array_item_context(self, id_, path, subpath, value):
        return f'{self.safe_element_path(id_)}, {path}, {subpath}, {value}'