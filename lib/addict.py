from inspect import isgenerator
import re
import copy


class Dict(dict):
    def __init__(self, *args, **kwargs):
        for arg in args:
            if not arg:
                continue
            elif isinstance(arg, Dict):
                for key, val in arg.to_dict().items():
                    self[key] = self._hook(val)
            elif isinstance(arg, dict):
                for key, val in arg.items():
                    self[key] = self._hook(val)
            elif isinstance(arg, tuple) and (not isinstance(arg[0], tuple)):
                self[arg[0]] = self._hook(arg[1])
            elif isinstance(arg, (list, tuple)) or isgenerator(arg):
                for key, val in arg:
                    self[key] = self._hook(val)
            else:
                raise TypeError("Dict does not understand "
                                "{0} types".format(type(arg)))

        for key, val in kwargs.items():
            self[key] = val

    def __setattr__(self, name, value):
        if hasattr(Dict, name):
            raise AttributeError("'Dict' object attribute "
                                 "'{0}' is read-only".format(name))
        else:
            self[name] = value

    def __setitem__(self, name, value):
        super(Dict, self).__setitem__(name, value)

    @classmethod
    def _hook(cls, item):
        if isinstance(item, Dict):
            return item
        if isinstance(item, dict):
            return cls(item)
        elif isinstance(item, (list, tuple)):
            return type(item)(cls._hook(elem) for elem in item)
        return item

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __getitem__(self, name):
        if name not in self:
            self[name] = Dict()
        else:
            self[name] = self._hook(super(Dict, self).__getitem__(name))
        return super(Dict, self).__getitem__(name)

    def __delattr__(self, name):
        del self[name]

    _re_pattern = re.compile('[a-zA-Z_][a-zA-Z0-9_]*')

    def __dir__(self):
        dict_keys = []
        for k in self.keys():
            if isinstance(k, str):
                m = self._re_pattern.match(k)
                if m:
                    dict_keys.append(m.string)

        obj_attrs = list(dir(Dict))

        return dict_keys + obj_attrs

    def _ipython_display_(self):
        print(str(self))    # pragma: no cover

    def _repr_html_(self):
        return str(self)

    def prune(self, prune_zero=False, prune_empty_list=True):
        for key, val in list(self.items()):
            if ((not val) and ((val != 0) or prune_zero) and
                    not isinstance(val, list)):
                del self[key]
            elif isinstance(val, Dict):
                val.prune(prune_zero, prune_empty_list)
                if not val:
                    del self[key]
            elif isinstance(val, (list, tuple)):
                new_iter = self._prune_iter(val, prune_zero, prune_empty_list)
                if (not new_iter) and prune_empty_list:
                    del self[key]
                else:
                    if isinstance(val, tuple):
                        new_iter = tuple(new_iter)
                    self[key] = new_iter

    @classmethod
    def _prune_iter(cls, some_iter, prune_zero=False, prune_empty_list=True):
        new_iter = []
        for item in some_iter:
            if item == 0 and prune_zero:
                continue
            elif isinstance(item, Dict):
                item.prune(prune_zero, prune_empty_list)
                if item:
                    new_iter.append(item)
            elif isinstance(item, (list, tuple)):
                new_item = type(item)(
                    cls._prune_iter(item, prune_zero, prune_empty_list))
                if new_item or not prune_empty_list:
                    new_iter.append(new_item)
            else:
                new_iter.append(item)
        return new_iter

    def to_dict(self):
        base = {}
        for key, value in self.items():
            if isinstance(value, type(self)):
                base[key] = value.to_dict()
            elif isinstance(value, (list, tuple)):
                base[key] = type(value)(
                    item.to_dict() if isinstance(item, type(self)) else
                    item for item in value)
            else:
                base[key] = value
        return base

    def copy(self):
        return Dict(self.to_dict())

    def __deepcopy__(self, memo):
        y = self.__class__()
        memo[id(self)] = y
        for key, value in self.items():
            y[copy.deepcopy(key, memo)] = copy.deepcopy(value, memo)
        return y

    def update(self, *args, **kwargs):
        other = {} 
        if args:
            if len(args) > 1:
                raise TypeError()
            other.update(args[0])
        other.update(kwargs)
        for k, v in other.items():
            if ((k not in self) or
                (not isinstance(self[k], dict)) or
                (not isinstance(v, dict))):
                self[k] = v
            else:
                self[k].update(v)

    def __getnewargs__(self):
        return tuple(self.items())

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)