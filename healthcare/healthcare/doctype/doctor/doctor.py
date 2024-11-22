# Copyright (c) 2024, sigzen and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Doctor(Document):
    
	
	def before_save(self):
		
		if self.is_new() and not frappe.db.exists("User", self.email):
			
			user = frappe.new_doc("User")
			user.email = self.email
			user.first_name = self.name1
			user.enabled = 1
			user.append("roles", {"role": "Doctor"})
			user.save(ignore_permissions=True)

			frappe.msgprint(f"User {self.email} created with the Doctor role.")
