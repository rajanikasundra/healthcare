# Copyright (c) 2024, sigzen and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MedicalHistory(Document):
	def validate(self):
		existing_conditions = []
		for entry in self.medical_history:
			if entry.patient_condition in existing_conditions:
				frappe.throw(f"Duplicate condition found: {entry.patient_condition}")
			existing_conditions.append(entry.patient_condition)

