from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    emp_old_id = fields.Char(string='Old ID')
    religion = fields.Selection([
        ('muslim', 'Muslim'),
        ('non_muslim', 'Non Muslim'),
    ], string='Religion')

    id_type = fields.Selection([
        ('iqama', 'Iqama'),
        ('id', 'ID'),
    ], string='ID Type')

    id_number = fields.Char(string='ID Number')
    id_exp_grgn = fields.Char(string='ID Expiry Date (Gregorian)')
    id_exp_hijri = fields.Char(string='ID Expiry Date (Hijri)')
    passport_expiry = fields.Char(string='Passport Expiry Date')
    bnk_name = fields.Char(string='Bank Name')
    iban_no = fields.Char(string='IBANNumber')
    iqama_profession = fields.Char(string='Iqama Profession')
    iqama_profession_arabic = fields.Char(string='Iqama Profession (Arabic)')
    joining_date = fields.Date(string='Joining Date')
    leaving_date = fields.Date(string='Leaving Date ')
    ot_entitelment = fields.Selection([
        ('yes', 'YES'),
        ('no', 'NO'),
    ], string='OT Entitlement ')
    ot_rate = fields.Char('OT Rate')
    subscriber_no_gosi = fields.Char("Subscriber's Number GOSI")
    doj_gosi = fields.Char("D O J as per GOSI")
    subscription_period_status = fields.Char("Subscription period status (Arabic)")
    no_of_estoffice = fields.Char("The number of the establishment's office at the Ministry of Labor")
    no_of_mlabor = fields.Char("The facility number at the Ministry of Labor")
    sponsor_name_arabic = fields.Char("Sponsor Name (Arabic)")
    no_for_sponsor = fields.Char("Number for Sponsor")
    age_employee = fields.Char("Age Employee")
    emp_border_no = fields.Char("EMP BORDER NO")
    driving_license_no = fields.Char("Driving License No")
    driving_license_expiry_date = fields.Char("Driving License Expiry Date")
    grade = fields.Char("Grade")
    scope_points = fields.Char("Scope points")
    no_of_dependence = fields.Char("Number of Dependence")
