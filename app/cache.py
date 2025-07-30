from app import redis_client

def cache_slug(slug, long_url):
    redis_client.setex(f"slug:{slug}", 86400, long_url)  # 1 day cache

def get_cached_slug(slug):
    return redis_client.get(f"slug:{slug}")

def invalidate_slug(slug):
    redis_client.delete(f"slug:{slug}")
