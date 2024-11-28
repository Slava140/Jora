from database import Base, pk_int, str_255_unique, created_at, updated_at


class UserM(Base):
    __tablename__ = 'users'

    id:                 pk_int
    username:           str_255_unique
    email:              str_255_unique
    hashed_password:    str
    created_at:         created_at
    updated_at:         updated_at
