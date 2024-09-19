# this one can be optimized for sure

banned = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ`~=+[]{}|!@#$%&()>< "


def check(x):
    return all(i not in banned and ord(i) < 128 for i in x)


MAX = 4
seen_classes = set()
best_way = {}
alldunders = open("dunders.txt").read().splitlines(keepends=False)


def recurs(oname, obj, attrs, depth=0):
    if isinstance(obj, bool):
        obj = int(obj)
    if depth == MAX:
        return
    if not check(oname):
        return
    if isinstance(obj, int):
        if obj not in best_way or len(best_way[obj]) > len(oname):
            best_way[obj] = oname
        print(oname, obj)
        return
    for attr in attrs:
        try:
            new_obj = getattr(obj, attr)
            if isinstance(new_obj, int):
                if not check(attr):
                    continue
                if new_obj not in best_way or len(best_way[new_obj]) > len(oname + "." + attr):
                    best_way[new_obj] = oname + "." + attr
                print(oname + "." + attr, new_obj)
                continue
            recurs(f'{oname}.{attr}', new_obj, alldunders, depth+1)
        except:
            pass


def main():
    objnames = dir(__builtins__) + ['check'] + ['__debug__']
    objnames = [name for name in objnames if check(name)]
    for objname in objnames:
        obj = eval(objname)
        objattrs = alldunders
        recurs(objname, obj, objattrs)
    print(best_way)


if __name__ == "__main__":
    main()
