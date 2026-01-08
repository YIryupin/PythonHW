import time
import psycopg2
from psycopg2.extras import RealDictCursor

#from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


#def get_connection():
#    """
#    Возвращает новое соединение с PostgreSQL.
#    Используется синхронный драйвер psycopg2 — для небольшого бота этого достаточно.
#    """
#    return psycopg2.connect(
#        host=DB_HOST,
#        port=DB_PORT,
#        dbname=DB_NAME,
#        user=DB_USER,
#        password=DB_PASSWORD,
#        cursor_factory=RealDictCursor,
#    )



class DatabaseManager:
    def __init__(self, host, port, database, user, password):
        max_attempts: int = 10 
        delay_seconds: int = 3
        """
        Ждём, пока база данных будет доступна.
        Полезно при старте через docker-compose, когда контейнер бота поднимается
        быстрее, чем Postgres.
        """
        for attempt in range(1, max_attempts + 1):
            try:
                self.connection = psycopg2.connect(
                    host=host,
                    port=port,
                    database=database,
                    user=user,
                    password=password,
                    cursor_factory=RealDictCursor
                )
                break
            except psycopg2.OperationalError as exc:
                print(f"Database is not ready yet (attempt {attempt}/{max_attempts}): {exc}")
                time.sleep(delay_seconds)
        if self.connection is None: RuntimeError("Database is not available after several attempts")
        #Авто завершение транзакций
        self.connection.autocommit = True

    def execute_procedure(self, procedure_name, params=None):
        """Выполнение хранимой процедуры"""
        with self.connection.cursor() as cursor:
            cursor.callproc(procedure_name, params or [])
            result = cursor.fetchall() if cursor.description else None
            self.connection.commit()
            return result

    def execute_query(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            self.connection.commit()

    def close(self):
        """Закрытие соединения"""
        if self.connection:
            self.connection.close()

class DBLib:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        
    def g21matches_getcounter(self, telegram_id):
        """
        Получение текущего значения счётчика спичек
        
        Args:
            db_manager: Объект DatabaseManager
            telegram_id: ID пользователя Telegram
        Returns:
            int: Текущее количество спичек
        """
        result = self.db_manager.execute_procedure(
            'g21matches_getcounter',
            [telegram_id]
        )

        if result and len(result) > 0:
            # Проверяем структуру результата
            row = result[0]
            
            if isinstance(row, dict):
                return row.get('g21matches_getcounter')                 
        
        return 21
    
    def g21matches_setcounter(self, telegram_id, match_counter):
        """
        Установка значения счётчика спичек
        
        Args:
            db_manager: Объект DatabaseManager
            telegram_id: ID пользователя Telegram
            match_counter: Новое значение счётчика
        """
        self.db_manager.execute_procedure(
            'g21matches_setcounter',
            [telegram_id, match_counter]
        )

    def CreateOrUpdateUser(self, telegram_id, username):
        """
        Создание или обновление пользователя
        
        Args:
            db_manager: Объект DatabaseManager
            telegram_id: ID пользователя Telegram
            username: Имя пользователя
        """
        self.db_manager.execute_procedure(
            'createorupdateuser',
            [telegram_id, username]
        )

    def ChangeUserGame(self, telegram_id, gameId):
        """
        Создание или обновление пользователя
        
        Args:
            db_manager: Объект DatabaseManager
            telegram_id: ID пользователя Telegram
            gameId: код игры
        """
        self.db_manager.execute_procedure(
            'changeusergame',
            [telegram_id, gameId]
        )

    def GetCurrentGame(self, telegram_id):
        """
        Запрос текущей игры пользователя
        
        Args:
            db_manager: Объект DatabaseManager
            telegram_id: ID пользователя Telegram
        """
        result = self.db_manager.execute_procedure(
            'getcurrentgame',
            [telegram_id]
        )
        if result and len(result) > 0:
            # Проверяем структуру результата
            row = result[0]
            
            if isinstance(row, dict):
                return row.get('getcurrentgame')                 
        return None


    def userplaylogs_gamestart(self, telegram_id):
        """
        Логирование начала игры
        
        Args:
            db_manager: Объект DatabaseManager
            telegram_id: ID пользователя Telegram
        """
        result = self.db_manager.execute_procedure(
            'userplaylogs_gamestart',
            [telegram_id]
        )
        # if result and len(result) > 0:
        #     return result[0][0]  # Возвращаем GameSessionId
        # return None

    def userplaylogs_gamefinish(self, telegram_id, game_status):
        """
        Логирование окончания игры
        
        Args:
            db_manager: Объект DatabaseManager
            telegram_id: ID пользователя Telegram
            game_status: Статус игры ('WinPlayer', 'WinBot', 'Nobody')
        """
        if game_status not in ['WinPlayer', 'WinBot', 'Nobody']:
            raise ValueError("Invalid game_status. Must be 'WinPlayer', 'WinBot', or 'Nobody'")
        
        self.db_manager.execute_procedure(
            'userplaylogs_gamefinish',
            [telegram_id, game_status]
        )

    def userplaylogs_playerstats(self, telegram_id, days_count=30):
        """
        Получение статистики игрока
        
        Args:
            db_manager: Объект DatabaseManager
            telegram_id: ID пользователя Telegram
            days_count: Количество дней для анализа (по умолчанию 30)
        
        Returns:
            dict: Статистика с ключами 'wins', 'losses', 'draws', 'total_games'
        """
        result = self.db_manager.execute_procedure(
            'userplaylogs_playerstats',
            [telegram_id, days_count]
        )
        
        return result