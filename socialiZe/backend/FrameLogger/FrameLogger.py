import asyncio
import csv
import sqlite3
import threading
from datetime import datetime


class ThreadSafeFrameLogger:
    def __init__(self, db_path='frame_log.db', batch_size=100):
        """
        Initializes the logger with a SQLite database, sets up the batch size
        for logging, and prepares thread safety mechanisms.

        Args:
            db_path (str): The file path for the SQLite database.
                           Defaults to 'frame_log.db'.
            batch_size (int): The number of frame logs to accumulate before
                              batch writing to the database. Defaults to 100.
        """
        self.db_path = db_path
        self.batch_size = batch_size
        self.batch = []
        self.lock = threading.Lock()
        self._setup_db()

    def _setup_db(self):
        """
        Sets up the SQLite database table if it doesn't already exist.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS frame_log (
                    frame_number INTEGER,
                    timestamp TEXT
                )
            ''')
            conn.commit()

    def log_frame(self, frame_number):
        """
        Thread-safe logging of the frame number along with the absolute
        timestamp, buffering until batch size is reached.

        Args:
            frame_number (int): The current frame number to log.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        with self.lock:
            self.batch.append((frame_number, timestamp))
            if len(self.batch) >= self.batch_size:
                self._write_batch_to_db()

    def _write_batch_to_db(self):
        """
        Safely writes the buffered frame logs to the SQLite database.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany('INSERT INTO frame_log (frame_number, \
                               timestamp) VALUES (?, ?)', self.batch)
            conn.commit()
        self.batch.clear()  # Clear the batch after writing

    def flush(self):
        """
        Ensures any remaining logs in the batch are safely written to the
        database.
        """
        with self.lock:
            if self.batch:
                self._write_batch_to_db()

    def export_to_csv(self, csv_path):
        """
        Exports the logged frame data from the database to a specified CSV file.

        Args:
            csv_path (str): The file path for the output CSV file.
        """
        with self.lock, sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM frame_log')
            frame_logs = cursor.fetchall()

            with open(csv_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['frame_number', 'timestamp'])
                writer.writerows(frame_logs)

    def clear_database(self):
        """
        Clears the frame_log table in the database to be ready for subsequent
        recordings.
        """
        with self.lock, sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM frame_log')
            conn.commit()


class AsyncFrameLogger:
    def __init__(self, db_path='frame_log.db', batch_size=100):
        self.db_path = db_path
        self.batch_size = batch_size
        self.batch = []
        self.lock = asyncio.Lock()  # Use asyncio's Lock for async context
        self.loop = asyncio.get_running_loop()

    async def _setup_db(self):
        async with self.lock:
            await self.loop.run_in_executor(None, self._sync_setup_db)

    def _sync_setup_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS frame_log (
                    frame_number INTEGER,
                    timestamp TEXT
                )
            ''')
            conn.commit()

    async def log_frame(self, frame_number, timestamp):
        async with self.lock:
            self.batch.append((frame_number, 
                               timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')))
            if len(self.batch) >= self.batch_size:
                await self._write_batch_to_db()

    async def _write_batch_to_db(self):
        batch_copy = self.batch.copy()
        self.batch.clear()
        await self.loop.run_in_executor(None, self._sync_write_batch_to_db, batch_copy)

    def _sync_write_batch_to_db(self, batch):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany('INSERT INTO frame_log (frame_number, \
                               timestamp) VALUES (?, ?)', batch)
            conn.commit()

    async def flush(self):
        async with self.lock:
            if self.batch:
                await self._write_batch_to_db()
    
    async def clear_database(self):
        # Use a lock for thread safety
        async with self.lock:
            # Execute the blocking database operation in a background thread
            await self.loop.run_in_executor(None, self._sync_clear_database)

    def _sync_clear_database(self):
        # This function performs the actual database clearing operation
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM frame_log')
            conn.commit()

    async def export_to_csv(self, csv_path):
        # Ensure thread safety and asyncio compatibility
        async with self.lock:
            # Use run_in_executor to run blocking I/O operations in a background
            # thread
            await self.loop.run_in_executor(None, 
                                            self._sync_export_to_csv, csv_path)

    def _sync_export_to_csv(self, csv_path):
        # This is the synchronous part of exporting to CSV
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM frame_log')
            frame_logs = cursor.fetchall()

            with open(csv_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['frame_number', 'timestamp'])
                writer.writerows(frame_logs)
