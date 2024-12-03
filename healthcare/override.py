import frappe
import random
import string
from frappe.utils import cint, now
from erpnext.stock.serial_batch_bundle import SerialBatchCreation

class customSerialBatchCreation(SerialBatchCreation):
    print("########################")
    def custom_get_auto_created_serial_nos(self):
        sr_nos = []  # List to store generated serial numbers
        serial_nos_details = []  # List to store details for bulk insert
        
        abc = frappe.get_doc('Settings')
        check = abc.set_random_serial_no
        print("++++++++++++++++++++",check)
        # if check :
            
        # 	for _i in range(cint(qty)):
        # 		random = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        # 		print("*************",random)
        # 		serial_nos.append(get_new_serial_number(random))

        # 	print("_____________-----------------------",serial_nos)
        # 	return serial_nos
      
      
        
        voucher_no = ""
        if self.get("voucher_no"):
            voucher_no = self.get("voucher_no")

        # Generate serial numbers for the specified quantity
        for _ in range(abs(cint(self.actual_qty))):
            # Check if random serial numbers are enabled in Settings
            settings_doc = frappe.get_doc("Settings")
            if settings_doc.set_random_serial_no:
                # Generate a random 6-character alphanumeric string
                random_serial = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            else:
                # Generate serial number using Serial No Series
                random_serial = frappe.model.naming.make_autoname(self.serial_no_series, "Serial No")

            # Append the generated serial number to the list
            sr_nos.append(random_serial)

            # Prepare details for bulk insert
            serial_nos_details.append(
                (
                    random_serial,
                    random_serial,
                    now(),
                    now(),
                    frappe.session.user,
                    frappe.session.user,
                    self.warehouse,
                    self.company,
                    self.item_code,
                    self.item_name,
                    self.description,
                    "Active",
                    voucher_no,
                    self.batch_no,
                )
            )

        # Perform bulk insert into the Serial No DocType
        if serial_nos_details:
            fields = [
                "name",
                "serial_no",
                "creation",
                "modified",
                "owner",
                "modified_by",
                "warehouse",
                "company",
                "item_code",
                "item_name",
                "description",
                "status",
                "purchase_document_no",
                "batch_no",
            ]
            frappe.db.bulk_insert("Serial No", fields=fields, values=serial_nos_details)

        # Return the list of generated serial numbers
        return sr_nos