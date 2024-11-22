
import frappe
from frappe.model.document import Document

def create_purchase_order_from_material_request(self, method):
    
    material_request = frappe.get_doc('Material Request', self.name)
    
    
    for item in material_request.items:
        item_doc = frappe.get_doc('Item', item.item_code)
        
    
        if hasattr(item_doc, 'reorder_level'):
            if item.qty <= item_doc.reorder_level:
                purchase_order = frappe.new_doc('Purchase Order')
                purchase_order.supplier = material_request.supplier
                purchase_order.append('items', {
                    'item_code': item.item_code,
                    'qty': item.qty,  
                    'schedule_date': frappe.utils.nowdate(),
                })
                purchase_order.save()
                frappe.db.commit()
                return purchase_order.name
        else:
            frappe.log_error(f"Reorder level is not defined for item: {item.item_code}", "Material Request Error")
    
    return None
