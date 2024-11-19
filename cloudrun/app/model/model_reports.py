from pydantic import BaseModel

from datetime import datetime


class JawImage(BaseModel):
    url: str
    file_name: str
    size: int


class Gemini(BaseModel):
    calculus: int
    gingivitis: int
    mouthUlcers: int
    discoloration: int
    caries: int
    
    def parse_style(self, data: int) -> str:
        if data == 0:
            return "tag green"
        elif data == 1:
            return "tag yellow"
        elif data == 2:
            return "tag orange"
        elif data == 3:
            return "tag red"
        else:
            return "Unknown"
    
    def parse_gemini(self, data: int) -> str:
        if data == 0:
            return "No sign"
        elif data == 1:
            return "Likely"
        elif data == 2:
            return "Likely"
        elif data == 3:
            return "Very likely"
        else:
            return "Unknown"
    
    @property
    def parsed_data(self):
        return {
            "calculus": self.parse_gemini(self.calculus),
            "calculus_style": self.parse_style(self.calculus),
            "gingivitis": self.parse_gemini(self.gingivitis),
            "gingivitis_style": self.parse_style(self.gingivitis),
            "mouthUlcers": self.parse_gemini(self.mouthUlcers),
            "mouthUlcers_style": self.parse_style(self.mouthUlcers),
            "discoloration": self.parse_gemini(self.discoloration),
            "discoloration_style": self.parse_style(self.discoloration),
            "caries": self.parse_gemini(self.caries),
            "caries_style": self.parse_style(self.caries),
        }


class DataReports(BaseModel):
    answer_for_question_1: str
    answer_for_question_2: str
    answer_for_question_3: str
    answer_for_question_4: str
    answer_for_question_5: str
    answer_for_question_6: str
    name: str
    gender: str
    age: str
    gemini: Gemini
    country_data: str
    last_name: str
    bot_otp_in: bool
    upper_jaw: JawImage
    country_code: str
    lower_jaw: JawImage
    privacy_agreement: bool
    date_of_birth: str
    state: str
    front_teeth: JawImage
    promo_opt_in: bool
    email: str
    opt_in_date: str
    phone_number: str
    answered_date: str
    report_url: str

    @property
    def parsed_data(self):
        return {
            **self.gemini.parsed_data,
            "answer_for_question_1": self.answer_for_question_1,
            "answer_for_question_2": self.answer_for_question_2,
            "answer_for_question_3": self.answer_for_question_3,
            "answer_for_question_4": self.answer_for_question_4,
            "answer_for_question_5": self.answer_for_question_5,
            "answer_for_question_6": self.answer_for_question_6,
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "country_data": self.country_data,
            "last_name": self.last_name,
            "bot_otp_in": self.bot_otp_in,
            "upper_jaw_url": self.upper_jaw.url,
            "upper_jaw_file_name": self.upper_jaw.file_name,
            "upper_jaw_size": self.upper_jaw.size,
            "country_code": self.country_code,
            "lower_jaw_url": self.lower_jaw.url,
            "lower_jaw_file_name": self.lower_jaw.file_name,
            "lower_jaw_size": self.lower_jaw.size,
            "privacy_agreement": self.privacy_agreement,
            "date_of_birth": self.date_of_birth,
            "state": self.state,
            "front_teeth_url": self.front_teeth.url,
            "front_teeth_file_name": self.front_teeth.file_name,
            "front_teeth_size": self.front_teeth.size,
            "promo_opt_in": self.promo_opt_in,
            "email": self.email,
            "opt_in_date": self.opt_in_date,
            "phone_number": self.phone_number,
            "answered_date": self.answered_date,
            "report_url": self.report_url,
        }


def get_age_by_datetime(date_of_birth: str) -> str:
    birth_date = datetime.strptime(date_of_birth, '%m/%d/%Y')
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return str(age)


def parse_data(data: dict) -> DataReports:
    gemini_data = data.get('gemini_data', {})
    gemini = Gemini(
        calculus=int(gemini_data['calculus']),
        gingivitis=int(gemini_data['gingivitis']),
        mouthUlcers=int(gemini_data['mouthUlcer']),
        discoloration=int(gemini_data['discoloration']),
        caries=int(gemini_data['caries']),
    )
    report_data = {
        'answer_for_question_1': data['answer_for_question_1'],
        'answer_for_question_2': data['answer_for_question_2'],
        'answer_for_question_3': data['answer_for_question_3'],
        'answer_for_question_4': data['answer_for_question_4'],
        'answer_for_question_5': data['answer_for_question_5'],
        'answer_for_question_6': data['answer_for_question_6'],
        'name': f"{data['first_name']} {data['last_name']}",
        'gender': data['gender'],
        'age': get_age_by_datetime(data['date_of_birth']),
        'gemini': gemini,
        'country_data': data['country_data'],
        'last_name': data['last_name'],
        'bot_otp_in': data['bot_otp_in'],
        'upper_jaw': JawImage(**data['upper_jaw']),
        'country_code': data['country_code'],
        'lower_jaw': JawImage(**data['lower_jaw']),
        'privacy_agreement': data['privacy_agreement'],
        'date_of_birth': data['date_of_birth'],
        'state': data['state'],
        'front_teeth': JawImage(**data['front_teeth']),
        'promo_opt_in': data['promo_opt_in'],
        'email': data['email'],
        'opt_in_date': data['opt_in_date'],
        'phone_number': data['phone_number'],
        'answered_date': data['answered_date'],
        'report_url': data['report_url']
    }
    
    return DataReports(**report_data)
