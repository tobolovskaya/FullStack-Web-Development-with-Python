from sqlalchemy import select

from connect import session
from models import Note, Tag, Record, note_m2m_tag

if __name__ == "__main__":
    q = (
        session.execute(
            select(
                Note.id,
                Note.name,
                Record.description,
                Record.done,
                Tag.name.label("tag"),
            )
            .join(Record)
            .join(note_m2m_tag)
            .join(Tag)
            .filter(Tag.name == "food")
        )
        .mappings()
        .all()
    )

    print(q)

    session.close()