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

