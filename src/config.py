from environs import Env

env = Env()
env.read_env()

DB_HOST = env.str("DB_HOST")
DB_NAME = env.str("DB_NAME")
DB_PASS = env.str("DB_PASS")
DB_USER = env.str("DB_USER")
DB_PORT = env.str("DB_PORT")
JWT_SECRET = env.str("JWT_SECRET")
JWT_SECRET_AFTER_REGISTER = env.str("JWT_SECRET_AFTER_REGISTER")
