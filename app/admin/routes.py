from datetime import datetime, timezone

from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from app.admin import admin_bp
from app.admin.forms import (
    BandContentForm,
    BandMemberActivityForm,
    BandMemberForm,
    ContactInfoForm,
    MediaPhotoForm,
    MediaVideoForm,
    MerchItemForm,
    NewsForm,
    ReleaseForm,
    ShowForm,
    TrackForm,
)
from app.extensions import db
from app.models import (
    BandContent,
    BandMember,
    BandMemberActivity,
    ContactInfo,
    MediaPhoto,
    MediaVideo,
    MerchItem,
    News,
    Release,
    ReleaseTrack,
    Show,
)
from app.services.image_upload import ImageUploadError, save_image_upload


def duration_to_seconds(duration):
    if not duration:
        return None

    try:
        minutes_text, seconds_text = duration.split(":", maxsplit=1)

        minutes = int(minutes_text)
        seconds = int(seconds_text)
    except (TypeError, ValueError):
        return None

    if minutes < 0 or not 0 <= seconds <= 59:
        return None

    return minutes * 60 + seconds


def seconds_to_duration(seconds):
    if seconds is None:
        return ""

    minutes, remaining_seconds = divmod(seconds, 60)

    return f"{minutes:02d}:{remaining_seconds:02d}"


@admin_bp.get("/")
@login_required
def dashboard():
    news_count = News.query.count()
    show_count = Show.query.count()
    release_count = Release.query.count()

    return render_template(
        "admin/dashboard.html",
        news_count=news_count,
        show_count=show_count,
        release_count=release_count,
    )


@admin_bp.route(
    "/news/add",
    methods=["GET", "POST"],
)
@login_required
def add_news():
    form = NewsForm()

    if form.validate_on_submit():
        news = News(
            title=form.title.data.strip(),
            short_text=form.short_text.data.strip(),
            body=(form.body.data.strip() if form.body.data else None),
            link_url=(form.link_url.data.strip() if form.link_url.data else None),
            is_published=form.is_published.data,
            is_featured=form.is_featured.data,
        )

        if news.is_published:
            news.published_at = datetime.now(timezone.utc)

        db.session.add(news)
        db.session.commit()

        flash(
            "News item saved.",
            "success",
        )

        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin/news_form.html",
        form=form,
        page_title="Add News",
    )


@admin_bp.get("/news")
@login_required
def news_list():
    news_items = News.query.order_by(News.created_at.desc()).all()

    return render_template(
        "admin/news_list.html",
        news_items=news_items,
    )


@admin_bp.route(
    "/news/<int:news_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_news(news_id):
    news = db.get_or_404(News, news_id)

    form = NewsForm(obj=news)

    if form.validate_on_submit():
        was_published = news.is_published

        news.title = form.title.data.strip()
        news.short_text = form.short_text.data.strip()

        news.body = form.body.data.strip() if form.body.data else None

        news.link_url = form.link_url.data.strip() if form.link_url.data else None

        news.is_published = form.is_published.data
        news.is_featured = form.is_featured.data

        if news.is_published and not was_published:
            news.published_at = datetime.now(timezone.utc)

        if not news.is_published:
            news.published_at = None

        db.session.commit()

        flash(
            "News item updated.",
            "success",
        )

        return redirect(url_for("admin.news_list"))

    return render_template(
        "admin/news_form.html",
        form=form,
        page_title="Edit News",
        submit_label="Update news",
    )


@admin_bp.post("/news/<int:news_id>/delete")
@login_required
def delete_news(news_id):
    news = db.get_or_404(News, news_id)

    db.session.delete(news)
    db.session.commit()

    flash(
        "News item deleted.",
        "success",
    )

    return redirect(url_for("admin.news_list"))


@admin_bp.get("/shows")
@login_required
def shows_list():
    shows = Show.query.order_by(Show.show_date.desc()).all()

    return render_template(
        "admin/shows_list.html",
        shows=shows,
    )


@admin_bp.route(
    "/shows/add",
    methods=["GET", "POST"],
)
@login_required
def add_show():
    form = ShowForm()

    if form.validate_on_submit():
        try:
            poster_image = (
                form.poster_image.data.strip() if form.poster_image.data else None
            )

            if form.poster_file.data and form.poster_file.data.filename:
                poster_image = save_image_upload(
                    form.poster_file.data,
                    "shows",
                )

        except ImageUploadError as exc:
            form.poster_file.errors.append(str(exc))

        else:
            show = Show(
                show_date=form.show_date.data,
                show_time=form.show_time.data,
                venue=form.venue.data.strip(),
                city=form.city.data.strip(),
                country=form.country.data.strip(),
                other_bands=(
                    form.other_bands.data.strip() if form.other_bands.data else None
                ),
                poster_image=poster_image,
                event_url=(
                    form.event_url.data.strip() if form.event_url.data else None
                ),
                ticket_url=(
                    form.ticket_url.data.strip() if form.ticket_url.data else None
                ),
                notes=(form.notes.data.strip() if form.notes.data else None),
                is_published=form.is_published.data,
                is_cancelled=form.is_cancelled.data,
            )

            db.session.add(show)
            db.session.commit()

            flash(
                "Show saved.",
                "success",
            )

            return redirect(url_for("admin.shows_list"))

    return render_template(
        "admin/show_form.html",
        form=form,
        show=None,
        page_title="Add Show",
    )


@admin_bp.route(
    "/shows/<int:show_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_show(show_id):
    show = db.get_or_404(Show, show_id)

    form = ShowForm(obj=show)

    if form.validate_on_submit():
        try:
            poster_image = (
                form.poster_image.data.strip() if form.poster_image.data else None
            )

            if form.poster_file.data and form.poster_file.data.filename:
                poster_image = save_image_upload(
                    form.poster_file.data,
                    "shows",
                )

        except ImageUploadError as exc:
            form.poster_file.errors.append(str(exc))

        else:
            show.show_date = form.show_date.data
            show.show_time = form.show_time.data
            show.venue = form.venue.data.strip()
            show.city = form.city.data.strip()
            show.country = form.country.data.strip()

            show.other_bands = (
                form.other_bands.data.strip() if form.other_bands.data else None
            )

            show.poster_image = poster_image

            show.event_url = (
                form.event_url.data.strip() if form.event_url.data else None
            )

            show.ticket_url = (
                form.ticket_url.data.strip() if form.ticket_url.data else None
            )

            show.notes = form.notes.data.strip() if form.notes.data else None

            show.is_published = form.is_published.data
            show.is_cancelled = form.is_cancelled.data

            db.session.commit()

            flash(
                "Show updated.",
                "success",
            )

            return redirect(url_for("admin.shows_list"))

    return render_template(
        "admin/show_form.html",
        form=form,
        show=show,
        page_title="Edit Show",
    )


@admin_bp.post("/shows/<int:show_id>/delete")
@login_required
def delete_show(show_id):
    show = db.get_or_404(Show, show_id)

    db.session.delete(show)
    db.session.commit()

    flash(
        "Show deleted.",
        "success",
    )

    return redirect(url_for("admin.shows_list"))


@admin_bp.get("/releases")
@login_required
def releases_list():
    releases = Release.query.order_by(
        Release.sort_order.asc(),
        Release.release_year.desc(),
        Release.title.asc(),
    ).all()

    return render_template(
        "admin/releases_list.html",
        releases=releases,
    )


@admin_bp.route(
    "/releases/add",
    methods=["GET", "POST"],
)
@login_required
def add_release():
    form = ReleaseForm()

    if form.validate_on_submit():
        try:
            cover_image = (
                form.cover_image.data.strip() if form.cover_image.data else None
            )

            if form.cover_image_file.data and form.cover_image_file.data.filename:
                cover_image = save_image_upload(
                    form.cover_image_file.data,
                    "releases",
                )

        except ImageUploadError as exc:
            form.cover_image_file.errors.append(str(exc))

        else:
            release = Release(
                title=form.title.data.strip(),
                release_type=form.release_type.data,
                release_year=form.release_year.data,
                description=(
                    form.description.data.strip() if form.description.data else None
                ),
                cover_image=cover_image,
                artwork_credit=(
                    form.artwork_credit.data.strip()
                    if form.artwork_credit.data
                    else None
                ),
                label=(form.label.data.strip() if form.label.data else None),
                catalog_number=(
                    form.catalog_number.data.strip()
                    if form.catalog_number.data
                    else None
                ),
                format=(form.format.data.strip() if form.format.data else None),
                release_date=form.release_date.data,
                lineup=(form.lineup.data.strip() if form.lineup.data else None),
                recording_info=(
                    form.recording_info.data.strip()
                    if form.recording_info.data
                    else None
                ),
                engineering_credit=(
                    form.engineering_credit.data.strip()
                    if form.engineering_credit.data
                    else None
                ),
                mixing_mastering_credit=(
                    form.mixing_mastering_credit.data.strip()
                    if form.mixing_mastering_credit.data
                    else None
                ),
                additional_notes=(
                    form.additional_notes.data.strip()
                    if form.additional_notes.data
                    else None
                ),
                bandcamp_url=(
                    form.bandcamp_url.data.strip() if form.bandcamp_url.data else None
                ),
                spotify_url=(
                    form.spotify_url.data.strip() if form.spotify_url.data else None
                ),
                youtube_url=(
                    form.youtube_url.data.strip() if form.youtube_url.data else None
                ),
                other_url_label=(
                    form.other_url_label.data.strip()
                    if form.other_url_label.data
                    else None
                ),
                other_url=(
                    form.other_url.data.strip() if form.other_url.data else None
                ),
                sort_order=form.sort_order.data or 0,
                is_published=form.is_published.data,
            )

            db.session.add(release)
            db.session.commit()

            flash(
                "Release saved.",
                "success",
            )

            return redirect(url_for("admin.releases_list"))

    return render_template(
        "admin/release_form.html",
        form=form,
        release=None,
        page_title="Add Release",
    )


@admin_bp.route(
    "/releases/<int:release_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_release(release_id):
    release = db.get_or_404(
        Release,
        release_id,
    )

    form = ReleaseForm(obj=release)

    if form.validate_on_submit():
        try:
            cover_image = (
                form.cover_image.data.strip() if form.cover_image.data else None
            )

            if form.cover_image_file.data and form.cover_image_file.data.filename:
                cover_image = save_image_upload(
                    form.cover_image_file.data,
                    "releases",
                )

        except ImageUploadError as exc:
            form.cover_image_file.errors.append(str(exc))

        else:
            release.title = form.title.data.strip()
            release.release_type = form.release_type.data
            release.release_year = form.release_year.data

            release.description = (
                form.description.data.strip() if form.description.data else None
            )

            release.cover_image = cover_image

            release.artwork_credit = (
                form.artwork_credit.data.strip() if form.artwork_credit.data else None
            )

            release.label = form.label.data.strip() if form.label.data else None

            release.catalog_number = (
                form.catalog_number.data.strip() if form.catalog_number.data else None
            )

            release.format = form.format.data.strip() if form.format.data else None

            release.release_date = form.release_date.data

            release.lineup = form.lineup.data.strip() if form.lineup.data else None

            release.recording_info = (
                form.recording_info.data.strip() if form.recording_info.data else None
            )

            release.engineering_credit = (
                form.engineering_credit.data.strip()
                if form.engineering_credit.data
                else None
            )

            release.mixing_mastering_credit = (
                form.mixing_mastering_credit.data.strip()
                if form.mixing_mastering_credit.data
                else None
            )

            release.additional_notes = (
                form.additional_notes.data.strip()
                if form.additional_notes.data
                else None
            )

            release.bandcamp_url = (
                form.bandcamp_url.data.strip() if form.bandcamp_url.data else None
            )

            release.spotify_url = (
                form.spotify_url.data.strip() if form.spotify_url.data else None
            )

            release.youtube_url = (
                form.youtube_url.data.strip() if form.youtube_url.data else None
            )

            release.other_url_label = (
                form.other_url_label.data.strip() if form.other_url_label.data else None
            )

            release.other_url = (
                form.other_url.data.strip() if form.other_url.data else None
            )

            release.sort_order = form.sort_order.data or 0
            release.is_published = form.is_published.data

            db.session.commit()

            flash(
                "Release updated.",
                "success",
            )

            return redirect(url_for("admin.releases_list"))

    return render_template(
        "admin/release_form.html",
        form=form,
        release=release,
        page_title="Edit Release",
    )


@admin_bp.post("/releases/<int:release_id>/delete")
@login_required
def delete_release(release_id):
    release = db.get_or_404(
        Release,
        release_id,
    )

    db.session.delete(release)
    db.session.commit()

    flash(
        "Release deleted.",
        "success",
    )

    return redirect(url_for("admin.releases_list"))


@admin_bp.route(
    "/releases/<int:release_id>/tracks",
    methods=["GET", "POST"],
)
@login_required
def release_tracks(release_id):
    release = db.get_or_404(
        Release,
        release_id,
    )

    form = TrackForm()

    if form.validate_on_submit():
        track = ReleaseTrack(
            release_id=release.id,
            track_number=form.track_number.data,
            title=form.title.data.strip(),
            duration_seconds=duration_to_seconds(form.duration.data),
        )

        db.session.add(track)
        db.session.commit()

        flash(
            "Track added.",
            "success",
        )

        return redirect(
            url_for(
                "admin.release_tracks",
                release_id=release.id,
            )
        )

    return render_template(
        "admin/release_tracks.html",
        release=release,
        form=form,
    )


@admin_bp.route(
    "/releases/<int:release_id>/tracks/<int:track_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_release_track(release_id, track_id):
    release = db.get_or_404(
        Release,
        release_id,
    )

    track = db.get_or_404(
        ReleaseTrack,
        track_id,
    )

    if track.release_id != release.id:
        return "", 404

    form = TrackForm()

    if form.validate_on_submit():
        track.track_number = form.track_number.data
        track.title = form.title.data.strip()
        track.duration_seconds = duration_to_seconds(form.duration.data)

        db.session.commit()

        flash(
            "Track updated.",
            "success",
        )

        return redirect(
            url_for(
                "admin.release_tracks",
                release_id=release.id,
            )
        )

    if not form.is_submitted():
        form.track_number.data = track.track_number
        form.title.data = track.title
        form.duration.data = seconds_to_duration(track.duration_seconds)

    return render_template(
        "admin/release_track_form.html",
        release=release,
        track=track,
        form=form,
    )


@admin_bp.post("/releases/<int:release_id>/tracks/<int:track_id>/delete")
@login_required
def delete_release_track(release_id, track_id):
    release = db.get_or_404(
        Release,
        release_id,
    )

    track = db.get_or_404(
        ReleaseTrack,
        track_id,
    )

    if track.release_id != release.id:
        return "", 404

    db.session.delete(track)
    db.session.commit()

    flash(
        "Track deleted.",
        "success",
    )

    return redirect(
        url_for(
            "admin.release_tracks",
            release_id=release.id,
        )
    )


@admin_bp.route(
    "/band",
    methods=["GET", "POST"],
)
@login_required
def band_content():
    content = BandContent.query.first()

    if content is None:
        content = BandContent()
        db.session.add(content)
        db.session.commit()

    form = BandContentForm(obj=content)

    if form.validate_on_submit():
        content.intro = form.intro.data.strip() if form.intro.data else None

        content.history = form.history.data.strip() if form.history.data else None

        db.session.commit()

        flash(
            "Band content updated.",
            "success",
        )

        return redirect(url_for("admin.band_content"))

    members = BandMember.query.order_by(
        BandMember.sort_order.asc(),
        BandMember.name.asc(),
    ).all()

    return render_template(
        "admin/band.html",
        form=form,
        members=members,
    )


@admin_bp.get("/band/members/<int:member_id>/activity")
@login_required
def band_member_activity(member_id):
    member = db.get_or_404(
        BandMember,
        member_id,
    )

    activities = (
        BandMemberActivity.query.filter_by(
            band_member_id=member.id,
        )
        .order_by(
            BandMemberActivity.sort_order.asc(),
            BandMemberActivity.start_year.asc(),
            BandMemberActivity.id.asc(),
        )
        .all()
    )

    return render_template(
        "admin/band_member_activity.html",
        member=member,
        activities=activities,
    )


@admin_bp.route(
    "/band/members/<int:member_id>/activity/add",
    methods=["GET", "POST"],
)
@login_required
def add_band_member_activity(member_id):
    member = db.get_or_404(
        BandMember,
        member_id,
    )

    form = BandMemberActivityForm()

    if form.validate_on_submit():
        activity = BandMemberActivity(
            band_member_id=member.id,
            role=form.role.data.strip(),
            start_year=form.start_year.data,
            end_year=form.end_year.data,
            sort_order=form.sort_order.data or 0,
        )

        db.session.add(activity)
        db.session.commit()

        flash(
            "Activity period added.",
            "success",
        )

        return redirect(
            url_for(
                "admin.band_member_activity",
                member_id=member.id,
            )
        )

    return render_template(
        "admin/band_member_activity_form.html",
        member=member,
        form=form,
        activity=None,
        page_title="Add Activity Period",
    )


@admin_bp.route(
    "/band/members/<int:member_id>/activity/<int:activity_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_band_member_activity(member_id, activity_id):
    member = db.get_or_404(
        BandMember,
        member_id,
    )

    activity = db.get_or_404(
        BandMemberActivity,
        activity_id,
    )

    if activity.band_member_id != member.id:
        return "", 404

    form = BandMemberActivityForm(obj=activity)

    if form.validate_on_submit():
        activity.role = form.role.data.strip()
        activity.start_year = form.start_year.data
        activity.end_year = form.end_year.data
        activity.sort_order = form.sort_order.data or 0

        db.session.commit()

        flash(
            "Activity period updated.",
            "success",
        )

        return redirect(
            url_for(
                "admin.band_member_activity",
                member_id=member.id,
            )
        )

    return render_template(
        "admin/band_member_activity_form.html",
        member=member,
        form=form,
        activity=activity,
        page_title="Edit Activity Period",
    )


@admin_bp.post("/band/members/<int:member_id>/activity/<int:activity_id>/delete")
@login_required
def delete_band_member_activity(member_id, activity_id):
    member = db.get_or_404(
        BandMember,
        member_id,
    )

    activity = db.get_or_404(
        BandMemberActivity,
        activity_id,
    )

    if activity.band_member_id != member.id:
        return "", 404

    db.session.delete(activity)
    db.session.commit()

    flash(
        "Activity period deleted.",
        "success",
    )

    return redirect(
        url_for(
            "admin.band_member_activity",
            member_id=member.id,
        )
    )


@admin_bp.route(
    "/band/members/add",
    methods=["GET", "POST"],
)
@login_required
def add_band_member():
    form = BandMemberForm()

    if form.validate_on_submit():
        try:
            image = form.image.data.strip() if form.image.data else None

            if form.image_file.data and form.image_file.data.filename:
                image = save_image_upload(
                    form.image_file.data,
                    "band",
                )

        except ImageUploadError as exc:
            form.image_file.errors.append(str(exc))

        else:
            member = BandMember(
                name=form.name.data.strip(),
                slug=(form.slug.data.strip() if form.slug.data else None),
                role=form.role.data.strip(),
                image=image,
                bio=(form.bio.data.strip() if form.bio.data else None),
                other_projects=(
                    form.other_projects.data.strip()
                    if form.other_projects.data
                    else None
                ),
                stage_setup=(
                    form.stage_setup.data.strip() if form.stage_setup.data else None
                ),
                studio_setup=(
                    form.studio_setup.data.strip() if form.studio_setup.data else None
                ),
                sort_order=form.sort_order.data or 0,
                is_active=form.is_active.data,
            )

            db.session.add(member)
            db.session.commit()

            flash(
                "Band member added.",
                "success",
            )

            return redirect(url_for("admin.band_content"))

    return render_template(
        "admin/band_member_form.html",
        form=form,
        member=None,
        page_title="Add Band Member",
    )


@admin_bp.route(
    "/band/members/<int:member_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_band_member(member_id):
    member = db.get_or_404(
        BandMember,
        member_id,
    )

    form = BandMemberForm(
        obj=member,
        member=member,
    )

    if form.validate_on_submit():
        try:
            image = form.image.data.strip() if form.image.data else None

            if form.image_file.data and form.image_file.data.filename:
                image = save_image_upload(
                    form.image_file.data,
                    "band",
                )

        except ImageUploadError as exc:
            form.image_file.errors.append(str(exc))

        else:
            member.name = form.name.data.strip()
            member.slug = form.slug.data.strip() if form.slug.data else None
            member.role = form.role.data.strip()
            member.image = image

            member.bio = form.bio.data.strip() if form.bio.data else None

            member.other_projects = (
                form.other_projects.data.strip() if form.other_projects.data else None
            )

            member.stage_setup = (
                form.stage_setup.data.strip() if form.stage_setup.data else None
            )

            member.studio_setup = (
                form.studio_setup.data.strip() if form.studio_setup.data else None
            )

            member.sort_order = form.sort_order.data or 0
            member.is_active = form.is_active.data

            db.session.commit()

            flash(
                "Band member updated.",
                "success",
            )

            return redirect(url_for("admin.band_content"))

    return render_template(
        "admin/band_member_form.html",
        form=form,
        member=member,
        page_title="Edit Band Member",
    )


@admin_bp.post("/band/members/<int:member_id>/delete")
@login_required
def delete_band_member(member_id):
    member = db.get_or_404(
        BandMember,
        member_id,
    )

    db.session.delete(member)
    db.session.commit()

    flash(
        "Band member deleted.",
        "success",
    )

    return redirect(url_for("admin.band_content"))


@admin_bp.get("/media/videos")
@login_required
def media_videos():
    videos = MediaVideo.query.order_by(
        MediaVideo.sort_order.asc(),
        MediaVideo.year.desc(),
        MediaVideo.title.asc(),
    ).all()

    return render_template(
        "admin/media_videos.html",
        videos=videos,
    )


@admin_bp.route(
    "/media/videos/add",
    methods=["GET", "POST"],
)
@login_required
def add_media_video():
    form = MediaVideoForm()

    if form.validate_on_submit():
        video = MediaVideo(
            title=form.title.data.strip(),
            youtube_url=form.youtube_url.data.strip(),
            description=(
                form.description.data.strip() if form.description.data else None
            ),
            year=form.year.data,
            sort_order=form.sort_order.data or 0,
            is_published=form.is_published.data,
        )

        db.session.add(video)
        db.session.commit()

        flash(
            "Video saved.",
            "success",
        )

        return redirect(url_for("admin.media_videos"))

    return render_template(
        "admin/media_video_form.html",
        form=form,
        page_title="Add Video",
    )


@admin_bp.route(
    "/media/videos/<int:video_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_media_video(video_id):
    video = db.get_or_404(
        MediaVideo,
        video_id,
    )

    form = MediaVideoForm(obj=video)

    if form.validate_on_submit():
        video.title = form.title.data.strip()
        video.youtube_url = form.youtube_url.data.strip()

        video.description = (
            form.description.data.strip() if form.description.data else None
        )

        video.year = form.year.data
        video.sort_order = form.sort_order.data or 0
        video.is_published = form.is_published.data

        db.session.commit()

        flash(
            "Video updated.",
            "success",
        )

        return redirect(url_for("admin.media_videos"))

    return render_template(
        "admin/media_video_form.html",
        form=form,
        page_title="Edit Video",
    )


@admin_bp.post("/media/videos/<int:video_id>/delete")
@login_required
def delete_media_video(video_id):
    video = db.get_or_404(
        MediaVideo,
        video_id,
    )

    db.session.delete(video)
    db.session.commit()

    flash(
        "Video deleted.",
        "success",
    )

    return redirect(url_for("admin.media_videos"))


@admin_bp.get("/media/photos")
@login_required
def media_photos():
    photos = MediaPhoto.query.order_by(
        MediaPhoto.sort_order.asc(),
        MediaPhoto.event_date.desc(),
        MediaPhoto.id.desc(),
    ).all()

    return render_template(
        "admin/media_photos.html",
        photos=photos,
    )


@admin_bp.route(
    "/media/photos/add",
    methods=["GET", "POST"],
)
@login_required
def add_media_photo():
    form = MediaPhotoForm()

    if form.validate_on_submit():
        try:
            image_path = form.image_path.data.strip() if form.image_path.data else None

            if form.image_file.data and form.image_file.data.filename:
                image_path = save_image_upload(
                    form.image_file.data,
                    "media",
                )

        except ImageUploadError as exc:
            form.image_file.errors.append(str(exc))

        else:
            photo = MediaPhoto(
                title=(form.title.data.strip() if form.title.data else None),
                image_path=image_path,
                image_url=(
                    form.image_url.data.strip() if form.image_url.data else None
                ),
                photographer=(
                    form.photographer.data.strip() if form.photographer.data else None
                ),
                source_url=(
                    form.source_url.data.strip() if form.source_url.data else None
                ),
                event_name=(
                    form.event_name.data.strip() if form.event_name.data else None
                ),
                event_date=form.event_date.data,
                description=(
                    form.description.data.strip() if form.description.data else None
                ),
                sort_order=form.sort_order.data or 0,
                is_published=form.is_published.data,
            )

            db.session.add(photo)
            db.session.commit()

            flash(
                "Photo saved.",
                "success",
            )

            return redirect(url_for("admin.media_photos"))

    return render_template(
        "admin/media_photo_form.html",
        form=form,
        photo=None,
        page_title="Add Photo",
    )


@admin_bp.route(
    "/media/photos/<int:photo_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_media_photo(photo_id):
    photo = db.get_or_404(
        MediaPhoto,
        photo_id,
    )

    form = MediaPhotoForm(obj=photo)

    if form.validate_on_submit():
        try:
            image_path = form.image_path.data.strip() if form.image_path.data else None

            if form.image_file.data and form.image_file.data.filename:
                image_path = save_image_upload(
                    form.image_file.data,
                    "media",
                )

        except ImageUploadError as exc:
            form.image_file.errors.append(str(exc))

        else:
            photo.title = form.title.data.strip() if form.title.data else None

            photo.image_path = image_path

            photo.image_url = (
                form.image_url.data.strip() if form.image_url.data else None
            )

            photo.photographer = (
                form.photographer.data.strip() if form.photographer.data else None
            )

            photo.source_url = (
                form.source_url.data.strip() if form.source_url.data else None
            )

            photo.event_name = (
                form.event_name.data.strip() if form.event_name.data else None
            )

            photo.event_date = form.event_date.data

            photo.description = (
                form.description.data.strip() if form.description.data else None
            )

            photo.sort_order = form.sort_order.data or 0
            photo.is_published = form.is_published.data

            db.session.commit()

            flash(
                "Photo updated.",
                "success",
            )

            return redirect(url_for("admin.media_photos"))

    return render_template(
        "admin/media_photo_form.html",
        form=form,
        photo=photo,
        page_title="Edit Photo",
    )


@admin_bp.post("/media/photos/<int:photo_id>/delete")
@login_required
def delete_media_photo(photo_id):
    photo = db.get_or_404(
        MediaPhoto,
        photo_id,
    )

    db.session.delete(photo)
    db.session.commit()

    flash(
        "Photo deleted.",
        "success",
    )

    return redirect(url_for("admin.media_photos"))


@admin_bp.route(
    "/contact",
    methods=["GET", "POST"],
)
@login_required
def contact_info():
    contact = ContactInfo.query.first()

    if contact is None:
        contact = ContactInfo()
        db.session.add(contact)
        db.session.commit()

    form = ContactInfoForm(obj=contact)

    if form.validate_on_submit():
        contact.intro = form.intro.data.strip() if form.intro.data else None

        contact.general_email = (
            form.general_email.data.strip() if form.general_email.data else None
        )

        contact.booking_email = (
            form.booking_email.data.strip() if form.booking_email.data else None
        )

        contact.press_email = (
            form.press_email.data.strip() if form.press_email.data else None
        )

        contact.facebook_url = (
            form.facebook_url.data.strip() if form.facebook_url.data else None
        )

        contact.instagram_url = (
            form.instagram_url.data.strip() if form.instagram_url.data else None
        )

        contact.youtube_url = (
            form.youtube_url.data.strip() if form.youtube_url.data else None
        )

        contact.bandcamp_url = (
            form.bandcamp_url.data.strip() if form.bandcamp_url.data else None
        )

        db.session.commit()

        flash(
            "Contact information updated.",
            "success",
        )

        return redirect(url_for("admin.contact_info"))

    return render_template(
        "admin/contact.html",
        form=form,
    )


@admin_bp.get("/merch")
@login_required
def merch_items():
    items = MerchItem.query.order_by(
        MerchItem.sort_order.asc(),
        MerchItem.name.asc(),
    ).all()

    return render_template(
        "admin/merch_items.html",
        items=items,
    )


@admin_bp.route(
    "/merch/add",
    methods=["GET", "POST"],
)
@login_required
def add_merch_item():
    form = MerchItemForm()

    if form.validate_on_submit():
        try:
            image_path = None

            if form.image_file.data and form.image_file.data.filename:
                image_path = save_image_upload(
                    form.image_file.data,
                    "merch",
                )

        except ImageUploadError as exc:
            form.image_file.errors.append(str(exc))

        else:
            item = MerchItem(
                name=form.name.data.strip(),
                description=(
                    form.description.data.strip() if form.description.data else None
                ),
                price_cents=form.price_cents.data,
                image_path=image_path,
                external_url=(
                    form.external_url.data.strip() if form.external_url.data else None
                ),
                availability=(
                    form.availability.data.strip() if form.availability.data else None
                ),
                stock_quantity=form.stock_quantity.data,
                sort_order=form.sort_order.data or 0,
                is_published=form.is_published.data,
            )

            db.session.add(item)
            db.session.commit()

            flash(
                "Merch item saved.",
                "success",
            )

            return redirect(url_for("admin.merch_items"))

    return render_template(
        "admin/merch_item_form.html",
        form=form,
        item=None,
        page_title="Add Merch Item",
    )


@admin_bp.route(
    "/merch/<int:item_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_merch_item(item_id):
    item = db.get_or_404(
        MerchItem,
        item_id,
    )

    form = MerchItemForm(obj=item)

    if form.validate_on_submit():
        try:
            image_path = item.image_path

            if form.image_file.data and form.image_file.data.filename:
                image_path = save_image_upload(
                    form.image_file.data,
                    "merch",
                )

        except ImageUploadError as exc:
            form.image_file.errors.append(str(exc))

        else:
            item.name = form.name.data.strip()

            item.description = (
                form.description.data.strip() if form.description.data else None
            )

            item.price_cents = form.price_cents.data
            item.image_path = image_path

            item.external_url = (
                form.external_url.data.strip() if form.external_url.data else None
            )

            item.availability = (
                form.availability.data.strip() if form.availability.data else None
            )

            item.stock_quantity = form.stock_quantity.data
            item.sort_order = form.sort_order.data or 0
            item.is_published = form.is_published.data

            db.session.commit()

            flash(
                "Merch item updated.",
                "success",
            )

            return redirect(url_for("admin.merch_items"))

    return render_template(
        "admin/merch_item_form.html",
        form=form,
        item=item,
        page_title="Edit Merch Item",
    )


@admin_bp.post("/merch/<int:item_id>/delete")
@login_required
def delete_merch_item(item_id):
    item = db.get_or_404(
        MerchItem,
        item_id,
    )

    db.session.delete(item)
    db.session.commit()

    flash(
        "Merch item deleted.",
        "success",
    )

    return redirect(url_for("admin.merch_items"))
