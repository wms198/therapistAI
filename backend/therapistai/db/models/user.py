from sqlmodel import Field, SQLModel


# small wrapper around field and sa columns kwargs
# https://sqlmodel.tiangolo.com/tutorial/indexes/#declare-indexes-with-sqlmodel
# https://github.com/fastapi/sqlmodel/issues/82#issuecomment-1005858022
# email: str = Field(sa_column_kwargs={"unique": True, "index": True})
def AField(*args, **kwargs):
    return Field(*args, sa_column_kwargs=kwargs)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    firstName: str
    lastName: str
    email: str = AField(unique=True, index=True)
    emailProvider: str
    password: str
