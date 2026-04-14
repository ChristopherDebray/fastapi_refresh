import re
from sqlalchemy.exc import IntegrityError

def extract_field_from_integrity_error(error: IntegrityError) -> str:
    """
        Extract the field name from an IntegrityError of SQLAlchemy.
        
        Usefull for unique constraint error — parse the message
        psycopg2 pour récupérer le nom du champ concerné.
            
        Returns:
            The name of the field (ex: "email") or "unknown" if not parsable
    """
    match = re.search(r'Key \((\w+)\)', str(error.orig))
    return match.group(1) if match else "unknown"