// Copyright (c) 2024, sigzen and contributors
// For license information, please see license.txt

frappe.ui.form.on("Patient", {
	refresh(frm) {

        if (frm.doc.docstatus == 1) { // Check if the Patient document is submitted
            frm.add_custom_button(
                "Make Payment", // Label for the button
                function () {
                    // Redirect to Payment Entry creation
                    frappe.model.open_mapped_doc({
                        method: "healthcare.payment_entry.create_payment_entry", // Backend method
                        frm: frm
                    });
                },
                "Actions" // Adds the button under the "Actions" menu
            );
        }

	},
});
