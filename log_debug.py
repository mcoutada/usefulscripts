import funcy
import sys
import logging

def main(args):

    is_debug = True if args[0:1] == ["DEBUG"] else False

    logging.basicConfig(level=logging.DEBUG if is_debug else logging.INFO)

    @funcy.log_calls(logging.debug)
    def func1(args):
        logging.info("Starting 1")
        return sum(args)

    @funcy.log_durations(logging.debug)
    def func2(args):
        logging.info("Starting 2")
        return sum(args)

    @funcy.log_errors(logging.debug)
    def func3(args):
        logging.info("Starting 3")
        a = 1 / 0
        return sum(args)

    func1([1,2,3])
    func2([1,2,3])
    func3([1,2,3])


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)

exit()

########################################################################################

# Sin DEBUG
# python test1.py

# log:
# INFO:root:Starting 1
# INFO:root:Starting 2
# INFO:root:Starting 3

# Con DEBUG
# python test1.py DEBUG

# log:
# DEBUG:root:Call func1([1, 2, 3])
# INFO:root:Starting 1
# DEBUG:root:-> 6 from func1([1, 2, 3])
# INFO:root:Starting 2
# DEBUG:root:   99.66 mks in func2([1, 2, 3])
# INFO:root:Starting 3
# DEBUG:root:Traceback (most recent call last):
#   File "/home/mcoutada/.local/lib/python3.10/site-packages/funcy/debug.py", line 119, in inner
#     return func(*args, **kwargs)
#   File "/home/mcoutada/alkemy/OT303-python/SPRINT02/OT303-38/test1.py", line 25, in func3
#     a = 1 / 0
# ZeroDivisionError: division by zero
#     raised in func3([1, 2, 3])



# también se pueden combinar los decoradores
#     @funcy.log_errors(logging.debug)
#     @funcy.log_durations(logging.debug)
#     @funcy.log_calls(logging.debug)
#     def func1(args):
#         logging.info("Starting 1")
#         return sum(args)
