import frappe

def validate(doc,event):
    
    if doc.has_serial_no == 1 and doc.item_name and doc.item_group and doc.stock_uom :
        
        item_name = doc.item_name
        item_group = doc.item_group
        uom = doc.stock_uom
        
        name = item_name.split()
        group = item_group.split()
        uom = uom.split()
        words = name + group + uom
        
        initials = ''.join(word[0] for word in words)
        doc.serial_no_series = f"{initials}.####"
    
    