from jinja2 import FileSystemLoader, Environment, select_autoescape

import config
from client.email import MailSender

smtp_config = {"smtp_server": config.smtp_server,
               "smtp_port": config.smtp_port,
               "username": config.sender_email,
               "password": config.pass_email,
               "sender_email": config.sender_email}


class MailEnv:

    def set_env_mail(self, templates: str, filename: str, **kwargs):
        env = Environment(loader=FileSystemLoader(templates),
                          autoescape=select_autoescape())
        template = env.get_template(filename)
        body = template.render(kwargs)
        return body


async def send_register_notify_email(message):
    subject = "Registration"
    templates = "mail_template"
    filename = "register_notify.html"
    data = {"username": message["username"]}
    body = MailEnv().set_env_mail(templates=templates, filename=filename, **data)
    MailSender(**smtp_config).send_mail(body=body, subject=subject, email_to=message["email"])


async def send_delete_project_notify_email(message):
    subjects = "Project Deleted"
    templates = "mail_template"
    filename = "projects_delete.html"
    data = {"username": message["username"], "name": message["name"], "deletion_date": message["deletion_date"]}
    body = MailEnv().set_env_mail(templates=templates, filename=filename, **data)
    MailSender(**smtp_config).send_mail(body=body, subject=subjects, email_to=message["email"])
