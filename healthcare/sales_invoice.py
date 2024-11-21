import frappe
def before_save(doc,event):
    doc.additional_discount_percentage = 5
    
    total = doc.rounded_total
    insurance_percentage = doc.custom_insurance_percentage or 0  
    insurance_amount = (insurance_percentage / 100) * total
    net_payable = total - insurance_amount
    
    # if net_payable < 0:
    #     frappe.throw("Insurance coverage exceeds total amount.")

    doc.net_total = net_payable
    doc.rounded_total = round(net_payable)  
    doc.grand_total = net_payable
    doc.outstanding_amount = net_payable
    
