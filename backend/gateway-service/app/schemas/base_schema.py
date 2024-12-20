from pydantic import ConfigDict, BaseModel, Field


class BaseSchema(BaseModel):
    @property
    def as_db_dict(self):
        to_db = self.model_dump(exclude_defaults=True, exclude_none=True, exclude={"identifier", "id"})
        for key in ["id", "identifier"]:
            if key in self.model_dump().keys():
                to_db[key] = self.model_dump()[key].hex
        return to_db