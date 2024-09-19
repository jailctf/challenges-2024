# get and call

solve1.py contains a solution that calls `builtins.breakpoint`

solve2.py contains a solution that calls `sys.breakpointhook`

the premise here is that we can do arbitrary getattr and call functions with no arguments, but we cant do anything more

the trick here is to deviate from the standard no builtins escape of `object.__subclasses__()[num].__init__.__globals__` and instead use popitem to traverse module dictionaries

one gets the last item of a dict using `dict_obj.values().__reversed__().__next__()`

additionally, one gets the last item of a list using `list_obj.__reversed__().__next__()`

ok there was also an unintended where you could get the iter function by using `__reduce__` on some iter object and then use the `__self__` of that to get to builtins and win
