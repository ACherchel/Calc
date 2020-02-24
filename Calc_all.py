prise_roll_hrom = {220:17000, 250:16500, 310:16000, 450:16000}
gear = [42,60,64,70,84,90,110]
losses = 0.03
weigt_roll_hrom = [840,600,620,640,700,900]
sallary_flat_hrom = 330 # за за тонну
sallary_cut = 2.5
cargo_waste = 1700 # за тонну

def Roll_Flat_To_Sheet(type='H1', lenght=1050, density=220, widht=930,weigt=1000):
    cost = prise_roll_hrom[density]
    weigt_flat_sheets = round(((density/1e3)*widht*lenght/1e6),4)
    count_sheets_flat = round(weigt*(1-losses)/weigt_flat_sheets)
    cost_flat_sheet = round((cost+ (weigt/1000*(sallary_flat_hrom+cargo_waste)))/count_sheets_flat, 2)
    flat = {'type':type, 'density': density, 'size':(lenght, widht), 'count_sheets': count_sheets_flat,
            'cost_sheet': cost_flat_sheet, 'weigt_flat_sheets': weigt_flat_sheets }
    return flat


def Flat_To_Sheets (data=None):
    # Прогонка полученных параметров через ф-ю Roll_Flat_To_Sheet()
    lenght_order, widht_order, quantity = data
    cut_description=[]
    flat = Roll_Flat_To_Sheet()
    lenght_flat, widht_flat = flat['size']

    # Подбор варианта порезки/ загрузка патерна порезки
    number_parts_residue = 0
    number_of_cutting = 0
    lenght_order, widht_order= 320, 210 # temp

    cut_ll_ww = [lenght_flat//lenght_order, widht_flat//widht_order,
          lenght_flat % lenght_order, widht_flat, widht_flat % widht_order, lenght_flat]
    cut_lw_wl = [lenght_flat//widht_order, widht_flat//lenght_order,
            lenght_flat%widht_order,widht_flat, widht_flat%lenght_order, lenght_flat]
    print (cut_ll_ww, cut_lw_wl)



    # Проверка исключения: "порезка с переворотом"
    cutting_residue_max = max(cut['ll_ww'][2], cut['ll_ww'][3],cut['lw_wl'][2], cut['lw_wl'][2], cut['lw_wl'][3])

    if cutting_residue_max >= widht_order:
        number_parts_residue = cutting_residue_max//widht_order
    elif cutting_residue_max >= lenght_order:
        number_parts_residue = cutting_residue_max//lenght_order
    print(f'Патерн порезки: %s' %cut)


    cut_variant_1 = cut['ll_ww'][0]*cut['ll_ww'][1]
    cut_variant_2 = cut['lw_wl'][0]*cut['lw_wl'][1]
    s1 = cut['ll_ww'][2]*widht_flat + cut['ll_ww'][3]*lenght_flat
    s2 = cut['lw_wl'][2]*widht_flat + cut['lw_wl'][3]*lenght_flat
    print(cut_variant_1, cut_variant_2, s1, s2)
    if cut_variant_1 == cut_variant_2 and number_parts_residue == 0:
        if s1 > s2:
            cut_description.append('ll_ww')
        else:
            cut_description.append('lw_wl')
    elif  cut_variant_1 > cut_variant_2 and number_parts_residue == 0:
        cut_description.append('ll_ww')
    elif cut_variant_1 > cut_variant_2 and number_parts_residue == 0:
        cut_description.append('lw_wl')
    else:
        cut_description.append('turn')
    count_parts = max (cut_variant_2, cut_variant_1) + number_parts_residue
    print (count_parts, cut_description)




  #  cutting_part_max+=numder_of_cutting_residue


     # вычисление параметров: кол-во листов, вес заказа, стоимость
    #quantity_sheets_order = (quantity/count_flat_sheets)
    #cost_order = quantity_sheets_order*flat['cost_sheet']
    #weigt_order = (quantity/count_flat_sheets)*flat['weigt_flat_sheets']

    # выгрузка данных в return
    #order_data = {'type': type, 'density':density, 'size': (size_flat_big,widht),
   #               'quantity':quantity, 'cost':cost_order, 'weigt': weigt_order}
    #return order_data


#t= Roll_Flat_To_Sheet('c')
#print (t)

s= Flat_To_Sheets([1050,930,1000])
#print (s)
