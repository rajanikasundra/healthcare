frappe.ui.form.on('Customer', {
    onload: function (frm) {
        frm.set_df_property('customer_type', 'hidden', 1);
        frm.set_df_property('customer_type', 'reqd', 0);
    },


    refresh: function(frm){
            // for customer to appointment
            frm.add_custom_button(__('Create Appointment'), function () {
                const customer_name = encodeURIComponent(frm.doc.name);
                window.location.href = `/app/appointment/new-appointment-1?customer_name=${customer_name}`;
            }, __("Actions"));

    },

});

















// refresh : function(frm) {

    //     if (frm.doc.docstatus == 0) { 
    //         frm.add_custom_button(
    //             "Sales Invoice For Payment", 
    //             function () {
    //                 // Redirect to Payment Entry creation
    //                 frappe.model.open_mapped_doc({
    //                     method: "healthcare.payment_entry.create_payment_entry", // Backend method
    //                     frm: frm
    //                 });
    //             },
    //             "Actions" // Adds the button under the "Actions" menu
    //         );
    //     }

	// },