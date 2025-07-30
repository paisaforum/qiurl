import string, random
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import URL, User
from app.cache import cache_slug, get_cached_slug, invalidate_slug
from app import db

bp = Blueprint("routes", __name__)

def generate_slug(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

@bp.route("/", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        url = request.form.get("url")
        slug = request.form.get("slug") or generate_slug()
        if URL.query.filter_by(slug=slug).first():
            flash("Slug already in use", "danger")
        else:
            new_url = URL(slug=slug, original_url=url, user_id=current_user.id)
            db.session.add(new_url)
            db.session.commit()
            cache_slug(slug, url)
            flash(f"Short URL created: {request.host_url}{slug}", "success")
    urls = URL.query.order_by(URL.created_at.desc()).all() if current_user.is_admin else current_user.urls
    users = User.query.all() if current_user.is_admin else []
    return render_template("dashboard.html", urls=urls, users=users)

@bp.route("/delete/<slug>")
@login_required
def delete(slug):
    url = URL.query.filter_by(slug=slug).first_or_404()
    if current_user.id != url.user_id and not current_user.is_admin:
        return "Unauthorized", 403
    db.session.delete(url)
    db.session.commit()
    invalidate_slug(slug)
    flash("Link deleted", "info")
    return redirect(url_for("routes.dashboard"))

@bp.route("/<slug>")
def redirect_to(slug):
    cached = get_cached_slug(slug)
    if cached:
        return redirect(cached, code=302)
    url = URL.query.filter_by(slug=slug).first()
    if url:
        cache_slug(slug, url.original_url)
        return redirect(url.original_url, code=302)
    return "Link not found", 404
