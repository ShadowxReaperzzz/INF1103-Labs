
# =====================================================
# SUPPLIER CLASS
# Stores supplier information.
# Associated with Product through an object reference.
# =====================================================


class Supplier:
    def __init__(self, supplier_id: str, name: str,
                 contact_email: str):
        self.supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    def display_information(self) -> None:
        print(
            f"Supplier ID: {self.supplier_id} | "
            f"Name: {self.name} | "
            f"Email: {self.contact_email}"
        )

    def to_dict(self) -> dict:
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_email": self.contact_email
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data["supplier_id"],
            data["name"],
            data["contact_email"]
        )
