# -*- coding: UTF-8 -*-

from Level import Main as level


if __name__ == '__main__':
    try:
        level.main()
    except KeyboardInterrupt:
        print('Aborted by keyboard command')
    except Exception as e:
        input('An error occured!\nOriginal Error message:\n%s\nPress enter to exit.' % (
                '\n' + str(e) + '\n'))
        raise

# TODO Alles okay mit den schnellsten Linien?

# TODO Windows venv!!!!!
