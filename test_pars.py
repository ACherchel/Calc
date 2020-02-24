def Cut_Flat_to_Sheet(size_flat1, size_flat_2, size_order1, size_order_2):
    if size_flat1 != size_flat_2:
        length_flat = max(size_flat1, size_flat_2)
        widht_flat = min(size_flat_2, size_flat1)
    else:
        length_flat, widht_flat = size_flat1, size_flat_2

    if size_order1 != size_order_2:
        lenght_order = max(size_order1, size_order_2)
        widht_order = min(size_order1, size_order_2)
    else:
        lenght_order, widht_order = size_order1, size_order_2

    if (length_flat // lenght_order) * (widht_flat // widht_order) == 0:
        return None

    lenght_cur, widht_cur = length_flat, widht_flat
    lenght_cur1, widht_cur1 = length_flat, widht_flat
    cut_number_lengt, cut_number_widht, cut_number_lengt_widht, cut_number_widht_lenght = 0, 0, 0, 0
    # offcut1, offcut2, offcut3, offcut4 = None, None, None, None
    # numbers_parts1 = None
    # numbers_parts2 = None

    while lenght_cur >= lenght_order:
        lenght_cur -= lenght_order
        cut_number_lengt += 1
    offcut1 = [length_flat, lenght_order, lenght_cur, widht_flat, 'll']

    while widht_cur >= widht_order:
        widht_cur -= widht_order
        cut_number_widht += 1
    # print(widht_cur, length_flat, lenght_cur)
    offcut2 = [widht_flat, widht_order, widht_cur, length_flat - lenght_cur, 'ww']

    if (lenght_cur1 // widht_order) != 0:
        while lenght_cur1 >= widht_order:
            lenght_cur1 -= widht_order
            cut_number_lengt_widht += 1
    offcut3 = [length_flat, widht_order, lenght_cur1, widht_flat, 'lw']

    if (widht_cur1 // lenght_order) != 0:
        while widht_cur1 >= lenght_order:
            widht_cur1 -= lenght_order
            cut_number_widht_lenght += 1
    # print(widht_cur1, length_flat, lenght_cur)
    offcut4 = [widht_flat, lenght_order,  widht_cur1, length_flat - lenght_cur1, 'wl']

    numbers_parts1 = cut_number_widht * cut_number_lengt
    numbers_parts2 = cut_number_lengt_widht * cut_number_widht_lenght
    if numbers_parts1 == 0: offcut1, offcut2 = None, None
    if numbers_parts2 == 0: offcut3, offcut4 = None, None
    return numbers_parts1, offcut1, offcut2, numbers_parts2, offcut3, offcut4


def Request_Flat_Sheet(lenght_order, widht_order, size1, size2):
    global pattern_cut_list
    numbers = []
    offcuts_all = []
    offcut = []
    offcut_app = []
    offcut_cur1 = []
    offcut_cur2 = []
    number_parts_app1 = 0
    number_parts_app2 = 0
    turn = None

    variant_cut = Cut_Flat_to_Sheet(size1, size2, lenght_order, widht_order)
    variant_cut_direct = variant_cut[0:3]
    variant_cut_revers = variant_cut[3:]

    print('variant_cut', variant_cut)
    for i in variant_cut:
        if i != None and isinstance(i, list): offcut.append(i)
        if i != None and isinstance(i, int): numbers.append(i)
    print('offcut ', offcut , ' numbers aooend ', numbers)

    for i in offcut[:2]:
        vid = 'direct'
        if i[2] != 0 and i[3] != 0:
            # print('i[0] i[1] -1 ', i[0], i[1])
            a = Cut_Flat_to_Sheet(i[2], i[3], lenght_order, widht_order)
            # print ('a1 ', a)

            if a == None:
                # print('a = NONE', a)
                offcut_cur1.append(i[2:4])

            if a != None:
                # print('a non None ', a)
                number_parts_app1 = a[0] + a[3]
                for i in a:
                    if i != None and isinstance(i, list): offcut_cur1.append(i[2:4])
                    if i != None and isinstance(i, list):
                        offcut_app.append(i)
                offcut_app.append(vid)
            turn = True
    print('offcut app ' , offcut_app)


    # print('offcur1 ' , offcut_cur1)
    #print('offcut2:4 ',offcut[2:4])
    for i in offcut[2:4]:
        vid = 'revers'
        if i[2] != 0 and i[3] != 0:
            # print ('i[2] i[1] - 2 ', i[2], i[3], 'numbers befor', number_parts_app2)
            a = Cut_Flat_to_Sheet(i[2], i[3], lenght_order, widht_order)
            # print ('a2 ', a)

            if a == None:
                # print('i_1 ', i)
                offcut_cur2.append(i[2:4])

            if a != None:
                number_parts_app2 = a[0] + a[3]
                for i in a:
                    if i != None and isinstance(i, list): offcut_cur2.append(i[2:4])
                    if i != None and isinstance(i, list):
                        offcut_app.append(i)
            offcut_app.append(vid)
            turn = True

            # print('i[0] i[1] -2 ', i[0], i[1], 'numbers after', number_parts_app2)

    # print('offcur2 ', offcut_cur2)

    if variant_cut[0] >= variant_cut[3]:
        #print('offcut_all befor ', offcuts_all)
        offcuts_all.append(offcut_cur1)
        #print('offcut_all after ', offcuts_all)
        #print('cur1 ', offcuts_all)

    elif variant_cut[0] < variant_cut[3]:
        offcuts_all.append(offcut_cur2)
        #print ('cur2')

    #if turn: offcuts_all.append('turn')

    # if (variant_cut[0] + number_parts_app1) > (variant_cut[3] + number_parts_app2):
    #     offcuts_all.append(offcut_cur1)
    # else:
    #     offcuts_all.append(offcut_cur2)

    number_parts = max((variant_cut[0] + number_parts_app1), (variant_cut[3] + number_parts_app2))
    # print(' number parts ', (variant_cut[0] + number_parts_app1), (variant_cut[3] + number_parts_app2))

    if offcut_app   and 'direct' in offcut_app:
        pattern_cut_list = [offcut[:2], offcut_app[:2]]

    print (offcut_app)
    if offcut_app:
        if 'revers' in offcut_app:
            print (' helow')
            pattern_cut_list = [offcut[2:4], offcut_app[2:4]]

    if turn: pattern_cut_list.append('turn')

    print('pattern ', pattern_cut_list)





    return number_parts, offcuts_all


def calc():
    lenght_order, widht_order = 600, 420
    size1, size2 = 1050, 930
    t = Request_Flat_Sheet(lenght_order, widht_order, size1, size2)
    # for i in range (100,900, 100):
    #     lenght_order = i
    #     for k in range (100,900,100):
    #         widht_order= k
    #         t= Request_Flat_Sheet(lenght_order, widht_order, size1, size2)
    #         print(lenght_order, widht_order, size1, size2, t)
    print(lenght_order, widht_order, size1, size2, t)


calc()
