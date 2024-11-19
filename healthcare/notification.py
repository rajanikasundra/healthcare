
from frappe.model.document import Document
import frappe
from frappe.utils import now_datetime,  add_to_date

def send_reminder_to_receptionist():
	# Get current time and time 10 minutes from now
	now = now_datetime()
	ten_minutes_from_now =  add_to_date(now, minutes=10)

	# Fetch appointments within the next 10 minutes where notification is not sent
	upcoming_appointments = frappe.get_all(
		'Appointment Scheduling',
		filters={
			'appointement_date': ['between', [now, ten_minutes_from_now]],
			'status': 'Pending',  # Only for confirmed appointments
			'notification_sent': 0  # Notification not sent
		},
		fields=['name', 'patient_details', 'appointement_date']
	)

	for appointment in upcoming_appointments:
		# Fetch the receptionist (owner of the appointment)
		receptionist = appointment.patient_details

		# Send system notification to the receptionist
		create_system_notification(
			user=receptionist,
			message=f"Reminder: Appointment scheduled at {appointment.appointement_date} is starting soon."
		)

		# Mark the notification as sent
		frappe.db.set_value('Appointment Scheduling', appointment.name, 'notification_sent', 1)



def create_system_notification(user, message):
    frappe.publish_realtime(
        event="eval_js",
        message={"message": message},
        user=user
    )