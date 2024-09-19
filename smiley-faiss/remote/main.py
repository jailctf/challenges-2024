#!/usr/local/bin/python3
# slightly modified. original at https://github.com/facebookresearch/faiss/blob/main/contrib/rpc.py
import pickle
from io import BytesIO
import importlib

safe_modules = {
    'numpy',
    'numpy.core.multiarray',
}


class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Only allow safe modules.
        if "save" in name or "load" in name:
            return
        if module in safe_modules:
             import safernumpy
             import safernumpy.core.multiarray
             return getattr({"numpy": safernumpy, "numpy.core.multiarray": safernumpy.core.multiarray}[module], name)
        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                     (module, name))

if __name__ == "__main__":
    #RestrictedUnpickler(BytesIO().load()
    RestrictedUnpickler(BytesIO(bytes.fromhex(input(">")))).load()
