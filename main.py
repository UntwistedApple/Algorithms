# -*- coding: UTF-8 -*-

from Level import Main as level

if __name__ == '__main__':
    try:
        level.main()
    except KeyboardInterrupt:
        print('Aborted by keyboard command')
