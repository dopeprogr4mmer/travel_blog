from django.template import loader
from django.views.generic.edit import FormView
from contactus.forms import ContactUsForm, SUBJECT_CHOICES
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import threading

recipients = ['supp0rt.travelrealindia@gmail.com']
bcc = ['rchouhan791@gmail.com']

def send(fromaddr, msg):
    smtp_server = "email-smtp.us-east-2.amazonaws.com"
    smtp_username = 'AKIA5H4YXSVOEZC3QUKP'
    smtp_password = 'BMP0VeHnbDxlTqJ6XoPt7K1fme67+RrcMh964z1i7xgx'
    smtp_port        = "2587"   #25, 587 or 2587
    smtp_do_tls      = True

    server      = smtplib.SMTP(
        host    = smtp_server,
        port    = smtp_port,
        timeout = 10
    )

    server.set_debuglevel(10)
    server.starttls()
    server.ehlo()
    server.login(smtp_username, smtp_password)
    server.sendmail(fromaddr, recipients + bcc, msg.as_string())
    server.quit()
    return True


class ContactUsView(FormView):
    template_name = 'contactus/contact.html'
    email_template_name = 'contactus/contact_notification_email.txt'
    form_class = ContactUsForm
    success_url = "/contact/success/"
    
    def get_initial(self):
        initial = super(ContactUsView, self).get_initial()
        if not self.request.user.is_anonymous:
            initial['name'] = self.request.user.get_full_name()
            initial['email'] = self.request.user.email
        initial['subject'] = '-----'

        return initial

    def form_valid(self, form):
        form_data = form.cleaned_data
        if not self.request.user.is_anonymous:
            form_data['username'] = self.request.user.username
        form_data['subject'] = dict(SUBJECT_CHOICES)[form_data['subject']]

        # POST to the support email
        tmpl = loader.get_template(self.email_template_name)
        content = tmpl.render(form_data)
        fromaddr         = "contact travelrealindia <contact.travelrealindia@gmail.com>"
        content_type     = "plain"
        msg              = email.mime.text.MIMEText( content, content_type, "utf-8" )
        msg["From"]      = fromaddr
        msg[ "Subject" ] = "Contact US Request/Feedback"
        msg[ "To" ]      = ",".join(recipients)
        task = threading.Thread(
                    target=send,
                    args=(fromaddr, msg)
                )
        task.start()

        return super(ContactUsView, self).form_valid(form)
