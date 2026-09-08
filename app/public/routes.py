from datetime import datetime
from urllib.parse import parse_qs, urlparse
from zoneinfo import ZoneInfo

from flask import render_template

from app.models import (
    BandContent,
    BandMember,
    ContactInfo,
    MediaPhoto,
    MediaVideo,
    MerchItem,
    News,
    Release,
    Show,
)
from app.public import public_bp

SITE_TIMEZONE = ZoneInfo("Europe/Helsinki")


def get_youtube_video_id(url):
    parsed_url = urlparse(url)

    if parsed_url.hostname in {"youtu.be", "www.youtu.be"}:
        return parsed_url.path.lstrip("/")

    if parsed_url.hostname in {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
    }:
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]

        if parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/embed/", 1)[1].split("/", 1)[0]

        if parsed_url.path.startswith("/shorts/"):
            return parsed_url.path.split("/shorts/", 1)[1].split("/", 1)[0]

    return None


@public_bp.get("/")
def home():
    today = datetime.now(SITE_TIMEZONE).date()
    latest_news = (
        News.query.filter_by(is_published=True)
        .order_by(News.published_at.desc())
        .limit(5)
        .all()
    )

    featured_news = (
        News.query.filter(
            News.is_published.is_(True),
            News.is_featured.is_(True),
        )
        .order_by(
            News.published_at.desc(),
            News.id.desc(),
        )
        .first()
    )

    upcoming_shows = (
        Show.query.filter(
            Show.is_published.is_(True),
            Show.show_date >= today,
        )
        .order_by(Show.show_date.asc())
        .limit(5)
        .all()
    )

    recent_shows = (
        Show.query.filter(
            Show.is_published.is_(True),
            Show.show_date < today,
        )
        .order_by(Show.show_date.desc())
        .limit(3)
        .all()
    )

    latest_release = (
        Release.query.filter(
            Release.is_published.is_(True),
        )
        .order_by(
            Release.release_year.desc(),
            Release.sort_order.asc(),
        )
        .first()
    )

    band_content = BandContent.query.first()

    featured_photos = (
        MediaPhoto.query.filter(
            MediaPhoto.is_published.is_(True),
        )
        .order_by(
            MediaPhoto.sort_order.asc(),
            MediaPhoto.event_date.desc(),
            MediaPhoto.id.desc(),
        )
        .limit(3)
        .all()
    )

    featured_video = (
        MediaVideo.query.filter(
            MediaVideo.is_published.is_(True),
        )
        .order_by(
            MediaVideo.sort_order.asc(),
            MediaVideo.year.desc(),
            MediaVideo.title.asc(),
        )
        .first()
    )

    featured_video_item = None

    if featured_video:
        featured_video_id = get_youtube_video_id(
            featured_video.youtube_url,
        )

        if featured_video_id:
            featured_video_item = {
                "video": featured_video,
                "youtube_id": featured_video_id,
            }

    return render_template(
        "home.html",
        latest_news=latest_news,
        upcoming_shows=upcoming_shows,
        recent_shows=recent_shows,
        latest_release=latest_release,
        featured_photos=featured_photos,
        featured_video_item=featured_video_item,
        band_content=band_content,
        featured_news=featured_news,
    )


@public_bp.get("/news/<int:news_id>")
def news_detail(news_id):
    news_item = News.query.filter(
        News.id == news_id,
        News.is_published.is_(True),
    ).first_or_404()

    return render_template(
        "news_detail.html",
        news_item=news_item,
    )


@public_bp.get("/live")
def live():
    today = datetime.now(SITE_TIMEZONE).date()

    upcoming_shows = (
        Show.query.filter(
            Show.is_published.is_(True),
            Show.show_date >= today,
        )
        .order_by(Show.show_date.asc())
        .all()
    )

    recent_shows = (
        Show.query.filter(
            Show.is_published.is_(True),
            Show.show_date < today,
        )
        .order_by(Show.show_date.desc())
        .limit(3)
        .all()
    )

    return render_template(
        "live.html",
        upcoming_shows=upcoming_shows,
        recent_shows=recent_shows,
    )


@public_bp.route("/live/archive")
def live_archive():
    today = datetime.now(SITE_TIMEZONE).date()

    past_shows = (
        Show.query.filter(
            Show.is_published.is_(True),
            Show.show_date < today,
        )
        .order_by(Show.show_date.desc())
        .all()
    )

    return render_template(
        "live_archive.html",
        past_shows=past_shows,
    )


@public_bp.get("/music")
def music():
    releases = (
        Release.query.filter(
            Release.is_published.is_(True),
            Release.release_type != "demo",
        )
        .order_by(
            Release.release_year.desc(),
            Release.sort_order.asc(),
        )
        .all()
    )

    demos = (
        Release.query.filter(
            Release.is_published.is_(True),
            Release.release_type == "demo",
        )
        .order_by(
            Release.release_year.desc(),
            Release.sort_order.asc(),
        )
        .all()
    )

    return render_template(
        "music.html",
        releases=releases,
        demos=demos,
    )


@public_bp.get("/music/releases/<int:release_id>")
def release_detail(release_id):
    release = Release.query.filter(
        Release.id == release_id,
        Release.is_published.is_(True),
    ).first_or_404()

    return render_template(
        "release_detail.html",
        release=release,
    )


def format_member_activity(member):
    if not member.activities:
        return member.role

    parts = []

    for activity in member.activities:
        if activity.end_year is None:
            years = f"{activity.start_year}–"
        else:
            years = f"{activity.start_year}–{activity.end_year}"

        parts.append(f"{activity.role} ({years})")

    return ", ".join(parts)


@public_bp.get("/band")
def band():
    content = BandContent.query.first()

    members = (
        BandMember.query.filter_by(is_active=True)
        .order_by(
            BandMember.sort_order.asc(),
            BandMember.name.asc(),
        )
        .all()
    )

    former_members = (
        BandMember.query.filter_by(is_active=False)
        .order_by(
            BandMember.sort_order.asc(),
            BandMember.name.asc(),
        )
        .all()
    )

    for member in members:
        member.activity_display = format_member_activity(member)

    for member in former_members:
        member.activity_display = format_member_activity(member)

    return render_template(
        "band.html",
        content=content,
        members=members,
        former_members=former_members,
    )


@public_bp.get("/band/<string:slug>")
def band_member_profile(slug):
    member = BandMember.query.filter(
        BandMember.slug == slug,
        BandMember.is_active.is_(True),
    ).first_or_404()

    member.activity_display = format_member_activity(member)

    return render_template(
        "band_member_profile.html",
        member=member,
    )


@public_bp.get("/media")
def media():
    videos = (
        MediaVideo.query.filter(MediaVideo.is_published.is_(True))
        .order_by(
            MediaVideo.sort_order.asc(),
            MediaVideo.year.desc(),
            MediaVideo.title.asc(),
        )
        .all()
    )

    video_items = []

    for video in videos:
        video_id = get_youtube_video_id(video.youtube_url)

        if video_id:
            video_items.append(
                {
                    "video": video,
                    "youtube_id": video_id,
                }
            )

    photos = (
        MediaPhoto.query.filter(MediaPhoto.is_published.is_(True))
        .order_by(
            MediaPhoto.sort_order.asc(),
            MediaPhoto.event_date.desc(),
            MediaPhoto.id.desc(),
        )
        .all()
    )

    return render_template(
        "media.html",
        video_items=video_items,
        photos=photos,
    )


@public_bp.get("/contact")
def contact():
    contact_info = ContactInfo.query.first()

    return render_template(
        "contact.html",
        contact_info=contact_info,
    )


@public_bp.get("/merch")
def merch():
    items = (
        MerchItem.query.filter(MerchItem.is_published.is_(True))
        .order_by(
            MerchItem.sort_order.asc(),
            MerchItem.name.asc(),
        )
        .all()
    )

    contact_info = ContactInfo.query.first()

    return render_template(
        "merch.html",
        items=items,
        contact_info=contact_info,
    )
