from app.core.redis import redis_client

redis_client.set("test_key", "connected")
value = redis_client.get("test_key")

print("Redis value:", value)