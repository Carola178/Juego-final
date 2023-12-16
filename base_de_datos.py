import sqlite3
import pathlib

class DataBase:
    filename: str
    exists: bool
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor
    data: dict

    def __init__(self) -> None:
        self.filename = "datos.db"
        self.exists = pathlib.Path(self.filename).is_file()
        self.data = {}
        self.connection = None
        self.cursor = None
        self.connect()
        self.init_db()

    def connect(self) -> None:
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()

    def init_db(self) -> None:
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS player_data (player_id INTEGER, game_id INTEGER, score INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)"
        )
        self.connection.commit()

    def add_score(self, player_id: int, game_id: int, score: int) -> None:
        # Inserta la nueva puntuación usando la conexión establecida en la instancia
        self.cursor.execute(
            "INSERT INTO player_data (player_id, game_id, score) VALUES (?, ?, ?)",
            (player_id, game_id, score),
        )
        self.connection.commit()
        
    def load(self) -> None:
        self.connect()
        result = self.cursor.execute(
            "SELECT player_id, score FROM player_data ORDER BY player_id, score DESC"
        )
        print("=== Ranking 10 mejores puntajes ===")
        for r in result:
            player_id, score = r
            print(f"Player: {player_id}, Score: {score}")
            if player_id not in self.data:
                self.data[player_id] = []
            self.data[player_id].append(score)

    def show_last_10_scores(self, player_id_actual):
        result = self.cursor.execute(
            "SELECT player_id, score FROM player_data WHERE player_id = ? ORDER BY score DESC LIMIT 10",
            (player_id_actual,)
        )
        scores = result.fetchall()
        return scores


if __name__ == "__main__":
    db = DataBase()

    db.load()
    player_id_actual = 1 
    db.show_last_10_scores(player_id_actual)
