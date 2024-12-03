import frappe
def before_save(doc, event):
    if doc.is_new() and not frappe.db.exists("User", doc.customer_email):
			
        user = frappe.new_doc("User")
        user.email = doc.customer_email
        user.first_name = doc.custom_patient
        user.enabled = 1
        user.append("roles", {"role": "Patient"})
        user.save(ignore_permissions=True)

        frappe.msgprint(f"User {doc.customer_email} created with the Patient role.")
    
    
    # user permission for doctor
    if frappe.db.exists("User", doc.custom_doctor_email):
        create_user_permission(
            user=doc.custom_doctor_email,
            allow="Customer",
            for_value=doc.custom_patient
        )

    # Set User Permission for the Patient
    if frappe.db.exists("User", doc.customer_email):
        create_user_permission(
            user=doc.customer_email,
            allow="Customer",
            for_value=doc.custom_patient
        )

def create_user_permission(user, allow, for_value):
    """
    Create a new User Permission if it doesn't already exist.
    """
    existing_permission = frappe.db.exists(
        "User Permission",
        {
            "user": user,
            "allow": allow,
            "for_value": for_value
        }
    )
    if not existing_permission:
        user_permission = frappe.new_doc("User Permission")
        user_permission.user = user
        user_permission.allow = allow
        user_permission.for_value = for_value
        user_permission.save(ignore_permissions=True)
    else : frappe.msgprint("already exists permission")
    
    
    
    
    
    
    
    
    
    
    
    
        
        

    
    

  
    
    
from erpnext.crm.doctype.appointment.appointment import Appointment
class CustomAppoinment(Appointment):
    def send_confirmation_email(self):
        verify_url = self._get_verify_url()
        template = "confirm_appointment"
        args = {
			"link": verify_url,
			"site_url": frappe.utils.get_url(),
			"full_name": self.custom_patient,
		}
        frappe.sendmail(
			recipients=[self.customer_email],
			template=template,
			args=args,
			subject=("Appointment Confirmation"),
		)
        if frappe.session.user == "Guest":
            frappe.msgprint(("Please check your email to confirm the appointment"))
        else:
            frappe.msgprint(("Appointment was created. But no lead was found. Please check the email to confirm")
			)
    
    
    

   


    # doctor_email = frappe.db.get_value("Doctor", doc.custom_doctor, "email")
    # if not doctor_email:
    #     frappe.throw(f"The selected Doctor '{doc.custom_doctor}' does not have an email address set.")
    
    # # Check if a User already exists with this email
    # if not frappe.db.exists("User", doctor_email):
    #     frappe.throw(f"No User exists with the email '{doctor_email}'. Please create a User for this Doctor.")
    
    # # Optionally, set user permissions for the Doctor's email (if needed)
    # if not frappe.db.exists("User Permission", {"user": frappe.session.user, "for_value": doctor_email}):
    #     frappe.get_doc({
    #         "doctype": "User Permission",
    #         "user": frappe.session.user,
    #         "allow": "Doctor",
    #         "for_value": doctor_email
    #     }).insert(ignore_permissions=True)
        
    # frappe.msgprint("success")

