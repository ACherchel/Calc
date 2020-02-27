def Cut_Flat_to_Sheet(size_flat1, size_flat_2, size_order1, size_order_2):

    min_cut = 5
    max_cut = 1050
    min_flat = 420
    max_flat = 1100

    if not isinstance(size_flat1, int) or not isinstance(size_flat_2, int) or not isinstance(size_order1, int) or not isinstance(size_order_2, int):
        return  None

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

    if (length_flat // lenght_order) * (widht_flat // widht_order) == 0: # checking: order sheet must been < flat sheet
        return None
    if min_cut > lenght_order or lenght_order > max_cut or min_cut > widht_order or widht_order > max_cut:
        return None
    if min_flat > length_flat or length_flat > max_flat or min_flat > widht_flat or widht_order > max_flat:
        return None

    lenght_cur, widht_cur = length_flat, widht_flat
    lenght_cur1, widht_cur1 = length_flat, widht_flat
    cut_number_lengt, cut_number_widht, cut_number_lengt_widht, cut_number_widht_lenght = 0, 0, 0, 0

# Cutting - 4 variants
    while lenght_cur >= lenght_order:
        lenght_cur -= lenght_order
        cut_number_lengt += 1
    offcut1 = [length_flat, lenght_order, lenght_cur, widht_flat, 'll', cut_number_lengt]

    while widht_cur >= widht_order:
        widht_cur -= widht_order
        cut_number_widht += 1
    offcut2 = [widht_flat, widht_order, widht_cur, length_flat - lenght_cur, 'ww', cut_number_widht]

    if (lenght_cur1 // widht_order) != 0:
        while lenght_cur1 >= widht_order:
            lenght_cur1 -= widht_order
            cut_number_lengt_widht += 1
    offcut3 = [length_flat, widht_order, lenght_cur1, widht_flat, 'lw', cut_number_lengt_widht]

    if (widht_cur1 // lenght_order) != 0:
        while widht_cur1 >= lenght_order:
            widht_cur1 -= lenght_order
            cut_number_widht_lenght += 1
    offcut4 = [widht_flat, lenght_order,  widht_cur1, length_flat - lenght_cur1, 'wl', cut_number_widht_lenght]

    numbers_parts1 = cut_number_widht * cut_number_lengt
    numbers_parts2 = cut_number_lengt_widht * cut_number_widht_lenght
    if numbers_parts1 == 0: offcut1, offcut2 = None, None
    if numbers_parts2 == 0: offcut3, offcut4 = None, None
    return numbers_parts1, offcut1, offcut2, numbers_parts2, offcut3, offcut4


def Request_Flat_Sheet(lenght_order, widht_order, size1, size2):
    numbers = []
    offcuts_all = []
    offcut = []
    offcut_cur1 = []
    offcut_cur2 = []
    number_parts_app1 = 0
    number_parts_app2 = 0
    variant_cut_direct = ['direct']
    variant_cut_revers = ['revers']

    variant_cut = Cut_Flat_to_Sheet(size1, size2, lenght_order, widht_order)
    if variant_cut:
        variant_cut_direct.append(variant_cut[1:3])
        variant_cut_revers.append(variant_cut[3:])
    else:
        return None

    for i in variant_cut:
        if i != None and isinstance(i, list): offcut.append(i)
        if i != None and isinstance(i, int): numbers.append(i)

    for i in offcut[:2]:
        if i[2] != 0 and i[3] != 0:
            a = Cut_Flat_to_Sheet(i[2], i[3], lenght_order, widht_order)

            if a == None:
                offcut_cur1.append(i[2:4])

            if a != None:
                variant_cut_direct.append('turn')
                number_parts_app1 = a[0] + a[3]
                for i in a:
                    if i != None and isinstance(i, list):
                        offcut_cur1.append(i[2:4])
                        variant_cut_direct.append(i)

    for i in offcut[2:4]:
        if i[2] != 0 and i[3] != 0:
            a = Cut_Flat_to_Sheet(i[2], i[3], lenght_order, widht_order)

            if a == None:
                offcut_cur2.append(i[2:4])

            if a != None:
                variant_cut_revers.append('turn')
                number_parts_app2 = a[0] + a[3]
                for i in a:
                    if i != None and isinstance(i, list):
                        offcut_cur2.append(i[2:4])
                        variant_cut_revers.append(i)

    variant_direct_cut = variant_cut[0] + number_parts_app1
    variant_revers_cut = variant_cut[3] + number_parts_app2

    if variant_direct_cut >= variant_revers_cut:
        number_parts = variant_direct_cut
        offcuts_all.append(offcut_cur1)
        pattern_cut_list = variant_cut_direct

    else:
        number_parts = variant_revers_cut
        offcuts_all.append(offcut_cur2)
        pattern_cut_list = variant_cut_revers

    return number_parts, offcuts_all, pattern_cut_list


def calc():
    lenght_order, widht_order = 210, 310
    size1, size2 = 1050, 930
    t = Request_Flat_Sheet(lenght_order, widht_order, size1, size2)
    for i in range (100,1050, 100):
        lenght_order = i
        for k in range (100,900,100):
            widht_order= k
            t= Request_Flat_Sheet(lenght_order, widht_order, size1, size2)
            print(lenght_order, widht_order, size1, size2, t)
    print(lenght_order, widht_order, size1, size2, t)


calc()

# if __name__ == '__main__':
#
#     size1 = int(input('Original sheet size1  '))
#     size2 = int(input('Original sheet size2  '))
#     lenght_order = int(input('lenght order:  '))
#     widht_order = int(input('widht_order:  '))
#
#     t = Request_Flat_Sheet(lenght_order, widht_order, size1, size2)
