from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class BookForm(FlaskForm):
    location = StringField("ქალაქი", validators=[DataRequired()])
    title = StringField("წიგნის სახელწოდება", validators=[DataRequired()])
    quantity = IntegerField("წიგნის რაოდენობა", validators=[DataRequired()])

    status = SelectField(
        "წიგნის მდგომარეობა",
        choices=[("new", "ახალი"), ("used", "გამოყენებული")],
        validators=[DataRequired()]
    )
    exchange_with = StringField("Exchange With")

    category = SelectField(
        "აირჩიეთ კატეგორია",
        choices=[
            ("buy", "შეძენა"),
            ("sell", "გაყიდვა"),
            ("gifting", "ჩუქება"),
            ("giveaway", "გაჩუქება"),
            ("exchange", "გაცვლა"),
            ("donation", "ქველმოქმედება"),
        ],
        validators=[DataRequired()]
    )

    img = FileField(
        "დაამატე სურათი",
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'])]
    )

    submit = SubmitField("დამატება")

    
         

 

    # def validate_password1(self,field):
    #     has_lower=False
    #     has_upper=False
    #     has_digit=False
    #     has_punctuations=False

    #     for char in field.data:
    #         if char in ascii_lowercase:
    #             has_lower=True
    #         if char in ascii_uppercase:
    #             has_upper=True
    #         if char in digits:
    #             has_digit=True
    #         if char in punctuation:
    #             has_punctuations=True
        

    #     if not has_lower:
    #         raise ValidationError("შეიტანეთ პატარა ასოები")
    #     if not has_upper:
    #         raise ValidationError("შეიტანეთ დიდი ასოები")
    #     if not has_digit:
    #         raise ValidationError("შეიტანეთ ციფრები")
    #     if not has_punctuations:
    #         raise ValidationError("შეიტანეთ პუნქტუაციის ნიშნები")
