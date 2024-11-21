// frappe.ui.form.on('Sales Invoice', {
    

//     validate: function (frm) {

//         let insurance_amount = (frm.doc.custom_insurance_percentage / 100) * frm.doc.total;
//         frm.doc.grand_total = frm.doc.grand_total - insurance_amount;

//         // Show a message if insurance covers everything
//         if (frm.doc.grand_total <= 0) {
//             frappe.msgprint(__('Insurance coverage exceeds or matches total amount.'));
//             frm.doc.grand_total = 0;
//         }
//     }



// });
