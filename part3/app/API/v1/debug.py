from flask_restx import Namespace, Resource
from app import db
from sqlalchemy import text  # ✅ Ajouté

api = Namespace("debug", description="Debug endpoints")

@api.route("/db")
class DebugDB(Resource):
    def get(self):
        """Retourne la configuration de la base de données utilisée"""
        return {"database_uri": str(db.engine.url)}, 200


@api.route("/tables")
class DebugTables(Resource):
    def get(self):
        """Liste toutes les tables et le nombre d’enregistrements"""
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        result = {}

        for table in tables:
            # ✅ Correction ici : on utilise text()
            count = db.session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            result[table] = count

        return result, 200
