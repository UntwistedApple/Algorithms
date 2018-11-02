

def read():
    keys = dict()
    f = open('config.ini')
    data = f.readlines()
    f.close()

    if data[-1:][0] != '\n':
        raise ImportError('There has to be a new line at the end of the config.ini file!')

    for line in data:
        if line[0] in '#\n':
            continue

        temp = ''
        keyname = None

        for char in line:
            if char == '=':
                keyname = temp
                temp = ''
            elif char in '#\n':

                if temp.isdecimal():
                    temp = int(temp)
                elif temp.isdigit():
                    temp = float(temp)

                keys[keyname] = temp

                if char == '#':
                    break
            else:
                temp += char
    return keys


if __name__ == '__main__':
    print(read())