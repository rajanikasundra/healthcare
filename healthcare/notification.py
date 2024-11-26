
from frappe.model.document import Document
import frappe
from frappe.utils import now_datetime,  add_to_date

def send_reminder_to_receptionist():
	
	now = now_datetime()
	ten_minutes_from_now =  add_to_date(now, minutes=10)

	
	upcoming_appointments = frappe.get_all(
		'Appointment Scheduling',
		filters={
			'appointement_date': ['between', [now, ten_minutes_from_now]],
			'status': 'Pending',  
			'notification_sent': 0  
		},
		fields=['name', 'patient_details', 'appointement_date']
	)

	for appointment in upcoming_appointments:
		receptionist = appointment.patient_details

		create_system_notification(
			user=receptionist,
			message=f"Reminder: Appointment scheduled at {appointment.appointement_date} is starting soon."
		)

		frappe.db.set_value('Appointment Scheduling', appointment.name, 'notification_sent', 1)



def create_system_notification(user, message):
    frappe.publish_realtime(
        event="eval_js",
        message={"message": message},
        user=user
    )
    
    
    
    
    
    
# import frappe
# from frappe.utils import nowdate

# def send_payment_reminders(doc,events):
#     print("\n\n aaaaaaaaa1  \n\n")
#     overdue_invoices = frappe.get_all('Sales Invoice', filters={
#         'outstanding_amount': ['>', 0],
#         'due_date': ['<=', nowdate()]
#     })
#     print("\n\n aaaaaaaaa2  \n\n")
#     for invoice in overdue_invoices:
#         invoice_doc = frappe.get_doc('Sales Invoice', invoice.name)
#         print(f"\n\n aaaaaaaaa {invoice}  \n\n")
#         send_notification(invoice_doc)

# def send_notification(invoice_doc):
#     print("\n\n aaaaaaaaa2323  \n\n")
#     frappe.notify(
#         title="Payment Reminder: Invoice #{}".format(invoice_doc.name),
#         message="Dear Customer, your invoice is overdue. Please make the payment at the earliest.",
#         type="warning"  # You can change the type to "info", "error", etc.
#     )




import frappe
from frappe.utils import nowdate

def send_payment_reminders(doc, method):
    # Fetch overdue invoices
    overdue_invoices = frappe.get_all(
        'Sales Invoice',
        filters={
            'outstanding_amount': ['>', 0],
            'due_date': ['<=', nowdate()]
        },
        fields=['name', 'customer']  # Include necessary fields
    )

    for invoice in overdue_invoices:
        invoice_doc = frappe.get_doc('Sales Invoice', invoice.name)
        send_system_notifications(invoice_doc)

def send_system_notifications(invoice_doc):
    # Get specific patient user
    patient_user = frappe.db.get_value("Customer", invoice_doc.customer, "email_id")
    notified_users = []

    # Notify the patient if a user account exists
    if patient_user and frappe.db.exists("User", patient_user):
        notified_users.append(patient_user)

    # Notify roles like Administrator or Receptionist
    target_roles = ["Administrator", "Receptionist"]
    for role in target_roles:
        role_users = frappe.get_all(
            "Has Role",
            filters={"role": role},
            fields=["parent"]  # 'parent' refers to the User linked to the role
        )
        for user in role_users:
            if frappe.db.exists("User", user["parent"]):
                notified_users.append(user["parent"])

    # Remove duplicates in case a user has multiple roles
    notified_users = list(set(notified_users))
    print(f"\n\nNotified Users: {notified_users}\n\n")

    # Create notifications for each valid user
    for user in notified_users:
        notification = frappe.new_doc("Notification Log")
        notification.subject = f"{invoice_doc.name}"
        notification.document_type = "Sales Invoice"
        notification.document_name = invoice_doc.name
        notification.for_user = user
        notification.type = "Alert"
        notification.email_content = (
            f"Dear {user}, <br><br>"
            f"Invoice #{invoice_doc.name} is overdue. "
            f"Please follow up or make the payment at the earliest."
        )
        notification.save(ignore_permissions=True)



    










# set completed status in appoinment doctype
# def update_appointment_status(doc, method):
    
#     if doc.customer: 
#         appointment = frappe.get_doc("Appointment", doc.customer)
        
#         appointment.status = "Completed"
#         appointment.save()
        
#         frappe.msgprint(f"Appointment {appointment.name} status updated to Completed.")
