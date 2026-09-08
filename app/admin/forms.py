import re

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    FileField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import (
    URL,
    DataRequired,
    Email,
    Length,
    NumberRange,
    Optional,
    Regexp,
    ValidationError,
)

from app.models import BandMember

IMAGE_PATH_PATTERN = re.compile(
    r"^[A-Za-z0-9_./ -]+\.(?:jpg|jpeg|png|webp|gif)$",
    re.IGNORECASE,
)


def validate_image_path(form, field):
    if not field.data:
        return

    value = field.data.strip()

    if value.startswith(("/", "\\")):
        raise ValidationError("Use a relative path inside the static directory.")

    if ".." in value:
        raise ValidationError("Parent directory references are not allowed.")

    if not IMAGE_PATH_PATTERN.fullmatch(value):
        raise ValidationError("Use a valid JPG, JPEG, PNG, WEBP or GIF image path.")


class NewsForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[
            DataRequired(),
            Length(max=200),
        ],
    )

    short_text = TextAreaField(
        "Short text",
        validators=[
            DataRequired(),
            Length(max=500),
        ],
    )

    body = TextAreaField(
        "Full text",
        validators=[
            Optional(),
        ],
    )

    link_url = StringField(
        "Optional link",
        validators=[
            Optional(),
            URL(),
            Length(max=500),
        ],
    )

    is_published = BooleanField("Publish immediately")

    is_featured = BooleanField("Feature on homepage")

    submit = SubmitField("Save news")


class ShowForm(FlaskForm):
    show_date = DateField(
        "Date",
        validators=[DataRequired()],
        format="%Y-%m-%d",
    )

    show_time = TimeField(
        "Time",
        validators=[Optional()],
        format="%H:%M",
    )

    venue = StringField(
        "Venue",
        validators=[
            DataRequired(),
            Length(max=200),
        ],
    )

    city = StringField(
        "City",
        validators=[
            DataRequired(),
            Length(max=150),
        ],
    )

    country = StringField(
        "Country",
        validators=[
            DataRequired(),
            Length(max=150),
        ],
    )

    other_bands = TextAreaField(
        "Other bands",
        validators=[Optional()],
    )

    poster_image = StringField(
        "Poster image",
        validators=[
            Optional(),
            Length(max=500),
            validate_image_path,
        ],
    )

    poster_file = FileField(
        "Upload poster",
        validators=[Optional()],
    )

    event_url = StringField(
        "Event URL",
        validators=[
            Optional(),
            URL(),
            Length(max=500),
        ],
    )

    ticket_url = StringField(
        "Ticket URL",
        validators=[
            Optional(),
            URL(),
            Length(max=500),
        ],
    )

    notes = TextAreaField(
        "Notes",
        validators=[Optional()],
    )

    is_published = BooleanField("Publish immediately")

    is_cancelled = BooleanField("Cancelled")

    submit = SubmitField("Save show")


class ReleaseForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[
            DataRequired(),
            Length(max=200),
        ],
    )

    release_type = SelectField(
        "Release type",
        choices=[
            ("album", "Album"),
            ("ep", "EP"),
            ("demo", "Demo"),
            ("single", "Single"),
            ("split", "Split album"),
            ("compilation", "Compilation"),
            ("other", "Other"),
        ],
        validators=[DataRequired()],
    )

    release_year = IntegerField(
        "Release year",
        validators=[
            Optional(),
            NumberRange(min=1980, max=2100),
        ],
    )

    description = TextAreaField(
        "Description",
        validators=[Optional()],
    )

    cover_image = StringField(
        "Cover image",
        validators=[
            Optional(),
            Length(max=500),
            validate_image_path,
        ],
    )

    cover_image_file = FileField(
        "Upload cover",
        validators=[Optional()],
    )

    artwork_credit = StringField(
        "Artwork credit",
        validators=[
            Optional(),
            Length(max=250),
        ],
    )

    label = StringField(
        "Label",
        validators=[
            Optional(),
            Length(max=250),
        ],
    )

    catalog_number = StringField(
        "Catalog number",
        validators=[
            Optional(),
            Length(max=100),
        ],
    )

    format = StringField(
        "Format",
        validators=[
            Optional(),
            Length(max=100),
        ],
    )

    release_date = DateField(
        "Release date",
        validators=[Optional()],
        format="%Y-%m-%d",
    )

    lineup = TextAreaField(
        "Lineup",
        validators=[Optional()],
    )

    recording_info = TextAreaField(
        "Recording information",
        validators=[Optional()],
    )

    engineering_credit = StringField(
        "Engineering credit",
        validators=[
            Optional(),
            Length(max=250),
        ],
    )

    mixing_mastering_credit = StringField(
        "Mixing / mastering credit",
        validators=[
            Optional(),
            Length(max=250),
        ],
    )

    additional_notes = TextAreaField(
        "Additional notes",
        validators=[Optional()],
    )

    bandcamp_url = StringField(
        "Bandcamp URL",
        validators=[
            Optional(),
            URL(),
            Length(max=500),
        ],
    )

    spotify_url = StringField(
        "Spotify URL",
        validators=[
            Optional(),
            URL(),
            Length(max=500),
        ],
    )

    youtube_url = StringField(
        "YouTube URL",
        validators=[
            Optional(),
            URL(),
            Length(max=500),
        ],
    )

    other_url_label = StringField(
        "Other URL label",
        validators=[
            Optional(),
            Length(max=100),
        ],
    )

    other_url = StringField(
        "Other URL",
        validators=[
            Optional(),
            URL(),
            Length(max=500),
        ],
    )

    sort_order = IntegerField(
        "Sort order",
        validators=[Optional()],
        default=0,
    )

    is_published = BooleanField("Publish immediately")

    submit = SubmitField("Save release")


class TrackForm(FlaskForm):
    track_number = IntegerField(
        "Track number",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=999),
        ],
    )

    title = StringField(
        "Title",
        validators=[
            DataRequired(),
            Length(max=250),
        ],
    )

    duration = StringField(
        "Duration",
        validators=[
            Optional(),
            Regexp(
                r"^\d{1,3}:\d{2}$",
                message="Use duration format MM:SS, for example 06:24.",
            ),
        ],
    )

    submit = SubmitField("Save track")


class BandContentForm(FlaskForm):
    intro = TextAreaField(
        "Band introduction",
        validators=[Optional()],
    )

    history = TextAreaField(
        "Band history",
        validators=[Optional()],
    )

    submit = SubmitField("Save band content")


class BandMemberForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(max=200),
        ],
    )

    def __init__(self, *args, member=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.member = member

    slug = StringField(
        "Profile URL slug",
        validators=[
            Optional(),
            Length(max=200),
            Regexp(
                r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
                message=(
                    "Use lowercase letters, numbers and single hyphens only, "
                    "for example henkka-disembowelment."
                ),
            ),
        ],
    )

    role = StringField(
        "Role",
        validators=[
            DataRequired(),
            Length(max=200),
        ],
    )

    image = StringField(
        "Image",
        validators=[
            Optional(),
            Length(max=500),
            validate_image_path,
        ],
    )

    image_file = FileField(
        "Upload portrait",
        validators=[Optional()],
    )

    bio = TextAreaField(
        "Biography",
        validators=[Optional()],
    )

    other_projects = TextAreaField(
        "Other bands / projects",
        validators=[Optional()],
    )

    stage_setup = TextAreaField(
        "Stage setup",
        validators=[Optional()],
    )

    studio_setup = TextAreaField(
        "Studio setup",
        validators=[Optional()],
    )

    sort_order = IntegerField(
        "Sort order",
        validators=[Optional()],
        default=0,
    )

    is_active = BooleanField("Current member")

    submit = SubmitField("Save member")

    def validate_slug(self, field):
        if not field.data:
            return

        slug = field.data.strip()

        existing_member = BandMember.query.filter_by(slug=slug).first()

        if existing_member and (
            self.member is None or existing_member.id != self.member.id
        ):
            raise ValidationError("This profile URL slug is already in use.")


class BandMemberActivityForm(FlaskForm):
    role = StringField(
        "Role",
        validators=[
            DataRequired(),
            Length(max=200),
        ],
    )

    start_year = IntegerField(
        "Start year",
        validators=[
            DataRequired(),
            NumberRange(min=2006, max=2100),
        ],
    )

    end_year = IntegerField(
        "End year",
        validators=[
            Optional(),
            NumberRange(min=2006, max=2100),
        ],
    )

    sort_order = IntegerField(
        "Sort order",
        validators=[Optional()],
        default=0,
    )

    submit = SubmitField("Save activity period")

    def validate_end_year(self, field):
        if field.data is None:
            return

        if self.start_year.data is not None and field.data < self.start_year.data:
            raise ValidationError("End year cannot be earlier than start year.")


class MediaVideoForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[
            DataRequired(),
            Length(max=200),
        ],
    )

    youtube_url = StringField(
        "YouTube URL",
        validators=[
            DataRequired(),
            URL(),
            Length(max=500),
        ],
    )

    description = TextAreaField(
        "Description",
        validators=[Optional()],
    )

    year = IntegerField(
        "Year",
        validators=[
            Optional(),
            NumberRange(min=1980, max=2100),
        ],
    )

    sort_order = IntegerField(
        "Sort order",
        validators=[Optional()],
        default=0,
    )

    is_published = BooleanField("Publish immediately")

    submit = SubmitField("Save video")


class MediaPhotoForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[
            Optional(),
            Length(max=200),
        ],
    )

    image_path = StringField(
        "Local image path",
        validators=[
            Optional(),
            Length(max=500),
            validate_image_path,
        ],
    )

    image_file = FileField(
        "Upload image",
        validators=[Optional()],
    )

    image_url = StringField(
        "External image URL",
        validators=[
            Optional(),
            URL(),
            Length(max=1000),
        ],
    )

    photographer = StringField(
        "Photographer",
        validators=[
            Optional(),
            Length(max=200),
        ],
    )

    source_url = StringField(
        "Source / photographer page",
        validators=[
            Optional(),
            URL(),
            Length(max=1000),
        ],
    )

    event_name = StringField(
        "Event",
        validators=[
            Optional(),
            Length(max=200),
        ],
    )

    event_date = DateField(
        "Date",
        validators=[Optional()],
    )

    description = TextAreaField(
        "Description",
        validators=[Optional()],
    )

    sort_order = IntegerField(
        "Sort order",
        validators=[Optional()],
        default=0,
    )

    is_published = BooleanField("Publish immediately")

    submit = SubmitField("Save photo")

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False

        image_path = self.image_path.data.strip() if self.image_path.data else ""
        image_url = self.image_url.data.strip() if self.image_url.data else ""
        image_file = (
            self.image_file.data
            if self.image_file.data and self.image_file.data.filename
            else None
        )

        if not image_path and not image_url and not image_file:
            self.image_file.errors.append(
                "Upload an image, add a local image path, or add an external image URL."
            )
            return False

        return True


class ContactInfoForm(FlaskForm):
    intro = TextAreaField(
        "Introduction",
        validators=[Optional()],
    )

    general_email = StringField(
        "General email",
        validators=[
            Optional(),
            Email(),
            Length(max=250),
        ],
    )

    booking_email = StringField(
        "Booking email",
        validators=[
            Optional(),
            Email(),
            Length(max=250),
        ],
    )

    press_email = StringField(
        "Press / media email",
        validators=[
            Optional(),
            Email(),
            Length(max=250),
        ],
    )

    facebook_url = StringField(
        "Facebook URL",
        validators=[
            Optional(),
            URL(),
            Length(max=500),
        ],
    )

    instagram_url = StringField(
        "Instagram URL",
        validators=[
            Optional(),
            URL(),
            Length(max=500),
        ],
    )

    youtube_url = StringField(
        "YouTube URL",
        validators=[
            Optional(),
            URL(),
            Length(max=500),
        ],
    )

    bandcamp_url = StringField(
        "Bandcamp URL",
        validators=[
            Optional(),
            URL(),
            Length(max=500),
        ],
    )

    submit = SubmitField("Save contact information")


class MerchItemForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(max=200),
        ],
    )

    description = TextAreaField(
        "Description",
        validators=[Optional()],
    )

    price_cents = IntegerField(
        "Price in cents",
        validators=[
            Optional(),
            NumberRange(min=0),
        ],
    )

    image_file = FileField(
        "Merch image",
        validators=[Optional()],
    )

    external_url = StringField(
        "External purchase URL",
        validators=[
            Optional(),
            URL(),
            Length(max=1000),
        ],
    )

    availability = StringField(
        "Availability",
        validators=[
            Optional(),
            Length(max=100),
        ],
    )

    stock_quantity = IntegerField(
        "Stock quantity",
        validators=[
            Optional(),
            NumberRange(min=0),
        ],
    )

    sort_order = IntegerField(
        "Sort order",
        validators=[Optional()],
        default=0,
    )

    is_published = BooleanField("Publish immediately")

    submit = SubmitField("Save merch item")
