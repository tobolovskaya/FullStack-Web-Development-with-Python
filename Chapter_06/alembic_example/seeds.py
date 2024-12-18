from connect import session
from models import Note, Record, Tag

if __name__ == "__main__":
    tag1 = Tag(name="groceries")
    tag2 = Tag(name="food")

    note = Note(name="Go to the store")

    note.tags = [tag1, tag2]

    rec1 = Record(description="Buy bread", note=note)
    rec2 = Record(description="Buy sausage 0.5 kg", note=note)
    rec3 = Record(description="Buy tomatoes 1 kg", note=note)

    session.add(note)
    session.commit()
    session.close()