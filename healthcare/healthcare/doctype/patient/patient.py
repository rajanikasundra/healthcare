# Copyright (c) 2024, sigzen and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, date_diff
class Patient(Document):
	def validate(self):
		print("abc")
		if date_diff(today(), self.date_of_birth) <= 0:
			frappe.throw("The patient's date of birth must be in the past.")
   
   
		# medical history condition not duplicate entry
		existing_conditions = []
		for entry in self.medical_history:
			if entry.patient_condition in existing_conditions:
				frappe.throw(f"Duplicate condition found in medical history: {entry.patient_condition}")
			existing_conditions.append(entry.patient_condition)

