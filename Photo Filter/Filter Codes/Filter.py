
# return img, nested list
def read_ppm_file(f):
    fp = open(f)
    fp.readline()  # reads P3 (assume it is P3 file)
    lst = fp.read().split()
    n = 0
    n_cols = int(lst[n])
    n += 1
    n_rows = int(lst[n])
    n += 1
    max_color_value = int(lst[n])
    n += 1
    img = []
    for r in range(n_rows):
        img_row = []
        for c in range(n_cols):
            pixel_col = []
            for i in range(3):
                pixel_col.append(int(lst[n]))
                n += 1
            img_row.append(pixel_col)
        img.append(img_row)
    fp.close()
    return img, max_color_value


# Works
def img_printer(img):
    row = len(img)
    col = len(img[0])
    cha = len(img[0][0])
    for i in range(row):
        for j in range(col):
            for k in range(cha):
                print(img[i][j][k], end=" ")
            print("\t|", end=" ")
        print()


filename = input()
operation = int(input())


img = read_ppm_file(filename)[0]
rgb = read_ppm_file(filename)[1]

if operation == 1:
    #getting new maximum and minimum values
    minimum = int(input())
    maximum = int(input())

    #setting new values for rgb values
    for a in range(len(img)):
        for b in range(len(img[a])):
            for c in range(len(img[a][b])):
                img[a][b][c] = ((img[a][b][c] - 0) / (rgb - 0)) * (maximum - minimum) + minimum
                img[a][b][c] = round(img[a][b][c], 4)


    img_printer(img)

if operation == 2:

    for a in range(3):
        #calculating mean
        kthchannelmean = 0
        kthchannelderivation = 0
        for i in range(len(img)):
            for j in range(len(img[i])):
                kthchannelmean = kthchannelmean + img[i][j][a]
        kthchannelmean = kthchannelmean / (len(img)*len(img[0]))
        #calculating derivation
        for i in range(len(img)):
            for j in range(len(img[i])):
                kthchannelderivation = kthchannelderivation + ((img[i][j][a]-kthchannelmean) ** 2)
        kthchannelderivation =(((kthchannelderivation / (len(img)*len(img[0]))) ** (1/2)) + 10**-6)
        #normalized versions
        for i in range(len(img)):
            for j in range(len(img[i])):

                normalized = (img[i][j][a] - kthchannelmean)/kthchannelderivation
                img[i][j][a] = round(normalized,4)

    img_printer(img)

if operation == 3:

    #averaging
    for a in range(len(img)):
        for b in range(len(img[a])):

            ort =(img[a][b][0] + img[a][b][1] + img[a][b][2] )/3
            ort = int(ort)
            img[a][b][0] = ort
            img[a][b][1] = ort
            img[a][b][2] = ort

    img_printer(img)

if operation == 4:

    filename = input()
    stride = int(input())

    #opening filter and making list
    f = open(filename,'r')
    list = []
    for lines in f:
        lines = lines.split()
        list = list + lines
    f.close()

    for i in range(len(list)):
        list[i] = float(list[i])
    starternum = int((((len(list)**(1/2))-1)/2))


    NewImgList = []
    #calculating the new value of the number with function
    def newValFinder(x,a,b,c):
        step = 0
        val = 0
        for i in range(2 * x + 1):
            for j in range(2 * x + 1):
                val += img[a-x+i][b-x+j][c] * list[step]
                step += 1

        val = int(val)

        return val
    #implementing new value for all pixels
    for a in range(starternum,len(img)-starternum,stride):
        img_row = []
        for b in range(starternum,len(img[a])-starternum,stride):
            pixel_col = []
            for c in range(3):
                newVal1 = newValFinder(starternum,a,b,c)
                if newVal1 > rgb:
                    newVal1 = rgb
                if newVal1 < 0:
                    newVal1 = 0
                pixel_col.append(newVal1)

            img_row.append(pixel_col)
        NewImgList.append(img_row)
    img_printer(NewImgList)

if operation == 5:
    filename = input()
    stride = int(input())
    # opening filter and making list
    f = open(filename,'r')
    list = []
    for lines in f:
        lines = lines.split()
        list = list + lines
    f.close()


    for i in range(len(list)):
        list[i] = float(list[i])
    starternum = int((((len(list) ** (1 / 2)) - 1) / 2))

    #using padding and making the list bigger
    img2 = []
    for a in range(-starternum, len(img)+starternum):
        img_row = []
        for b in range(-starternum, len(img)+starternum):
            pixel_col = []
            for i in range(3):
                if 0 <= a < len(img) and 0 <= b < len(img):
                    pixel_col.append(img[a][b][i])
                else:
                    pixel_col.append(0)

            img_row.append(pixel_col)
        img2.append(img_row)


    # calculating the new value of the number with function
    def newValFinder(x, a, b, c):
        step = 0
        val = 0
        for i in range(2 * x + 1):
            for j in range(2 * x + 1):
                val += img2[a - x + i][b - x + j][c] * list[step]
                step += 1
        val = int(val)
        return val


    # implementing new value for all pixels
    NewImgList = []
    for a in range(starternum,len(img2)-starternum,stride):
        img_row = []
        for b in range(starternum,len(img2)-starternum,stride):
            pixel_col = []
            for c in range(3):
                newVal1 = newValFinder(starternum,a,b,c)
                if newVal1 > rgb:
                    newVal1 = rgb
                if newVal1 < 0:
                    newVal1 = 0
                pixel_col.append(newVal1)

            img_row.append(pixel_col)
        NewImgList.append(img_row)
    img_printer(NewImgList)

if operation == 6:
    rng = int(input())
    # making a checker and make sure a value is changed only once
    controller = []
    for r in range(len(img)):
        img_row = []
        for c in range(len(img)):
            img_row.append(0)
        controller.append(img_row)

    #function for controlling the status of chechker(NOT USED)
    def control_printer(img):
        row = len(img)
        col = len(img[0])
        for i in range(row):
            for j in range(col):
                print(img[i][j], end=" ")

            print()
    #main function that makes the recurcion
    def fun(x=0,y=0):

        if x > len(img)-1 or y > len(img)-1 or x < 0 or y < 0:
            return

        if len(img) % 2 == 0:
            if x == 0 and y == len(img)-1:
                controller[x][y] = 1
                return
        if len(img) % 2 == 1:
            if x == len(img) - 1 and y == len(img)-1:
                controller[x][y] = 1
                return


        #When it comes to the bottom and top, make sure to switch to the right
        if (x == len(img)-1 and y % 2 == 0) or (x == 0 and y % 2 == 1):
            dif0 = img[x][y][0] - img[x][y+1][0]
            dif1 = img[x][y][1] - img[x][y+1][1]
            dif2 = img[x][y][2] - img[x][y+1][2]
            if dif0 < 0:
                dif0 = dif0 * (-1)
            if dif1 < 0:
                dif1 = dif1 * (-1)
            if dif2 < 0:
                dif2 = dif2 * (-1)
            if dif0 < rng and dif1 < rng and dif2 < rng:
                img[x][y+1][0] = img[x][y][0]
                img[x][y+1][1] = img[x][y][1]
                img[x][y+1][2] = img[x][y][2]
            controller[x][y] = 1

        #apply top to bottom change when y is even
        if x < len(img) -1 and y % 2 == 0  :
            if controller[x][y]==1:
                return
            dif0 = img[x][y][0] - img[x+1][y][0]
            dif1 = img[x][y][1] - img[x+1][y][1]
            dif2 = img[x][y][2] - img[x+1][y][2]
            if dif0 < 0:
                dif0 = dif0 * (-1)
            if dif1 < 0:
                dif1 = dif1 * (-1)
            if dif2 < 0:
                dif2 = dif2 * (-1)
            if dif0 < rng and dif1 < rng and dif2 < rng:
                img[x+1][y][0] = img[x][y][0]
                img[x+1][y][1] = img[x][y][1]
                img[x+1][y][2] = img[x][y][2]

            controller[x][y] = 1
        # apply bottom to top change when y is odd
        if x > 0 and y % 2 == 1 :
            if controller[x][y]==1:
                return
            dif0 = img[x][y][0] - img[x-1][y][0]
            dif1 = img[x][y][1] - img[x-1][y][1]
            dif2 = img[x][y][2] - img[x-1][y][2]
            if dif0 < 0:
                dif0 = dif0 * (-1)
            if dif1 < 0:
                dif1 = dif1 * (-1)
            if dif2 < 0:
                dif2 = dif2 * (-1)
            if dif0 < rng and dif1 < rng and dif2 < rng:
                img[x-1][y][0] = img[x][y][0]
                img[x-1][y][1] = img[x][y][1]
                img[x-1][y][2] = img[x][y][2]
            controller[x][y] = 1



        fun(x + 1, y)
        fun(x - 1, y)
        fun(x , y + 1)
        fun(x , y - 1)

        return img

    image = fun()
    img_printer(image)

if operation == 7:
    rng = int(input())
    # making a checker and make sure a value is changed only once
    controller = []
    for r in range(len(img)):
        img_row = []
        for c in range(len(img)):
            pixel_col = []
            for i in range(3):
                pixel_col.append(0)
            img_row.append(pixel_col)
        controller.append(img_row)


    # main function that makes the recurcion
    def fun(x=0, y=0,z=0):

        if z == -1 or z == 3 or x == len(img) or y == len(img) or x == -1 or y == -1:
            return
        #implementing changes when channel is red or blue
        if z == 0 or z == 2:
            # When it comes to the bottom or top, make sure to switch to the right
            if (x == len(img) - 1 and y % 2 == 0) or (x == 0 and y % 2 == 1):
                if y != len(img) - 1:
                    if controller[x][y][z] == 1:
                        return
                    dif0 = img[x][y][z] - img[x][y + 1][z]

                    if dif0 < 0:
                        dif0 = dif0 * (-1)

                    if dif0 < rng:
                        img[x][y + 1][z] = img[x][y][z]
                controller[x][y][z] = 1

            # apply top to bottom change when y is even
            if x < len(img) - 1 and y % 2 == 0:

                if controller[x][y][z] == 1:
                    return

                dif0 = img[x][y][z] - img[x + 1][y][z]
                if dif0 < 0:
                    dif0 = dif0 * (-1)

                if dif0 < rng:
                    img[x + 1][y][z] = img[x][y][z]
                controller[x][y][z] = 1

            # apply bottom to top change when y is odd
            if x > 0 and y % 2 == 1:
                if controller[x][y][z] == 1:
                    return
                dif0 = img[x][y][z] - img[x - 1][y][z]

                if dif0 < 0:
                    dif0 = dif0 * (-1)

                if dif0 < rng:
                    img[x - 1][y][z] = img[x][y][z]
                controller[x][y][z] = 1

        # implementing changes when channel is green
        if z == 1:
            # When it comes to the bottom or top, make sure to switch to the right
            if (x == len(img) - 1 and y % 2 == 1) or (x == 0 and y % 2 == 0):
                if y != 0:
                    if controller[x][y][z] == 1:
                        return
                    dif0 = img[x][y][z] - img[x][y - 1][z]

                    if dif0 < 0:
                        dif0 = dif0 * (-1)

                    if dif0 < rng:
                        img[x][y - 1][z] = img[x][y][z]

                    controller[x][y][z] = 1
            # apply bottom to top change when y is even
            if x > 0 and y % 2 == 0:
                if controller[x][y][z] == 1:
                    return img
                dif0 = img[x][y][z] - img[x - 1][y][z]
                if dif0 < 0:
                    dif0 = dif0 * (-1)

                if dif0 < rng:
                    img[x - 1][y][z] = img[x][y][z]

                controller[x][y][z] = 1
            # apply top to bottom change when y is odd
            if x < len(img) - 1 and y % 2 == 1:
                if controller[x][y][z] == 1:
                    return img
                dif0 = img[x][y][z] - img[x + 1][y][z]

                if dif0 < 0:
                    dif0 = dif0 * (-1)

                if dif0 < rng:
                    img[x + 1][y][z] = img[x][y][z]
                controller[x][y][z] = 1




        fun(x + 1, y, z)
        fun(x - 1, y, z)
        fun(x , y + 1, z)
        fun(x , y - 1, z)
        fun(x, y, z + 1)
        fun(x, y, z -1)




    fun()
    img_printer(img)
