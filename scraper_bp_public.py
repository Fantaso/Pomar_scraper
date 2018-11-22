from requests_html import HTMLSession
import os
import datetime
import time

'''
from scraper import Scraper

# start scaning a range of cedulas
client_db = Scraper(17000000, 18000000)
client_db.start_range()

# start scaning a list of cedulas
client_db = Scraper(cedula_list)
client_db.start_list()
'''

class ScraperBp:
    # get session in website
    def __init__(self, begin_cedula = 0, end_cedula = 1, cedula_list = []):
        self.URL_WEBSITE        = ''
        self.URL_VERIFY_CEDULA  = ''
        self.URL_FORM           = ''

        self.session            = HTMLSession() # initiates session
        self._request           = self.session.get(self.URL_WEBSITE)

        self.persons            = []
        self.begin_cedula       = begin_cedula
        self.end_cedula         = end_cedula
        self.cedula_list        = cedula_list
        self.attrs_list         = ['#RegistroNombre', '#RegistroApellido', \
                                    '#RegistroNacimientoDay','#RegistroNacimientoMonth', '#RegistroNacimientoYear', \
                                    '#RegistroSexo', \
                                    '#RegistroEmail', '#RegistroAltemail', \
                                    '#RegistroCodigo', '#RegistroNumero', \
                                    '#RegistroCiudad','#RegistroCiudadpre', \
                                    '#RegistroConocimiento', \
                                    '#RegistroCatas1', '#RegistroDegustaciones1', '#RegistroCursos1', \
                                    '#RegistroVisitas1', '#RegistroEventos1', '#RegistroNinguna1']

    def __str__(self):
        return 'Session: <{}>'.format(self.URL_WEBSITE)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.URL_WEBSITE)

    # if verification is ok
    def verify_cedula(self, cedula):
        url = self.URL_VERIFY_CEDULA + str(cedula)
        r = self.session.post(url)
        if r.text is '2':
            return True
        return False

    # request form
    def get_data(self, cedula, verification_code = '2'):
        url = os.path.join(self.URL_FORM, str(cedula), verification_code)
        r = self.session.post(url)
        return r

    # parse data & save data
    def parse_data(self, response, cedula, date_found):
        person = {  'cedula': cedula,
                    'name': '',
                    'last_name': '',
                    'sex': '',
                    'email': '',
                    'email_alt': '',
                    'city': '',
                    'birthday_year': '',
                    'birthday_month': '',
                    'birthday_day': '',
                    'phone_code': '',
                    'phone_num': '',
                    'city_attend': '',
                    'experience': '',
                    'cata': '',
                    'degustacion': '',
                    'curso': '',
                    'visita': '',
                    'evento': '',
                    'ninguna': '',
                    'date_found': date_found,
                    }

        for attr in self.attrs_list:
            parsed = response.html.find(attr, first = True).attrs.get('value')
            # names
            if attr == '#RegistroNombre':
                person.update(name = parsed)
            if attr == '#RegistroApellido':
                person.update(last_name = parsed)
            # gender
            if attr == '#RegistroSexo':
                genders = response.html.find(attr + ' > option')
                for gender in genders:
                    if gender.attrs.get('selected'):
                        person.update(sex = gender.text)
            # emails
            if attr == '#RegistroEmail':
                person.update(email = parsed)
            if attr == '#RegistroAltemail':
                person.update(email_alt = parsed)
            # birthday
            if attr == '#RegistroNacimientoDay':
                days = response.html.find(attr + ' > option')
                for day in days:
                    if day.attrs.get('selected'):
                        person.update(birthday_day = day.text)
            if attr == '#RegistroNacimientoMonth':
                months = response.html.find(attr + ' > option')
                for month in months:
                    if month.attrs.get('selected'):
                        person.update(birthday_month = month.text)
            if attr == '#RegistroNacimientoYear':
                years = response.html.find(attr + ' > option')
                for year in years:
                    if year.attrs.get('selected'):
                        person.update(birthday_year = year.text)
            # phone
            if attr == '#RegistroCodigo':
                codes = response.html.find(attr + ' > option')
                for code in codes:
                    if code.attrs.get('selected'):
                        person.update(phone_code = code.text)
            if attr == '#RegistroNumero':
                num = response.html.find(attr, first = True).attrs.get('value')
                # print(num, type(num))
                person.update(phone_num = num)
            # residence city
            if attr == '#RegistroCiudad':
                cities = response.html.find(attr + ' > option')
                for city in cities:
                    if city.attrs.get('selected'):
                        # print(city.text, type(city.text))
                        person.update(city = city.text)
            # city_attend RegistroCiudadpre
            if attr == '#RegistroCiudadpre':
                cities = response.html.find(attr + ' > option')
                for city in cities:
                    if city.attrs.get('selected'):
                        # print(city.text, type(city.text))
                        person.update(city_attend = city.text)
            # experience RegistroConocimiento
            if attr == '#RegistroConocimiento':
                experiences = response.html.find(attr + ' > option')
                for experience in experiences:
                    if experience.attrs.get('selected'):
                        # print(city.text, type(city.text))
                        person.update(experience = experience.text)
            # cata RegistroCatas1
            if attr == '#RegistroCatas1':
                cata = response.html.find(attr, first = True).attrs.get('value')
                if cata and cata == '1':
                    cata = True
                elif cata and cata == '0':
                    cata = False
                person.update(cata = cata)
            # degustacion RegistroDegustaciones1
            if attr == '#RegistroDegustaciones1':
                degustacion = response.html.find(attr, first = True).attrs.get('value')
                if degustacion and degustacion == '1':
                    degustacion = True
                elif degustacion and degustacion == '0':
                    degustacion = False
                person.update(degustacion = degustacion)
            # curso RegistroCursos1
            if attr == '#RegistroCursos1':
                curso = response.html.find(attr, first = True).attrs.get('value')
                if curso and curso == '1':
                    curso = True
                elif curso and curso == '0':
                    curso = False
                person.update(curso = curso)
            # visita RegistroVisitas1
            if attr == '#RegistroVisitas1':
                visita = response.html.find(attr, first = True).attrs.get('value')
                if visita and visita == '1':
                    visita = True
                elif visita and visita == '0':
                    visita = False
                person.update(visita = visita)
            # evento RegistroEventos1
            if attr == '#RegistroEventos1':
                evento = response.html.find(attr, first = True).attrs.get('value')
                if evento and evento == '1':
                    evento = True
                elif evento and evento == '0':
                    evento = False
                person.update(evento = evento)
            # ninguna RegistroNinguna1
            if attr == '#RegistroNinguna1':
                ninguna = response.html.find(attr, first = True).attrs.get('value')
                if ninguna and ninguna == '1':
                    ninguna = True
                elif ninguna and ninguna == '0':
                    ninguna = False
                person.update(ninguna = ninguna)
        return person

    def start_range(self):
        print('[---] STARTING RANGE CRAWLER [---]\n\n')
        for cedula in range(self.begin_cedula, self.end_cedula):
            print('[???] Trying Cedula: {}'.format(cedula))
            time.sleep(0.05)
            if self.verify_cedula(cedula):
                print('[...] Cedula Verified: {}'.format(cedula))
                response = self.get_data(cedula)
                if response:
                    date_found = datetime.datetime.now()
                    person = self.parse_data(response, cedula, date_found)
                    time.sleep(0.05)
                    self.add_person_to_database(person)
                    self.print_person(person)
                    self.persons.append(person)
        return self.persons

    def start_list(self):
        print('[---] STARTING LIST CRAWLER [---]\n\n')
        for cedula in self.cedula_list:
            print('[???] Trying Cedula: {}'.format(cedula))
            time.sleep(0.05)
            if self.verify_cedula(cedula):
                print('[...] Cedula Verified: {}'.format(cedula))
                response = self.get_data(cedula)
                if response:
                    date_found = datetime.datetime.now()
                    person = self.parse_data(response, cedula, date_found)
                    time.sleep(0.05)
                    self.add_person_to_database(person)
                    self.print_person(person)
                    self.persons.append(person)
        return self.persons

    # utils
    @staticmethod
    def add_person_to_database(person):
        # get variables
        cedula          = person.get('cedula')
        sex             = person.get('sex', 'NA')
        if sex: sex = sex[:1]
        name            = person.get('name', 'NA')
        last_name       = person.get('last_name', 'NA')
        phone_code      = person.get('phone_code', 'NA')
        phone_num       = person.get('phone_num', 'NA')
        city            = person.get('city', 'NA')
        birthday_year   = person.get('birthday_year', 'NA')
        birthday_month  = person.get('birthday_month', 'NA')
        birthday_day    = person.get('birthday_day', 'NA')
        email           = person.get('email', 'NA')
        email_alt       = person.get('email_alt', 'NA')
        city_attend     = person.get('city_attend', 'NA')
        experience      = person.get('experience', 'NA')
        cata            = person.get('cata', 'NA')
        degustacion     = person.get('degustacion', 'NA')
        curso           = person.get('curso', 'NA')
        visita          = person.get('visita', 'NA')
        evento          = person.get('evento', 'NA')
        ninguna         = person.get('ninguna', 'NA')
        date_found      = person.get('date_found', 'NA')
        # format string
        person_details = f'{cedula}, {sex}, {city}, {name}, {last_name}, {phone_code}-{phone_num}, {birthday_year}-{birthday_month}-{birthday_day}, {email}, {email_alt}, {city_attend}, {experience}, {cata}, {degustacion}, {curso}, {visita}, {evento}, {ninguna}, {date_found}\n'
        # save person to file
        with open('database_pomar.txt', 'a') as file:
            file.write(person_details)

    @staticmethod
    def print_person(person):
        # get variables
        cedula          = person.get('cedula')
        sex             = person.get('sex', 'NA')
        if sex: sex = sex[:1]
        name            = person.get('name', 'NA')
        last_name       = person.get('last_name', 'NA')
        phone_code      = person.get('phone_code', 'NA')
        phone_num       = person.get('phone_num', 'NA')
        city            = person.get('city', 'NA')
        birthday_year   = person.get('birthday_year', 'NA')
        birthday_month  = person.get('birthday_month', 'NA')
        birthday_day    = person.get('birthday_day', 'NA')
        email           = person.get('email', 'NA')
        email_alt       = person.get('email_alt', 'NA')
        city_attend     = person.get('city_attend', 'NA')
        experience      = person.get('experience', 'NA')
        cata            = person.get('cata', 'NA')
        degustacion     = person.get('degustacion', 'NA')
        curso           = person.get('curso', 'NA')
        visita          = person.get('visita', 'NA')
        evento          = person.get('evento', 'NA')
        ninguna         = person.get('ninguna', 'NA')
        date_found      = person.get('date_found', 'NA')
        # format string
        person_details = f'{cedula}, {sex}, {city}, {name}, {last_name}, {phone_code}-{phone_num}, {birthday_year}-{birthday_month}-{birthday_day}, {email}, {email_alt}, {city_attend}, {experience}, {cata}, {degustacion}, {curso}, {visita}, {evento}, {ninguna}, {date_found}\n'
        # print person details in terminal
        print('[+++] Person: {}'.format(person_details))

    @staticmethod
    def get_cedula_list_from_db():
        cedula_list = []
        with open('database_pomar.txt', 'r') as file:
            for line in file.readlines():
                cedula_list.append(line.split(' ')[0])
        return cedula_list
